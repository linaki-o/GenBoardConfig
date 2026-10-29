"""离线 Mock Provider：本地启发式核对器，无需网络与密钥。

用途：演示/回归/无密钥环境下的端到端走查。它不是"大模型"，
但严格遵循与真实 Provider 相同的输入输出契约。
"""

from __future__ import annotations

import json
import re
import time

from .base import LLMProvider, LLMRequest, LLMResponse, TokenUsage
from ....domain.matcher import significant_tokens


def _norm_key(value: str) -> str:
    text = (value or "").strip().upper()
    return "_".join(part for part in text.replace("-", "_").split("_") if part)


def _norm(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if re.fullmatch(r"0[xX][0-9A-Fa-f]+", text):
        return str(int(text, 16))
    if re.fullmatch(r"\d+", text):
        return str(int(text))
    return text.upper()


def _as_number(value: str) -> int | None:
    text = (value or "").strip()
    if re.fullmatch(r"0[xX][0-9A-Fa-f]+", text):
        return int(text, 16)
    if re.fullmatch(r"\d+", text):
        return int(text)
    return None


def _pin(value: str) -> str:
    text = (value or "").strip().upper().replace(" ", "").replace("-", "_")
    if not text:
        return ""
    body = re.sub(r"^GPIO(?![A-Z0-9])", "", text)
    m = re.match(r"^([A-Z])[_\-]?(\d+)$", body)
    if m:
        return f"{m.group(1)}{m.group(2)}"
    return body if not body.isdigit() else body


def _fragments(net_name: str) -> list[str]:
    """网络名中的可识别片段（用于与注释做子串比对）。"""
    text = re.sub(r"[^A-Za-z0-9]+", " ", (net_name or "").upper()).strip()
    out = []
    for frag in text.split():
        if len(frag) >= 3:
            out.append(frag)
    return out


class MockProvider(LLMProvider):
    name = "mock"

    def __init__(self, delay_ms: int = 40):
        self.delay_ms = delay_ms

    def complete(self, request: LLMRequest) -> LLMResponse:
        started = time.perf_counter()
        if self.delay_ms:
            time.sleep(self.delay_ms / 1000)
        try:
            payload = json.loads(request.user)
        except json.JSONDecodeError:
            return LLMResponse(error="MockProvider: 请求负载不是合法 JSON")

        if "columns" in payload and "requirements" not in payload:
            result = self._identify_columns(payload)
        elif "items" in payload and "requirements" not in payload:
            if payload.get("items") and "excel_function" in payload["items"][0]:
                result = self._review_functions(payload)
            else:
                result = self._map_symbols(payload)
        else:
            result = self._check(payload)
        content = json.dumps(result, ensure_ascii=False)
        return LLMResponse(
            content=content,
            parsed=result,
            usage=TokenUsage(
                prompt_tokens=len(request.user) // 3,
                completion_tokens=len(content) // 3,
            ),
            latency_ms=int((time.perf_counter() - started) * 1000),
        )

    # ------------------------------------------------------------------
    def _identify_columns(self, payload: dict) -> dict:
        fields = payload.get("fields", [])
        columns = []
        for idx, header in enumerate(payload.get("headers", [])):
            field_name = ""
            for candidate in fields:
                if candidate and candidate.lower() in str(header).lower():
                    field_name = candidate
                    break
            columns.append({"index": idx, "field": field_name, "confidence": 0.8 if field_name else 0.2})
        return {"columns": columns}

    def _review_functions(self, payload: dict) -> dict:
        """功能名等效关系（离线启发式）。"""
        results = []
        for item in payload.get("items", []):
            excel_fn = _norm_key(item.get("excel_function", ""))
            header_fn = _norm_key(item.get("header_function", ""))
            gpio_type = (item.get("excel_gpio_type") or "").upper()
            options = [_norm_key(o) for o in (item.get("options") or [])]
            excel_tokens = {t for t in excel_fn.split("_") if len(t) > 1}
            header_tokens = {t for t in header_fn.split("_") if len(t) > 1}
            shared = excel_tokens & header_tokens
            if header_fn in {"GPI", "GPO_PP", "GPO_OD"}:
                equivalent = True
                confidence = 0.85
                reason = f"配置使用通用 GPIO {header_fn} 实现「{excel_fn}」，电气方向匹配"
            elif shared:
                equivalent = True
                confidence = 0.8
                reason = f"功能名共有关键字 {'/'.join(sorted(shared))}，判定为同一功能"
            elif header_fn in options or excel_fn in options:
                equivalent = True
                confidence = 0.6
                reason = "功能在该引脚的可选范围内，视为等效"
            else:
                equivalent = False
                confidence = 0.45
                reason = f"「{excel_fn}」与「{header_fn}」无语义交集，建议人工确认"
            results.append(
                {
                    "requirement_id": item.get("requirement_id", ""),
                    "equivalent": equivalent,
                    "confidence": confidence,
                    "reason": reason,
                    "electrical_match": True if gpio_type in {"IN", "OUT"} else None,
                    "electrical_reason": f"{header_fn} 与 {gpio_type} 方向兼容",
                }
            )
        return {"results": results}

    def _map_symbols(self, payload: dict) -> dict:
        mappings = []
        for item in payload.get("items", []):
            net = item.get("net_name", "")
            candidates = item.get("candidates", []) or []
            pin = (item.get("pin") or "").upper()
            fragments = _fragments(net)
            best, score = "", 0.0
            for cand in candidates:
                cand_score = 0.0
                cand_pin = (cand.get("pin") or "").upper()
                if pin and cand_pin and pin == cand_pin:
                    cand_score += 2.0
                comments = " ".join(cand.get("comments") or []).upper()
                if comments:
                    cand_score += 0.5
                if fragments and any(frag in comments for frag in fragments):
                    cand_score += 2.0
                tokens = significant_tokens(_norm_key(net))
                cand_tokens = significant_tokens(_norm_key(cand.get("group", "")))
                if tokens & cand_tokens:
                    cand_score += len(tokens & cand_tokens)
                if cand_score > score:
                    best, score = cand.get("group", ""), cand_score
            mappings.append(
                {
                    "net_name": net,
                    "group": best if score >= 2.0 else "none",
                    "confidence": 0.92 if score >= 3.5 else (0.7 if score >= 2.5 else 0.3),
                    "reason": "按引脚、注释与名称相似度匹配" if best else "无匹配宏组",
                }
            )
        return {"mappings": mappings}

    def _check(self, payload: dict) -> dict:
        items = []
        for req in payload.get("requirements", []):
            expected = req.get("expected_value", "")
            candidates = req.get("candidates", [])
            if not candidates:
                items.append(
                    self._item(req, "missing", [], "", 0.75, "未在配置文件中找到对应项")
                )
                continue
            best = candidates[0]
            current = best.get("value", "")
            if not self._key_related(req, best):
                items.append(
                    self._item(
                        req,
                        "ambiguous",
                        [best["id"]],
                        current,
                        0.5,
                        "候选配置项与该行配置项名称不相关，无法自动判定",
                    )
                )
                continue
            exp_num = _as_number(expected)
            cur_num = _as_number(current)
            if exp_num is not None and cur_num is not None:
                if exp_num == cur_num:
                    items.append(
                        self._item(req, "match", [best["id"]], current, 0.92, "取值一致")
                    )
                else:
                    items.append(
                        self._item(
                            req,
                            "mismatch",
                            [best["id"]],
                            current,
                            0.88,
                            f"期望 {expected}，实际 {current}",
                        )
                    )
                continue
            # 记法不同（引脚名 vs 编号）
            if _pin(current) and _pin(current) == _pin(req.get("pin_name", "")):
                items.append(
                    self._item(
                        req, "match", [best["id"]], current, 0.85, "配置以引脚名给出，与管脚一致"
                    )
                )
                continue
            items.append(
                self._item(
                    req,
                    "ambiguous",
                    [best["id"]],
                    current,
                    0.5,
                    "取值记法不同，无法自动判定，需人工确认",
                )
            )
        return {"items": items, "unresolved_reason": ""}

    @staticmethod
    def _key_related(req: dict, candidate: dict) -> bool:
        """候选配置项是否与该行的配置项名称相关（避免仅凭数值巧合）。"""
        req_key = _norm_key(req.get("config_key", ""))
        ent_key = _norm_key(candidate.get("key", ""))
        if not req_key or not ent_key:
            return True
        req_sig = significant_tokens(req_key)
        ent_sig = significant_tokens(ent_key)
        if not req_sig or not ent_sig:
            return True
        return bool(req_sig & ent_sig)

    def _item(
        self,
        req: dict,
        status: str,
        matched: list[str],
        current: str,
        confidence: float,
        notes: str,
    ) -> dict:
        change = {
            "type": "none",
            "target": "",
            "old_value": "",
            "new_value": "",
            "reason": "",
        }
        if status == "mismatch" and matched:
            change = {
                "type": "set_macro",
                "target": matched[0],
                "old_value": current,
                "new_value": req.get("expected_value", ""),
                "reason": notes,
            }
        return {
            "requirement_id": req.get("id", ""),
            "status": status,
            "matched_entry_ids": matched,
            "current_value": current,
            "expected_value": req.get("expected_value", ""),
            "confidence": confidence,
            "evidence": [
                {
                    "entry_id": matched[0] if matched else "",
                    "line": 0,
                    "snippet": notes,
                }
            ],
            "proposed_change": change,
            "notes": notes,
        }
