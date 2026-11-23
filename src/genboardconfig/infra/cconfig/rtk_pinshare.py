"""Realtek PINSHARE 解析：引脚复用区块（Function / pad / 选中的复用功能）。

产出的每个条目对应一行 ``#define <MACRO>  (<MACRO>_<FUNC>)``，
value 的落点精确到**后缀**（如 ``GPO_OD``），因此写回时只替换该后缀。

宏名兼容 Realtek 的两种命名，故此处用通用标识符匹配，不写死 ``_PIN_`` 前缀：

* ``_PIN_C1``                —— 旧款，按端口字母 + 位号
* ``_LQFP216_..._PIN_201``   —— 新款，按封装 + 引脚编号
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ...domain.models import ConfigEntry, EntryKind
from .parser import CParseResult, file_hash

RE_FUNCTION = re.compile(r"^//\s*Function\s*:\s*(.+?)\s*$")
RE_DEFINE = re.compile(
    r"^#define\s+([A-Za-z_][A-Za-z0-9_]*)\s+\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)"
)
RE_ENUM = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"
    r"(0x[0-9A-Fa-f]+|[A-Za-z_][A-Za-z0-9_]*)\s*,"
)
RE_IF_PAREN = re.compile(r"^\s*#\s*if\s*\((.*)\)\s*$")
RE_IF_NAMED = re.compile(r"^\s*#\s*ifn?def\s+([A-Za-z_][A-Za-z0-9_]*)\s*$")
RE_ELIF = re.compile(r"^\s*#\s*elif\s*\((.*)\)\s*$")
RE_ELSE = re.compile(r"^\s*#\s*else\b")
RE_ENDIF = re.compile(r"^\s*#\s*endif\b")


def pad_of(macro: str) -> str:
    """从宏名提取引脚标识：``_PIN_C1`` → ``C1``；``_LQFP216_..._PIN_201`` → ``201``。"""
    idx = macro.rfind("_PIN_")
    return macro[idx + len("_PIN_"):] if idx >= 0 else macro


@dataclass
class PinshareDefine:
    """一条 ``#define`` 候选（同一 pad 可能有多个条件编译分支）。"""

    macro: str = ""
    symbol: str = ""
    suffix: str = ""
    line: int = 0
    col: int = 0
    value_col: int = 0
    value_len: int = 0
    raw_text: str = ""
    condition: str = ""


@dataclass
class PinshareBlock:
    """一个引脚复用区块。"""

    function: str = ""
    pad: str = ""
    macro_name: str = ""
    selected: str = ""            # 选中功能的**后缀**，如 GPO_OD
    selected_symbol: str = ""     # 完整符号，如 _PIN_C1_GPO_OD
    members: list[str] = field(default_factory=list)   # 该 pad 可选功能的后缀
    line: int = 0
    define_line: int = 0
    define_col: int = 0
    value_col: int = 0
    value_len: int = 0
    raw_text: str = ""
    condition: str = ""           # 所选分支的条件编译上下文
    defines: list[PinshareDefine] = field(default_factory=list)
    members_by_macro: dict[str, list[str]] = field(default_factory=dict)

    @property
    def macro(self) -> str:
        return self.macro_name

    def add_define(self, item: PinshareDefine) -> None:
        self.defines.append(item)

    def add_member(self, macro: str, suffix: str) -> None:
        self.members_by_macro.setdefault(macro, []).append(suffix)

    def pick(self) -> None:
        """选定代表定义：优先无条件编译分支，否则取第一个候选。"""
        if not self.defines:
            return
        chosen = next((d for d in self.defines if not d.condition), self.defines[0])
        self.macro_name = chosen.macro
        self.pad = pad_of(chosen.macro)
        self.selected = chosen.suffix
        self.selected_symbol = chosen.symbol
        self.define_line = chosen.line
        self.define_col = chosen.col
        self.value_col = chosen.value_col
        self.value_len = chosen.value_len
        self.raw_text = chosen.raw_text
        self.condition = chosen.condition
        self.members = list(self.members_by_macro.get(chosen.macro, []))


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
        warnings: list[str] = []
        if not blocks:
            warnings.append("未解析到任何引脚复用区块")
        elif not any(b.selected for b in blocks):
            warnings.append(
                f"识别到 {len(blocks)} 个引脚复用区块，但未能从 #define 中解析出选中的复用功能"
            )
        return CParseResult(
            entries=self.to_entries(blocks),
            text=text,
            encoding=encoding,
            newline=newline,
            lines=text.replace("\r\n", "\n").split("\n"),
            file_hash=file_hash(text),
            warnings=warnings,
        )

    def parse_blocks(self, text: str) -> list[PinshareBlock]:
        lines = text.replace("\r\n", "\n").split("\n")
        blocks: list[PinshareBlock] = []
        current: PinshareBlock | None = None
        conditions: list[str] = []

        for line_no, line in enumerate(lines, start=1):
            m = RE_FUNCTION.match(line)
            if m:
                current = PinshareBlock(function=m.group(1).strip(), line=line_no)
                blocks.append(current)
                continue

            # —— 条件编译 ——
            m = RE_IF_PAREN.match(line)
            if m:
                conditions.append(f"#if {m.group(1).strip()}")
                continue
            m = RE_IF_NAMED.match(line)
            if m:
                if not self._is_include_guard(m.group(1), lines, line_no):
                    conditions.append(f"#if {m.group(1)}")
                continue
            m = RE_ELIF.match(line)
            if m:
                if conditions:
                    conditions[-1] = f"#elif {m.group(1).strip()}"
                continue
            if RE_ELSE.match(line):
                if conditions:
                    conditions[-1] = f"{conditions[-1]} (else)"
                continue
            if RE_ENDIF.match(line):
                if conditions:
                    conditions.pop()
                continue

            if current is None:
                continue

            m = RE_DEFINE.match(line)
            if m:
                macro, symbol = m.group(1), m.group(2)
                # 只有「宏名_功能名」形式的右值才是复用功能选择；
                # _PIN_E18_OFF_REGION (_PIN_E18_xxx) 这类不是本宏的选择，跳过。
                if not symbol.startswith(macro + "_"):
                    continue
                suffix = symbol[len(macro) + 1:]
                current.add_define(
                    PinshareDefine(
                        macro=macro,
                        symbol=symbol,
                        suffix=suffix,
                        line=line_no,
                        col=m.start(1),
                        value_col=m.start(2) + len(macro) + 1,
                        value_len=len(suffix),
                        raw_text=line,
                        condition=" && ".join(c for c in conditions if c),
                    )
                )
                continue

            m = RE_ENUM.match(line)
            if m:
                member = m.group(1)
                for item in current.defines:
                    if member.startswith(item.macro + "_"):
                        current.add_member(item.macro, member[len(item.macro) + 1:])
                        break

        for block in blocks:
            block.pick()
        return blocks

    @staticmethod
    def _is_include_guard(name: str, lines: list[str], idx: int) -> bool:
        """`#ifndef X` 后紧跟 `#define X` → 头文件包含保护，不算条件。"""
        if not name:
            return False
        for j in range(idx, min(idx + 3, len(lines))):
            nxt = lines[j].strip()
            if not nxt:
                continue
            return bool(re.match(rf"^#\s*define\s+{re.escape(name)}\b", nxt))
        return False

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
                    condition=block.condition,
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
