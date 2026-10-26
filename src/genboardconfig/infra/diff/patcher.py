"""差异生成、备份与回滚。"""

from __future__ import annotations

import difflib
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class DiffResult:
    unified: str = ""
    added: int = 0
    removed: int = 0
    hunks: int = 0

    @property
    def empty(self) -> bool:
        return not self.unified.strip()


def unified_diff(old_text: str, new_text: str, path: str = "board.c") -> DiffResult:
    old_lines = old_text.replace("\r\n", "\n").split("\n")
    new_lines = new_text.replace("\r\n", "\n").split("\n")
    diff_lines = list(
        difflib.unified_diff(
            old_lines, new_lines, fromfile=f"a/{path}", tofile=f"b/{path}", lineterm=""
        )
    )
    added = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
    hunks = sum(1 for line in diff_lines if line.startswith("@@"))
    return DiffResult(unified="\n".join(diff_lines), added=added, removed=removed, hunks=hunks)


def backup_file(path: str | Path, workdir: str | Path) -> Path:
    """把原文件复制到工作区备份目录，返回备份路径。"""
    path = Path(path)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_dir = Path(workdir) / "backup"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{stamp}_{path.name}.bak"
    shutil.copy2(path, target)
    return target


def restore_file(backup: str | Path, target: str | Path) -> None:
    shutil.copy2(backup, target)
