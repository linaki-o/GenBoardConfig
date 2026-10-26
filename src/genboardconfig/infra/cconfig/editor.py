"""按落点（行/列区间）改写 .c 文本，保持原编码与换行风格。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextEdit:
    line: int          # 1-based
    col: int           # 0-based
    length: int        # 旧值长度
    new_value: str

    def describe(self) -> str:
        return f"L{self.line}:C{self.col}({self.length}) → {self.new_value!r}"


def apply_edits(text: str, edits: list[TextEdit]) -> str:
    """从后往前应用编辑，避免行号漂移。"""
    if not edits:
        return text
    lines = text.replace("\r\n", "\n").split("\n")
    ordered = sorted(edits, key=lambda e: (e.line, e.col), reverse=True)
    for edit in ordered:
        if not (1 <= edit.line <= len(lines)):
            raise ValueError(f"行号越界: {edit.describe()}")
        line = lines[edit.line - 1]
        end = edit.col + edit.length
        if edit.col < 0 or end > len(line):
            raise ValueError(f"列区间越界: {edit.describe()} 行内容={line!r}")
        lines[edit.line - 1] = line[: edit.col] + edit.new_value + line[end:]
    return "\n".join(lines)


def write_text(path: str | Path, text: str, encoding: str = "utf-8", newline: str = "\n") -> None:
    path = Path(path)
    data = text.replace("\n", newline) if newline != "\n" else text
    path.write_bytes(data.encode(encoding, errors="replace"))
