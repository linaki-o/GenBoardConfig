"""核对用例：Excel + .c → 逐项差异结论。

两种模式：
- 通用模式：一行 Excel ↔ 一个配置项（config_key / expected_value）
- 档案模式（HSI 等）：一行 Excel ↔ 多个属性（引脚/方向/输出类型/上电电平…）
"""

from __future__ import annotations

from pathlib import Path

from ..domain.hsi import HsiEngine, parse_chip_pin
from ..domain.matcher import Matcher
from ..domain.models import (
    ChangeType,
    CheckResult,
    CheckStatus,
    CheckSummary,
    GPIORequirement,
    Source,
)
from ..domain.normalize import norm_key
from ..domain.planner import Planner
from ..domain.profiles import Profile
from ..domain.rules import RuleEngine
from ..infra.cconfig.parser import CConfigParser
from ..infra.excel.reader import ExcelParser
from ..infra.llm.orchestrator import LLMOrchestrator
from .context import ProgressFn, Session


class CheckUseCase:
    def __init__(
        self,
        excel_parser: ExcelParser,
        c_parser: CConfigParser,
        matcher: Matcher,
        rules: RuleEngine,
        planner: Planner,
        orchestrator: LLMOrchestrator | None = None,
        profile: Profile | None = None,
    ):
        self.excel_parser = excel_parser
        self.c_parser = c_parser
        self.matcher = matcher
        self.rules = rules
        self.planner = planner
        self.orchestrator = orchestrator
        self.profile = profile
        self._symbol_overrides: dict[str, str] = {}

    # ------------------------------------------------------------------
    def run(
        self,
        session: Session,
        progress: ProgressFn | None = None,
        use_llm: bool = True,
    ) -> CheckResult:
        def report(message: str, percent: float) -> None:
            if progress:
                progress(message, percent)

        report("解析 Excel ...", 0.05)
        excel_result = self.excel_parser.parse(session.excel_path)
        report(f"Excel 解析完成：{len(excel_result.requirements)} 行", 0.2)

        report("解析 C 配置文件 ...", 0.3)
        c_result = self.c_parser.parse(session.c_path)
        report(f"C 文件解析完成：{len(c_result.entries)} 个配置项", 0.42)

        session.c_parse = c_result
        session.warnings.extend(excel_result.warnings)
        session.warnings.extend(c_result.warnings)

        if self.profile is not None and self._is_profile_mode():
            results, engine = self._run_profile(excel_result, c_result, report, use_llm)
            entries_by_id = {e.id: e for e in c_result.entries}
            candidates_by_req = {}
        else:
            results = self._run_generic(excel_result, c_result, report, use_llm)
            entries_by_id = {e.id: e for e in c_result.entries}
            engine = None

        summary = self._summarize(results, excel_result, c_result)
        extra: dict = {"profile": self.profile.id if self.profile else "generic"}
        if excel_result.filter_stats:
            extra["filter_stats"] = excel_result.filter_stats
        check_result = CheckResult(
            requirements=excel_result.requirements,
            entries=c_result.entries,
            results=results,
            summary=summary,
            excel_path=session.excel_path,
            c_path=session.c_path,
            c_file_hash=c_result.file_hash,
            column_mapping=excel_result.column_mapping,
            llm_calls=self.orchestrator.stats.calls if self.orchestrator else 0,
            llm_tokens=(
                self.orchestrator.stats.prompt_tokens
                + self.orchestrator.stats.completion_tokens
                if self.orchestrator
                else 0
            ),
            warnings=session.warnings,
            extra=extra,
        )
        session.check_result = check_result
        session.profile = self.profile
        report("核对完成", 1.0)
        return check_result

    # ------------------------------------------------------------------
    def _is_profile_mode(self) -> bool:
        if self.profile is None:
            return False
        return any(spec.check != "none" for spec in self.profile.attributes)

    def _run_profile(
        self, excel_result, c_result, report: ProgressFn, use_llm: bool
    ):
        assert self.profile is not None
        report("按档案核对端口位表 ...", 0.5)
        engine = HsiEngine(self.profile, c_result.entries)
        results = engine.check(excel_result.requirements)
        report(f"核对完成：{len(results)} 行", 0.7)

        if use_llm and self.orchestrator is not None:
            self._llm_review(results, engine, report)

        report("生成修改建议 ...", 0.95)
        for res in results:
            self._plan_profile(res)
        return results, engine

    def _llm_review(self, results, engine: HsiEngine, report: ProgressFn) -> None:
        """对规则无法判定的残余项，交给大模型复核。"""
        reqs: list[GPIORequirement] = []
        candidates: dict[str, list[dict]] = {}
        index: dict[str, object] = {}
        for res in results:
            for attr in res.attribute_results:
                if not attr.checkable:
                    continue
                if attr.status not in {CheckStatus.AMBIGUOUS, CheckStatus.UNRESOLVED}:
                    continue
                entry = (
                    engine.entries_by_id.get(attr.evidence[0].entry_id)
                    if attr.evidence
                    else None
                )
                if entry is None:
                    continue
                rid = f"{res.requirement_id}#{attr.name}"
                reqs.append(
                    GPIORequirement(
                        id=rid,
                        sheet=res.requirement_id,
                        function_name=attr.label,
                        config_key=entry.key,
                        config_key_norm=norm_key(entry.key),
                        expected_value=attr.expected,
                    )
                )
                candidates[rid] = [
                    {
                        "id": entry.id,
                        "key": entry.key,
                        "value": entry.value_raw,
                        "line": entry.line,
                        "raw": entry.raw_text.strip()[:200],
                    }
                ]
                index[rid] = attr
        if not reqs:
            return
        report(f"大模型复核 {len(reqs)} 条判定不清的项 ...", 0.75)
        llm_results = self.orchestrator.check(
            reqs,
            candidates,
            entries_by_id=engine.entries_by_id,
            progress=lambda msg, p: report(msg, 0.75 + 0.15 * p),
        )
        for lr in llm_results:
            attr = index.get(lr.requirement_id)
            if attr is None:
                continue
            if (
                lr.status in {CheckStatus.MATCH, CheckStatus.MISMATCH}
                and lr.confidence >= 0.7
                and lr.evidence
            ):
                attr.status = lr.status
                attr.confidence = lr.confidence
                attr.source = Source.LLM
                attr.notes += f"；模型复核：{lr.notes}"
                if lr.status == CheckStatus.MISMATCH and lr.proposed_change.type != "none":
                    attr.change = lr.proposed_change
            else:
                attr.notes += "；模型复核未给出确定结论，仍需人工确认"
        report("大模型复核完成", 0.92)

    @staticmethod
    def _plan_profile(res) -> None:
        """把属性级结论汇总为行级修改建议。"""
        changes = [
            attr.change
            for attr in res.attribute_results
            if attr.change is not None and attr.change.type.value != "none"
        ]
        blocked = [
            attr.change
            for attr in res.attribute_results
            if attr.change is not None
            and attr.change.type.value == "none"
            and attr.change.reason
        ]
        if changes:
            res.proposed_change = changes[0]
            res.selected = True
        elif blocked:
            res.proposed_change = blocked[0]
            res.selected = False
            res.notes += "；" + blocked[0].reason
        else:
            res.proposed_change.type = ChangeType.NONE

    # ------------------------------------------------------------------
    def _run_generic(
        self, excel_result, c_result, report: ProgressFn, use_llm: bool
    ):
        entries = c_result.entries
        entries_by_id = {e.id: e for e in entries}

        report("归一化与候选匹配 ...", 0.5)
        candidates_by_req: dict[str, list[dict]] = {}
        results = []
        for req in excel_result.requirements:
            candidates = self.matcher.candidates(req, entries)
            candidates_by_req[req.id] = [
                {
                    "id": c.entry.id,
                    "key": c.entry.key,
                    "value": c.entry.value_raw,
                    "owner": c.entry.owner,
                    "line": c.entry.line,
                    "raw": c.entry.raw_text.strip()[:200],
                    "score": round(c.score, 2),
                }
                for c in candidates[:6]
            ]
            results.append(self.rules.decide(req, candidates, entries_by_id))

        report("规则判定完成，整理歧义项 ...", 0.6)
        results = [self.rules.downgrade(r) for r in results]

        if use_llm and self.orchestrator is not None:
            pending = [
                req
                for req, res in zip(excel_result.requirements, results)
                if res.status in {CheckStatus.AMBIGUOUS, CheckStatus.UNRESOLVED}
            ]
            if pending:
                report(f"大模型核对 {len(pending)} 条歧义/未决项 ...", 0.65)
                llm_results = self.orchestrator.check(
                    pending,
                    candidates_by_req,
                    entries_by_id=entries_by_id,
                    progress=lambda msg, p: report(msg, 0.65 + 0.25 * p),
                )
                by_req = {r.requirement_id: r for r in llm_results}
                for idx, res in enumerate(results):
                    replacement = by_req.get(res.requirement_id)
                    if replacement is not None:
                        results[idx] = replacement
                report("大模型核对完成", 0.92)

        report("生成变更建议 ...", 0.95)
        for res in results:
            self.planner.plan(res, entries_by_id)
        return results

    @staticmethod
    def _summarize(results, excel_result, c_result) -> CheckSummary:
        counts: dict[str, int] = {}
        for res in results:
            counts[res.status.value] = counts.get(res.status.value, 0) + 1
        return CheckSummary(
            total=len(results),
            counts=counts,
            mismatches=counts.get(CheckStatus.MISMATCH.value, 0),
            missing=counts.get(CheckStatus.MISSING.value, 0),
            ambiguous=counts.get(CheckStatus.AMBIGUOUS.value, 0),
            match=counts.get(CheckStatus.MATCH.value, 0),
            not_applicable=counts.get(CheckStatus.NOT_APPLICABLE.value, 0),
            unresolved=counts.get(CheckStatus.UNRESOLVED.value, 0),
            excel_rows=len(excel_result.requirements),
            c_entries=len(c_result.entries),
        )


def build_matcher(aliases: dict) -> Matcher:
    return Matcher((aliases or {}).get("config_key_aliases") or {})


def build_rules(aliases: dict, threshold: float) -> RuleEngine:
    return RuleEngine(
        value_aliases=(aliases or {}).get("value_aliases") or {},
        confidence_threshold=threshold,
    )


def build_planner() -> Planner:
    return Planner()


def describe_key(req_config_key: str) -> str:
    return norm_key(req_config_key)
