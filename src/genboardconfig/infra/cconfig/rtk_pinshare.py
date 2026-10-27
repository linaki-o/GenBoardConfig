"""Realtek PINSHARE 解析：引脚复用区块（Function / pad / 选中的复用功能）。

产出的每个条目对应一行 ``#define _PIN_<PAD>  (_PIN_<PAD>_<FUNC>)``，
value 的落点精确到**后缀**（如 ``GPO_OD``），因此写回时只替换该后缀。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ...domain.models import ConfigEntry, EntryKind
from .parser import CParseResult, file_hash

RE_FUNCTION = re.compile(r"^//\s*Function\s*:\s*(.+?)\s*$")
RE_DEFINE = re.compile(
    r"^#define\s+(_PIN_[A-Z]+\d+)\s+\(\s*(_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*\)"
)
RE_ENUM = re.compile(
    r"^\s*(_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*=\s*"
    r"(0x[0-9A-Fa-f]+|_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*,"
)


@dataclass
class PinshareBlock:
    """一个引脚复用区块。"""

    function: str = ""
    pad: str = ""
    selected: str = ""            # 选中功能的**后缀**，如 GPO_OD
    selected_symbol: str = ""     # 完整符号，如 _PIN_C1_GPO_OD
    members: list[str] = field(default_factory=list)
    line: int = 0
    define_line: int = 0
    define_col: int = 0
    value_col: int = 0
    value_len: int = 0
    raw_text: str = ""

    @property
    def macro(self) -> str:
        return f"_PIN_{self.pad}" if self.pad else ""


class RtkPinshareParser:
    """把 PINSHARE 头文件解析成引脚复用区块。"""

    def parse(self, path: str | Path) -> "CParseResult":
        path = Path(path)
        raw = path.read_bytes()
        encoding = "utf-8"
        text = ""
        for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
            try:
                text = raw.decode(enc)
                encoding = enc
                break
            except UnicodeDecodeError:
                continue
        else:  # pragma: no cover
            text = raw.decode("latin-1", errors="replace")
        result = self.parse_text(text)
        result.file = str(path)
        result.encoding = encoding
        return result

    def parse_text(self, text: str, encoding: str = "utf-8", newline: str = "") -> "CParseResult":
        blocks = self.parse_blocks(text)
        newline = newline or ("\r\n" if "\r\n" in text else "\n")
        return CParseResult(
            entries=self.to_entries(blocks),
            text=text,
            encoding=encoding,
            newline=newline,
            lines=text.replace("\r\n", "\n").split("\n"),
            file_hash=file_hash(text),
            warnings=[] if blocks else ["未解析到任何引脚复用区块"],
        )

    def parse_blocks(self, text: str) -> list[PinshareBlock]:
        lines = text.replace("\r\n", "\n").split("\n")
        blocks: list[PinshareBlock] = []
        current: PinshareBlock | None = None

        for line_no, line in enumerate(lines, start=1):
            m = RE_FUNCTION.match(line)
            if m:
                current = PinshareBlock(function=m.group(1).strip(), line=line_no)
                blocks.append(current)
                continue
            if current is None:
                continue
            m = RE_DEFINE.match(line)
            if m:
                macro, symbol = m.group(1), m.group(2)
                pad = macro[len("_PIN_"):]
                suffix = symbol[len(macro) + 1:]
                value_start = m.start(2) + len(macro) + 1
                current.pad = pad
                current.selected = suffix
                current.selected_symbol = symbol
                current.define_line = line_no
                current.define_col = m.start(1)
                current.value_col = value_start
                current.value_len = len(suffix)
                current.raw_text = line
                continue
            m = RE_ENUM.match(line)
            if m:
                current.members.append(m.group(1))
        return blocks

    def to_entries(self, blocks: list[PinshareBlock], file: str = "") -> list[ConfigEntry]:
        """转成统一条目，便于复用核对/写回/报告链路。"""
        entries: list[ConfigEntry] = []
        for i, block in enumerate(blocks):
            if not block.selected:
                continue
            entries.append(
                ConfigEntry(
                    id=f"R{i:04d}",
                    kind=EntryKind.RTK_BLOCK,
                    key=block.function or block.macro,
                    key_norm=norm_key(block.function),
                    value_raw=block.selected,
                    value_normalized=block.selected,
                    value_kind="symbolic",
                    owner=block.macro,
                    file=file,
                    line=block.define_line or block.line,
                    col=block.define_col,
                    value_col=block.value_col,
                    value_len=block.value_len,
                    raw_text=block.raw_text,
                    context=f"{block.macro} 复用功能：{block.selected}",
                    comment=block.function,
                    group=block.pad,
                    role="pinshare",
                    function=block.function,
                    members=list(block.members),
                )
            )
        return entries


def norm_key(text: str) -> str:
    import re as _re

    return _re.sub(r"[^A-Z0-9]+", "_", (text or "").upper()).strip("_")
