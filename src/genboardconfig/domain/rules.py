"""判定规则引擎：把候选关联转成差异状态。"""

from __future__ import annotations

from .matcher import Candidate
from .models import (
    CheckStatus,
    ConfigEntry,
    Evidence,
    GPIORequirement,
    MatchResult,
    Source,
)
from .normalize import norm_gpio_num, norm_key, norm_pin, norm_value, values_equivalent

WEAK_SCORE = 0.55


class RuleEngine:
    def __init__(
        self,
        value_aliases: dict[str, list[str]] | None = None,
        confidence_threshold: float = 0.8,
    ):
        self.value_aliases = value_aliases or {}
        self.confidence_threshold = confidence_threshold

    def decide(
        self,
        req: GPIORequirement,
        candidates: list[Candidate],
        entries_by_id: dict[str, ConfigEntry],
    ) -> MatchResult:
        result = MatchResult(
            requirement_id=req.id,
            expected_value=req.expected_value,
            source=Source.DETERMINISTIC,
        )
        result.candidate_count = len(candidates)

        if not candidates:
            result.status = CheckStatus.MISSING
            result.confidence = 0.75
            result.notes = "未在配置文件中找到与该行对应的配置项"
            return result

        top = candidates[0]
        result.matched_entry_ids = [c.entry.id for c in candidates[:3]]
        result.current_value = top.entry.value_raw
        result.evidence = [
            Evidence(
                entry_id=c.entry.id,
                line=c.entry.line,
                snippet=c.entry.raw_text.strip()[:200],
            )
            for c in candidates[:3]
        ]

        # 多候选且取值不一致 → 歧义
        distinct = {
            norm_value(c.entry.value_raw, self.value_aliases) for c in candidates[:3]
        }
        if len(candidates) > 1 and len(distinct) > 1:
            result.status = CheckStatus.AMBIGUOUS
            result.confidence = 0.5
            result.notes = (
                f"存在 {len(candidates)} 个候选配置且取值不一致："
                + "、".join(f"L{c.entry.line} {c.entry.key}" for c in candidates[:3])
            )
            return result

        if top.entry.value_kind in {"expression", "none"}:
            result.status = CheckStatus.AMBIGUOUS
            result.confidence = 0.4
            result.notes = "配置值为表达式或无法定位，需人工确认"
            return result

        if not req.expected_value:
            result.status = CheckStatus.AMBIGUOUS
            result.confidence = 0.4
            result.notes = "Excel 未给出期望值"
            return result

        # 口径差异：配置以「引脚名」给出，Excel 以「编号」给出，但引脚本身一致
        ent_pin, _ = norm_pin(top.entry.value_raw)
        if req.pin_key and ent_pin and ent_pin == req.pin_key:
            result.status = CheckStatus.MATCH
            result.confidence = max(0.85, min(top.score, 0.99))
            result.notes = "配置以引脚名给出，与 Excel 管脚一致（记法不同，非差异）"
            return result

        equivalent = values_equivalent(
            req.expected_value, top.entry.value_raw, self.value_aliases
        )
        if equivalent:
            result.status = CheckStatus.MATCH
            result.confidence = min(max(top.score, 0.6), 0.99)
            result.notes = top.reason
        else:
            result.status = CheckStatus.MISMATCH
            result.confidence = min(max(top.score, 0.6), 0.95)
            result.notes = f"{top.reason}；期望 {req.expected_value}，实际 {top.entry.value_raw}"

        # 期望值是管脚名、而配置值是数字，或反之 —— 提示口径差异
        exp_num = norm_gpio_num(req.expected_value)
        cur_num = norm_gpio_num(top.entry.value_raw)
        if exp_num is not None and cur_num is not None and exp_num != cur_num:
            result.notes += "（GPIO 编号不一致）"
        elif req.pin_key and ent_pin and ent_pin != req.pin_key and (
            exp_num is not None or cur_num is not None
        ):
            result.notes += (
                f"（期望 {req.expected_value} 与配置 {top.entry.value_raw} 记法不同且引脚不一致）"
            )
        return result

    def downgrade(self, result: MatchResult) -> MatchResult:
        """低置信度降级为歧义，不自动生成修改。"""
        if (
            result.status in {CheckStatus.MATCH, CheckStatus.MISMATCH}
            and result.confidence < self.confidence_threshold
        ):
            result.status = CheckStatus.AMBIGUOUS
            result.notes = (result.notes + "；置信度低于阈值，已降级为歧义").strip("；")
        return result
