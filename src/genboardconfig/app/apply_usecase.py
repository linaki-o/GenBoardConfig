"""应用用例：生成变更预览并受控写回 .c 文件。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..domain.models import ChangeType, CheckStatus
from ..infra.cconfig.editor import TextEdit, apply_edits, write_text
from ..infra.diff.patcher import backup_file, restore_file, unified_diff
from ..infra.validate.semantic import SemanticReport, recheck
from ..infra.validate.structure import ValidationReport, check_structure
from .context import Session


@dataclass
class ApplyOutcome:
    applied: bool = False
    rolled_back: bool = False
    message: str = ""
    diff: str = ""
    added: int = 0
    removed: int = 0
    backup_path: str = ""
    target_path: str = ""
    new_text: str = ""
    edits: list[TextEdit] = field(default_factory=list)
    structure: ValidationReport | None = None
    semantic: SemanticReport | None = None
    skipped: list[str] = field(default_factory=list)


class ApplyUseCase:
    """只允许白名单编辑；写回后自动校验，失败回滚。"""

    APPLIABLE = {
        ChangeType.SET_MACRO,
        ChangeType.SET_STRUCT_FIELD,
        ChangeType.SET_ARRAY_ITEM,
        ChangeType.SET_PORT_BIT,
    }

    def build_edits(self, session: Session, selected_ids: set[str]) -> tuple[list[TextEdit], list[str]]:
        entries_by_id = session.entries_by_id()
        edits: list[TextEdit] = []
        skipped: list[str] = []
        seen_lines: set[tuple[int, int]] = set()
        for res in session.check_result.results:
            if res.requirement_id not in selected_ids:
                continue
            changes = [c for c in self._collect_changes(res) if c is not None]
            if not changes:
                skipped.append(
                    f"{res.requirement_id}: {res.proposed_change.reason or '无可自动应用的修改'}"
                )
                continue
            for change in changes:
                if change.type not in self.APPLIABLE or not change.target:
                    skipped.append(
                        f"{res.requirement_id}: {change.reason or change.type.value}（需人工处理）"
                    )
                    continue
                entry = entries_by_id.get(change.target)
                if entry is None:
                    skipped.append(f"{res.requirement_id}: 目标配置项不存在")
                    continue
                if entry.value_raw != change.old_value:
                    skipped.append(
                        f"{res.requirement_id}: 原值已变化（{entry.value_raw} ≠ {change.old_value}），跳过"
                    )
                    continue
                key = (entry.line, entry.value_col)
                if key in seen_lines:
                    skipped.append(f"{res.requirement_id}: 与其它变更落点冲突，跳过")
                    continue
                seen_lines.add(key)
                edits.append(
                    TextEdit(
                        line=entry.line,
                        col=entry.value_col,
                        length=entry.value_len,
                        new_value=change.new_value,
                    )
                )
        return edits, skipped

    @staticmethod
    def _collect_changes(res):
        """行级修改 + 属性级修改（档案模式）。"""
        changes = []
        if res.proposed_change is not None and res.proposed_change.type.value != "none":
            changes.append(res.proposed_change)
        for attr in res.attribute_results:
            if attr.change is not None and attr.change.type.value != "none":
                changes.append(attr.change)
        return changes

    def preview(self, session: Session, selected_ids: set[str]) -> ApplyOutcome:
        if session.c_parse is None:
            return ApplyOutcome(message="尚未解析 C 文件")
        edits, skipped = self.build_edits(session, selected_ids)
        if not edits:
            return ApplyOutcome(message="没有可自动应用的修改", skipped=skipped)
        try:
            new_text = apply_edits(session.c_parse.text, edits)
        except ValueError as exc:
            return ApplyOutcome(message=f"生成预览失败：{exc}", skipped=skipped)
        diff = unified_diff(session.c_parse.text, new_text, Path(session.c_path).name)
        return ApplyOutcome(
            message="预览已生成",
            diff=diff.unified,
            added=diff.added,
            removed=diff.removed,
            new_text=new_text,
            edits=edits,
            skipped=skipped,
            target_path=session.c_path,
        )

    def apply(
        self,
        session: Session,
        selected_ids: set[str],
        overwrite: bool = True,
        run_semantic: bool = True,
    ) -> ApplyOutcome:
        if session.c_parse is None:
            return ApplyOutcome(message="尚未解析 C 文件")
        outcome = self.preview(session, selected_ids)
        if not outcome.new_text:
            return outcome

        target = Path(session.c_path)
        backup = backup_file(target, session.workdir)
        outcome.backup_path = str(backup)

        if not overwrite:
            export = target.with_name(target.stem + ".genboard.c")
            write_text(export, outcome.new_text, session.c_parse.encoding, session.c_parse.newline)
            outcome.applied = True
            outcome.target_path = str(export)
            outcome.message = f"已导出修改结果：{export}"
            return outcome

        write_text(target, outcome.new_text, session.c_parse.encoding, session.c_parse.newline)

        structure = check_structure(outcome.new_text)
        outcome.structure = structure
        if not structure.ok:
            restore_file(backup, target)
            outcome.rolled_back = True
            outcome.applied = False
            outcome.message = "结构校验失败，已回滚：" + "；".join(structure.messages)
            return outcome

        if run_semantic:
            semantic = recheck(
                outcome.new_text,
                session.check_result,
                parser=session.parser,
                encoding=session.c_parse.encoding,
                newline=session.c_parse.newline,
                profile=session.profile,
                overrides=session.check_result.extra.get("symbol_overrides") or {},
            )
            outcome.semantic = semantic
            if semantic.level == "fail":
                restore_file(backup, target)
                outcome.rolled_back = True
                outcome.applied = False
                outcome.message = "语义复检失败，已回滚：" + "；".join(semantic.messages)
                return outcome
            if semantic.level == "warn":
                outcome.message = "已应用，但复检提示：" + "；".join(semantic.messages)
            else:
                outcome.message = "已应用并通过结构与语义复检"
        else:
            outcome.message = "已应用（未执行语义复检）"

        outcome.applied = True
        return outcome

    @staticmethod
    def restorable(result_status: str) -> bool:
        return result_status == CheckStatus.MISMATCH.value
