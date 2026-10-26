"""变更规划：把差异结论转换为可安全执行的 ChangePlan。"""

from __future__ import annotations

from .models import (
    ChangeType,
    CheckStatus,
    ConfigEntry,
    MatchResult,
    ProposedChange,
)

KIND_TO_CHANGE = {
    "macro": ChangeType.SET_MACRO,
    "macro_func": ChangeType.SET_MACRO,
    "struct_field": ChangeType.SET_STRUCT_FIELD,
    "array_item": ChangeType.SET_ARRAY_ITEM,
    "call_arg": ChangeType.NONE,
    "unknown": ChangeType.NONE,
}


class Planner:
    """只为可精确定位落点的差异生成修改；其余给出手工建议。"""

    def plan(
        self, result: MatchResult, entries_by_id: dict[str, ConfigEntry]
    ) -> ProposedChange:
        change = result.proposed_change
        if result.status == CheckStatus.MISSING:
            change.type = ChangeType.INSERT_BLOCK
            change.target = ""
            change.reason = "配置项缺失，需要人工确定插入位置与写法"
            change.new_value = result.expected_value
            return change

        if result.status != CheckStatus.MISMATCH:
            change.type = ChangeType.NONE
            return change

        if not result.matched_entry_ids:
            change.type = ChangeType.NONE
            change.reason = "未定位到可修改的配置项"
            return change

        entry = entries_by_id.get(result.matched_entry_ids[0])
        if entry is None:
            change.type = ChangeType.NONE
            change.reason = "目标配置项已失效"
            return change

        ctype = KIND_TO_CHANGE.get(entry.kind.value, ChangeType.NONE)
        if ctype is ChangeType.NONE:
            change.type = ChangeType.NONE
            change.reason = f"暂不支持自动修改 {entry.kind.value} 类型，需人工处理"
            return change

        change.type = ctype
        change.target = entry.id
        change.old_value = entry.value_raw
        change.new_value = result.expected_value
        change.reason = (
            f"L{entry.line} {entry.key}：期望 {result.expected_value}，实际 {entry.value_raw}"
        )
        return change
