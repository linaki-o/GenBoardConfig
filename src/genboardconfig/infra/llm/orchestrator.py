"""LLM 编排：分批、组装提示、结构化校验、重试与预算控制。"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ...domain.models import (
    CheckStatus,
    ConfigEntry,
    Evidence,
    GPIORequirement,
    MatchResult,
    ProposedChange,
    Source,
)
from .masker import Masker
from .prompt_repo import PROMPT_VERSION, PromptRepo
from .provider.base import LLMProvider, LLMRequest
from .schema import (
    CHECK_JSON_SCHEMA,
    COLUMN_JSON_SCHEMA,
    FUNCTION_JSON_SCHEMA,
    SYMBOL_JSON_SCHEMA,
    LlmCheckResponse,
    LlmColumnResponse,
    LlmFunctionResponse,
    LlmSymbolResponse,
)

ProgressFn = Callable[[str, float], None]


@dataclass
class OrchestratorStats:
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    errors: int = 0
    latency_ms: int = 0
    batches: int = 0
    messages: list[str] = field(default_factory=list)
    events: list[str] = field(default_factory=list)   # 供界面日志展示


class LLMOrchestrator:
    def __init__(
        self,
        provider: LLMProvider,
        prompt_repo: PromptRepo,
        masker: Masker | None = None,
        temperature: float = 0.0,
        batch_size: int = 20,
        max_tokens: int = 3072,
    ):
        self.provider = provider
        self.prompt_repo = prompt_repo
        self.masker = masker or Masker()
        self.temperature = temperature
        self.batch_size = max(1, batch_size)
        self.max_tokens = max_tokens
        self.stats = OrchestratorStats()

    # ------------------------------------------------------------------
    def check(
        self,
        requirements: list[GPIORequirement],
        candidates_by_req: dict[str, list[dict[str, Any]]],
        entries_by_id: dict[str, ConfigEntry] | None = None,
        progress: ProgressFn | None = None,
    ) -> list[MatchResult]:
        """对歧义/未决项调用 LLM 判定。"""
        results: list[MatchResult] = []
        if not requirements:
            return results
        by_id = entries_by_id or {}
        total = len(requirements)
        done = 0
        for start in range(0, total, self.batch_size):
            batch = requirements[start : start + self.batch_size]
            payload = {
                "requirements": [
                    self._req_payload(req, candidates_by_req.get(req.id, []))
                    for req in batch
                ]
            }
            user = json.dumps(payload, ensure_ascii=False, indent=2)
            system = self._system_prompt("check_gpio")
            self.stats.events.append(
                f"→ 请求模型复核 {len(reqs)} 条（后端 {self.provider.name}/"
                f"{self.provider.model_name}）："
                + "、".join(f"{r.id}={r.expected_value}" for r in reqs[:5])
            )
            response = self.provider.complete(
                LLMRequest(
                    system=system,
                    user=self.masker.mask(user),
                    json_schema=CHECK_JSON_SCHEMA,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
            )
            self._absorb(response)
            if response.error or not isinstance(response.parsed, dict):
                results.extend(self._fallback(batch, response.error or "模型输出无法解析"))
            else:
                try:
                    parsed = LlmCheckResponse.model_validate(response.parsed)
                except Exception as exc:  # noqa: BLE001
                    results.extend(self._fallback(batch, f"结构校验失败: {exc}"))
                else:
                    results.extend(self._to_results(parsed, batch, by_id))
            done += len(batch)
            if progress:
                progress(f"大模型核对 {done}/{total}", done / total)
        return results

    def review_functions(
        self,
        items: list[dict[str, Any]],
        progress: ProgressFn | None = None,
    ) -> dict[str, tuple[bool, float, str]]:
        """功能名等效关系复核（RTK 专用功能名 vs Excel (App) 功能名）。

        items: [{requirement_id, net_name, excel_function, header_function,
                 pad, excel_gpio_type, options:[...]}]
        返回 {requirement_id: (equivalent, confidence, reason)}
        """
        out: dict[str, tuple[bool, float, str, bool | None, str]] = {}
        if not items:
            return out
        net_by_id = {i.get("requirement_id", ""): i.get("net_name", "") for i in items}
        payload = {"items": items}
        self.stats.events.append(
            f"→ 请求模型判定功能名等效关系 {len(items)} 条"
            f"（后端 {self.provider.name}/{self.provider.model_name}）："
            + "、".join(
                f"{i.get('net_name')}({i.get('excel_function')}↔{i.get('header_function')})"
                for i in items[:5]
            )
        )
        response = self.provider.complete(
            LLMRequest(
                system=self._system_prompt("review_functions"),
                user=self.masker.mask(json.dumps(payload, ensure_ascii=False, indent=2)),
                json_schema=FUNCTION_JSON_SCHEMA,
                temperature=0.0,
                max_tokens=2048,
            )
        )
        self._absorb(response)
        if response.error or not isinstance(response.parsed, dict):
            return out
        try:
            parsed = LlmFunctionResponse.model_validate(response.parsed)
        except Exception:  # noqa: BLE001
            return out
        for item in parsed.results:
            out[item.requirement_id] = (
                item.equivalent,
                item.confidence,
                item.reason,
                item.electrical_match,
                item.electrical_reason,
            )
            net = net_by_id.get(item.requirement_id, item.requirement_id)
            elec = "" if item.electrical_match is None else (
                "，电气方向兼容" if item.electrical_match else "，电气方向不兼容"
            )
            self.stats.events.append(
                f"  · {net}：模型判定 "
                f"{'等效' if item.equivalent else '不等效'}{elec}，"
                f"置信度 {item.confidence:.2f} —— {item.reason}"
            )
        if progress:
            progress(f"功能名复核完成：{len(out)}/{len(items)}", 1.0)
        return out

    def map_symbols(
        self,
        items: list[dict[str, Any]],
        progress: ProgressFn | None = None,
    ) -> dict[str, tuple[str, float]]:
        """网络名 → 板级配置宏组前缀的语义映射。

        items 形如 {"net_name": "EE_SCL", "pin": "PD2", "candidates": [...]}
        返回 {net_name: (group, confidence)}；无法确定的不返回。
        """
        mapping: dict[str, tuple[str, float]] = {}
        if not items:
            return mapping
        payload = {"items": items}
        response = self.provider.complete(
            LLMRequest(
                system=self._system_prompt("map_symbols"),
                user=self.masker.mask(json.dumps(payload, ensure_ascii=False, indent=2)),
                json_schema=SYMBOL_JSON_SCHEMA,
                temperature=0.0,
                max_tokens=2048,
            )
        )
        self._absorb(response)
        if response.error or not isinstance(response.parsed, dict):
            return mapping
        try:
            parsed = LlmSymbolResponse.model_validate(response.parsed)
        except Exception:  # noqa: BLE001
            return mapping
        for item in parsed.mappings:
            if item.group and item.group != "none":
                mapping[item.net_name] = (item.group, item.confidence)
        if progress:
            progress(f"符号映射完成：{len(mapping)}/{len(items)}", 1.0)
        return mapping

    def identify_columns(
        self,
        headers: list[str],
        sample_rows: list[list[str]],
        candidate_fields: list[str],
    ) -> LlmColumnResponse:
        payload = {
            "headers": headers,
            "sample_rows": sample_rows[:5],
            "fields": candidate_fields,
        }
        response = self.provider.complete(
            LLMRequest(
                system=self._system_prompt("identify_columns"),
                user=self.masker.mask(json.dumps(payload, ensure_ascii=False, indent=2)),
                json_schema=COLUMN_JSON_SCHEMA,
                temperature=0.0,
                max_tokens=1024,
            )
        )
        self._absorb(response)
        if response.error or not isinstance(response.parsed, dict):
            return LlmColumnResponse()
        try:
            return LlmColumnResponse.model_validate(response.parsed)
        except Exception:  # noqa: BLE001
            return LlmColumnResponse()

    # ------------------------------------------------------------------
    def _req_payload(
        self, req: GPIORequirement, candidates: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "id": req.id,
            "excel_row": req.row_no,
            "sheet": req.sheet,
            "pin_name": req.pin_name_raw,
            "gpio_num": req.gpio_num,
            "function": req.function_name,
            "config_key": req.config_key,
            "expected_value": req.expected_value,
            "chip_instance": req.chip_instance,
            "polarity": req.polarity,
            "pull": req.pull,
            "candidates": candidates,
        }

    def _system_prompt(self, name: str) -> str:
        template = self.prompt_repo.get(name)
        body = template.text or "（提示词模板缺失，请检查 config/prompts）"
        return f"{body}\n\n[prompt_version: {PROMPT_VERSION} | template: {name}]"

    def _absorb(self, response) -> None:
        self.stats.calls += 1
        self.stats.batches += 1
        self.stats.prompt_tokens += response.usage.prompt_tokens
        self.stats.completion_tokens += response.usage.completion_tokens
        self.stats.latency_ms += response.latency_ms
        if response.error:
            self.stats.errors += 1
            self.stats.messages.append(response.error[:200])
            self.stats.events.append(
                f"✗ 模型调用失败（{self.provider.name}/{self.provider.model_name}）："
                f"{response.error[:300]}"
            )
        else:
            self.stats.events.append(
                f"✓ 模型调用成功（{self.provider.name}/{self.provider.model_name}）："
                f"耗时 {response.latency_ms} ms，令牌 "
                f"{response.usage.prompt_tokens}+{response.usage.completion_tokens}"
            )

    def _fallback(self, batch: list[GPIORequirement], reason: str) -> list[MatchResult]:
        return [
            MatchResult(
                requirement_id=req.id,
                status=CheckStatus.UNRESOLVED,
                confidence=0.0,
                expected_value=req.expected_value,
                source=Source.LLM,
                notes=f"模型调用失败：{reason}",
            )
            for req in batch
        ]

    def _to_results(
        self,
        parsed: LlmCheckResponse,
        batch: list[GPIORequirement],
        by_id: dict[str, ConfigEntry],
    ) -> list[MatchResult]:
        out: list[MatchResult] = []
        item_map = {item.requirement_id: item for item in parsed.items}
        for req in batch:
            item = item_map.get(req.id)
            if item is None:
                out.append(
                    MatchResult(
                        requirement_id=req.id,
                        status=CheckStatus.UNRESOLVED,
                        expected_value=req.expected_value,
                        source=Source.LLM,
                        notes="模型未返回该条结论",
                    )
                )
                continue
            status = CheckStatus(item.status)
            evidence = [
                Evidence(entry_id=e.entry_id, line=e.line, snippet=e.snippet)
                for e in item.evidence
                if not e.entry_id or e.entry_id in by_id
            ]
            if status in {CheckStatus.MATCH, CheckStatus.MISMATCH} and not evidence:
                status = CheckStatus.AMBIGUOUS
                item.notes = (item.notes + "；模型结论缺少证据引用，已降级").strip("；")
            change = ProposedChange(
                type=item.proposed_change.type,
                target=item.proposed_change.target,
                old_value=item.proposed_change.old_value,
                new_value=item.proposed_change.new_value,
                reason=item.proposed_change.reason,
            )
            out.append(
                MatchResult(
                    requirement_id=req.id,
                    status=status,
                    confidence=item.confidence,
                    matched_entry_ids=[e for e in item.matched_entry_ids if e in by_id],
                    current_value=item.current_value,
                    expected_value=item.expected_value or req.expected_value,
                    evidence=evidence,
                    proposed_change=change,
                    source=Source.LLM,
                    notes=item.notes,
                )
            )
        return out
