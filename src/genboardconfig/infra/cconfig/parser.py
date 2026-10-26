"""板级 .c 配置文件解析：抽取配置项并保留精确落点（行/列）。"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from ...domain.models import ConfigEntry, EntryKind
from ...domain.normalize import clean_text, norm_key, norm_value
from ...domain.hsi import parse_trailing_chip_pin

RE_DEFINE = re.compile(
    r"^\s*#\s*define\s+(?P<name>[A-Za-z_]\w*)"
    r"(?P<args>\((?:[^()]*)\))?"
    r"(?P<rest>.*)$"
)
RE_BITS_CALL = re.compile(r"\bBitsToByte\s*\(")
RE_PORT_TABLE = re.compile(
    r"^PORT_(?P<port>[A-Z])_DEFAULT_(?P<attr>[A-Z]+)$"
)
RE_STRUCT_INIT = re.compile(
    r"^\s*(?:static\s+|const\s+|volatile\s+)*struct\s+(?P<type>\w+)\s+"
    r"(?P<var>\w+)\s*(?P<arr>\[[^\]]*\])?\s*=\s*\{"
)
RE_ARRAY_INIT = re.compile(
    r"^\s*(?:static\s+|const\s+|volatile\s+)*"
    r"(?:(?:struct\s+\w+|unsigned\s+int|int|char|bool|uint\d+_t)\s+)+"
    r"(?P<var>\w+)\s*\[[^\]]*\]\s*=\s*\{"
)
RE_FIELD = re.compile(r"\.\s*(?P<field>[A-Za-z_]\w*)\s*=\s*(?P<value>[^,}\n]*)")
RE_CALL = re.compile(r"(?P<fn>[A-Za-z_]\w*)\s*\((?P<args>[^;()]*)\)")
RE_STRING = re.compile(r"\"([^\"]*)\"")
RE_TOKEN = re.compile(r"[A-Za-z_]\w*|0[xX][0-9A-Fa-f]+|\d+")

# 明确的非配置上下文（注释/包含）
RE_COMMENT_LINE = re.compile(r"^\s*(//|/\*|\*)")
RE_IF = re.compile(r"^\s*#\s*(if|ifdef|ifndef)\b(.*)$")
RE_ELIF = re.compile(r"^\s*#\s*elif\b(.*)$")
RE_ELSE = re.compile(r"^\s*#\s*else\b(.*)$")
RE_ENDIF = re.compile(r"^\s*#\s*endif\b")
RE_UNDEF = re.compile(r"^\s*#\s*undef\s+(\w+)")


@dataclass
class Scope:
    kind: str          # struct | array
    type: str
    var: str
    depth: int


@dataclass
class CParseResult:
    entries: list[ConfigEntry] = field(default_factory=list)
    text: str = ""
    encoding: str = "utf-8"
    newline: str = "\n"
    lines: list[str] = field(default_factory=list)
    file_hash: str = ""
    warnings: list[str] = field(default_factory=list)


def detect_encoding(raw: bytes) -> str:
    for enc in ("utf-8-sig", "utf-8", "gb18030", "big5", "latin-1"):
        try:
            raw.decode(enc)
            return enc
        except UnicodeDecodeError:
            continue
    return "latin-1"


def file_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


class CConfigParser:
    """轻量词法 + 规则解析，抽取宏定义、结构体字段、数组元素、函数调用参数。

    额外支持档案模式（HSI 等）：
    - 宏行尾注释（`#define DIG1_HPD_PORT STBC_PORT_B//DP_HPD`）→ 原理图网络名
    - 宏组分类（`_PORT` / `_BIT` / `_ACTIVE`）
    - 端口位表（`PORT_C_DEFAULT_OUT BitsToByte(...)`）→ 每个位一个可精确改写的条目
    """

    def __init__(
        self,
        group_cfg: dict | None = None,
        port_table_cfg: dict | None = None,
    ):
        self.group_cfg = group_cfg or {}
        self.port_table_cfg = port_table_cfg or {}
        self._port_suffixes = tuple(self.group_cfg.get("port_suffixes") or ["_PORT"])
        self._bit_suffixes = tuple(
            self.group_cfg.get("bit_suffixes") or ["_BIT", "_PIN", "_OUTPUT_PIN"]
        )
        self._active_suffixes = tuple(
            self.group_cfg.get("active_suffixes") or ["_ACTIVE", "_POL"]
        )
        self._port_prefix = (self.group_cfg.get("port_value") or {}).get(
            "prefix", "STBC_PORT_"
        )
        self._port_null = (self.group_cfg.get("port_value") or {}).get(
            "null", "STBC_PORT_NULL"
        )
        self._bit_prefix = (self.group_cfg.get("bit_value") or {}).get("prefix", "BIT")
        self._pin_pattern = (self.group_cfg.get("pin_value") or {}).get("pattern", "")

    def parse(self, path: str | Path) -> CParseResult:
        path = Path(path)
        raw = path.read_bytes()
        encoding = detect_encoding(raw)
        text = raw.decode(encoding, errors="replace")
        newline = "\r\n" if "\r\n" in text else "\n"
        return self.parse_text(text, encoding=encoding, newline=newline)

    def parse_text(
        self, text: str, encoding: str = "utf-8", newline: str = "\n"
    ) -> CParseResult:
        lines = text.replace("\r\n", "\n").split("\n")

        result = CParseResult(
            text=text, encoding=encoding, newline=newline, lines=lines,
            file_hash=file_hash(text),
        )
        scopes: list[Scope] = []
        depth = 0
        counter = 0
        conditions: list[str] = []
        undefs: set[str] = set()

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or RE_COMMENT_LINE.match(line):
                if "{" in line and "}" in line:
                    depth += line.count("{") - line.count("}")
                continue

            # —— 条件编译 ——
            m_if = RE_IF.match(line)
            if m_if:
                directive = m_if.group(1)
                body = m_if.group(2).strip()
                if directive == "ifndef" and self._is_include_guard(
                    body, lines, idx
                ):
                    continue  # 头文件包含保护，不算条件
                conditions.append(f"#if {body}")
                continue
            if RE_ELIF.match(line):
                if conditions:
                    conditions[-1] = f"#elif {RE_ELIF.match(line).group(1).strip()}"
                continue
            if RE_ELSE.match(line):
                if conditions:
                    conditions[-1] = f"{conditions[-1]} (else)"
                continue
            if RE_ENDIF.match(line):
                if conditions:
                    conditions.pop()
                continue
            m_undef = RE_UNDEF.match(line)
            if m_undef:
                undefs.add(m_undef.group(1))
                continue
            condition = " && ".join(c for c in conditions if c)

            struct_m = RE_STRUCT_INIT.match(line)
            array_m = RE_ARRAY_INIT.match(line)
            if struct_m:
                is_array = bool(struct_m.group("arr"))
                scopes.append(
                    Scope(
                        "array" if is_array else "struct",
                        struct_m.group("type"),
                        struct_m.group("var"),
                        depth + 1,
                    )
                )
            elif array_m:
                scopes.append(
                    Scope("array", "", array_m.group("var"), depth + 1)
                )

            owner = self._owner_label(scopes)
            context = self._context_of(lines, idx, scopes)

            if RE_DEFINE.match(line):
                for entry in self._parse_define(lines, idx, counter, context, condition):
                    result.entries.append(entry)
                    counter += 1
            elif struct_m or array_m:
                entry = self._parse_initializer_item(
                    lines, idx, counter, owner, context, scopes
                )
                if entry:
                    counter += 1
                    result.entries.append(entry)
            elif scopes and scopes[-1].kind == "array" and "{" in line and "}" in line:
                entry = self._parse_initializer_item(
                    lines, idx, counter, owner, context, scopes
                )
                if entry:
                    counter += 1
                    result.entries.append(entry)
            else:
                for entry in self._parse_fields_and_calls(
                    lines, idx, counter, owner, context, scopes
                ):
                    counter += 1
                    result.entries.append(entry)

            depth += line.count("{") - line.count("}")
            while scopes and depth < scopes[-1].depth:
                scopes.pop()

        if not result.entries:
            result.warnings.append("未在文件中解析到任何配置项，请确认文件格式是否受支持")
        return result

    # ---------- 内部解析 ----------

    @staticmethod
    def _owner_label(scopes: list[Scope]) -> str:
        if not scopes:
            return ""
        scope = scopes[-1]
        if scope.kind == "struct":
            return f"struct {scope.type} {scope.var}"
        return f"{scope.var}[]"

    @staticmethod
    def _context_of(lines: list[str], idx: int, scopes: list[Scope]) -> str:
        for offset in range(1, 4):
            j = idx - 1 - offset
            if j < 0:
                break
            candidate = lines[j].strip()
            if candidate and not candidate.startswith(("#", "//", "*", "/*")):
                return candidate[:160]
        return ""

    def _parse_define(
        self,
        lines: list[str],
        idx: int,
        counter: int,
        context: str,
        condition: str = "",
    ) -> list[ConfigEntry]:
        line = lines[idx - 1]
        m = RE_DEFINE.match(line)
        if not m:
            return []
        name = m.group("name")
        args = m.group("args")
        rest = m.group("rest")
        rest_start = m.start("rest")
        value_raw, value_col, value_len = self._extract_value(line, rest_start)
        if not value_raw:
            return []
        kind = EntryKind.MACRO_FUNC if args else EntryKind.MACRO
        group, role = self._classify_macro(name)
        comment = self._trailing_comment(line, value_col + value_len)
        port, bit = self._extract_pin_info(role, value_raw)

        entries = [
            ConfigEntry(
                id=f"E{counter:04d}",
                kind=kind,
                key=name,
                key_norm=norm_key(name),
                value_raw=value_raw,
                value_normalized=norm_value(value_raw),
                value_kind=self._value_kind(value_raw),
                owner=context,
                file="",
                line=idx,
                col=0,
                value_col=value_col,
                value_len=value_len,
                raw_text=line,
                context=context,
                comment=comment,
                condition=condition,
                group=group,
                role=role,
                port=port,
                bit=bit,
            )
        ]
        entries.extend(self._parse_port_table(line, idx, counter + 1, name))
        return entries

    # ---------- 档案模式辅助 ----------

    @staticmethod
    def _is_include_guard(name: str, lines: list[str], idx: int) -> bool:
        """`#ifndef X` 后紧跟 `#define X` → 头文件包含保护。"""
        if not name:
            return False
        for j in range(idx, min(idx + 3, len(lines))):
            nxt = lines[j].strip()
            if not nxt:
                continue
            return bool(re.match(rf"^#\s*define\s+{re.escape(name)}\b", nxt))
        return False

    def _classify_macro(self, name: str) -> tuple[str, str]:
        for suffix in self._port_suffixes:
            if name.endswith(suffix) and len(name) > len(suffix):
                return name[: -len(suffix)], "port"
        for suffix in sorted(self._bit_suffixes, key=len, reverse=True):
            if name.endswith(suffix) and len(name) > len(suffix):
                return name[: -len(suffix)], "bit"
        for suffix in sorted(self._active_suffixes, key=len, reverse=True):
            if name.endswith(suffix) and len(name) > len(suffix):
                return name[: -len(suffix)], "active"
        return "", ""

    @staticmethod
    def _trailing_comment(line: str, value_end: int) -> str:
        tail = line[value_end:]
        idx = tail.find("//")
        if idx < 0:
            return ""
        return tail[idx + 2 :].strip()

    def _extract_pin_info(self, role: str, value: str) -> tuple[str, int | None]:
        """从宏值中解析端口字母与位号。"""
        if role == "port":
            if value.startswith(self._port_prefix):
                letter = value[len(self._port_prefix) :]
                if letter.isalpha() and letter.upper() != "NULL":
                    return letter.upper(), None
            return "", None
        if role == "bit":
            if value.startswith(self._bit_prefix) and value[len(self._bit_prefix) :].isdigit():
                return "", int(value[len(self._bit_prefix) :])
            spec = parse_trailing_chip_pin(value)
            if spec:
                return spec[0], spec[1]
            return "", None
        return "", None
        if role == "bit":
            if value.startswith(self._bit_prefix) and value[len(self._bit_prefix) :].isdigit():
                return "", int(value[len(self._bit_prefix) :])
            m = re.search(r"PIN_([A-Z]{1,2})([0-9]+)$", value)
            if m:
                return m.group(1).upper(), int(m.group(2))
            return "", None
        return "", None

    def _parse_port_table(
        self, line: str, idx: int, counter: int, macro_name: str
    ) -> list[ConfigEntry]:
        """把 `PORT_C_DEFAULT_OUT BitsToByte(HIGH, HIGH, ...)` 拆成逐位条目。"""
        m = RE_PORT_TABLE.match(macro_name)
        if not m:
            return []
        call = RE_BITS_CALL.search(line)
        if not call:
            return []
        open_paren = call.end() - 1
        close_paren = line.rfind(")")
        if close_paren <= open_paren:
            return []
        inner = line[open_paren + 1 : close_paren]
        args: list[tuple[str, int]] = []
        depth = 0
        start = 0
        for i, ch in enumerate(inner):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                args.append((inner[start:i].strip(), start))
                start = i + 1
        tail = inner[start:].strip()
        if tail:
            args.append((tail, start))

        entries: list[ConfigEntry] = []
        count = len(args)
        for i, (text, offset) in enumerate(args):
            if not text:
                continue
            bit = count - 1 - i  # BitsToByte 参数自 bit7 到 bit0
            lead = len(inner[offset:]) - len(inner[offset:].lstrip())
            col = open_paren + 1 + offset + lead
            entries.append(
                ConfigEntry(
                    id=f"E{counter + i:04d}",
                    kind=EntryKind.PORT_BIT,
                    key=f"{macro_name}[{bit}]",
                    key_norm=norm_key(f"{macro_name}_{bit}"),
                    value_raw=text,
                    value_normalized=norm_value(text),
                    value_kind=self._value_kind(text),
                    owner=macro_name,
                    file="",
                    line=idx,
                    col=0,
                    value_col=col,
                    value_len=len(text),
                    raw_text=line,
                    context="",
                    group=macro_name,
                    role="port_bit",
                    port=m.group("port"),
                    bit=bit,
                    table=macro_name,
                )
            )
        return entries

    def _parse_initializer_item(
        self,
        lines: list[str],
        idx: int,
        counter: int,
        owner: str,
        context: str,
        scopes: list[Scope],
    ) -> ConfigEntry | None:
        line = lines[idx - 1]
        inner = self._brace_inner(line)
        if inner is None:
            return None
        inner_text, inner_offset = inner
        tokens = self._tokens(inner_text)
        if not tokens:
            return None
        name_tok, value_tok = None, None
        if len(tokens) >= 2:
            name_tok, value_tok = tokens[0], tokens[1]
        elif len(tokens) == 1:
            name_tok, value_tok = tokens[0], None
        key = name_tok[0] if name_tok else ""
        if len(key) >= 2 and key[0] == '"' and key[-1] == '"':
            key = key[1:-1]
        value = value_tok[0] if value_tok else ""
        if not value:
            return None
        value_col = inner_offset + (value_tok[1] if value_tok else 0)
        return ConfigEntry(
            id=f"E{counter:04d}",
            kind=EntryKind.ARRAY_ITEM,
            key=key,
            key_norm=norm_key(key),
            value_raw=value,
            value_normalized=norm_value(value),
            value_kind=self._value_kind(value),
            owner=owner,
            file="",
            line=idx,
            col=0,
            value_col=value_col,
            value_len=len(value),
            raw_text=line,
            context=context,
        )

    def _parse_fields_and_calls(
        self,
        lines: list[str],
        idx: int,
        counter: int,
        owner: str,
        context: str,
        scopes: list[Scope],
    ) -> list[ConfigEntry]:
        line = lines[idx - 1]
        out: list[ConfigEntry] = []
        for m in RE_FIELD.finditer(line):
            value = clean_text(m.group("value"))
            if not value:
                continue
            value_start = m.start("value")
            value_token = self._first_token(value)
            if not value_token:
                continue
            tok, tok_off = value_token
            out.append(
                ConfigEntry(
                    id=f"E{counter + len(out):04d}",
                    kind=EntryKind.STRUCT_FIELD,
                    key=m.group("field"),
                    key_norm=norm_key(m.group("field")),
                    value_raw=tok,
                    value_normalized=norm_value(tok),
                    value_kind=self._value_kind(tok),
                    owner=owner,
                    file="",
                    line=idx,
                    col=0,
                    value_col=value_start + tok_off,
                    value_len=len(tok),
                    raw_text=line,
                    context=context,
                )
            )
        if not out:
            for m in RE_CALL.finditer(line):
                args = m.group("args").strip()
                if not args:
                    continue
                first = self._first_token(args)
                if not first:
                    continue
                tok, tok_off = first
                out.append(
                    ConfigEntry(
                        id=f"E{counter + len(out):04d}",
                        kind=EntryKind.CALL_ARG,
                        key=m.group("fn"),
                        key_norm=norm_key(m.group("fn")),
                        value_raw=tok,
                        value_normalized=norm_value(tok),
                        value_kind=self._value_kind(tok),
                        owner=owner,
                        file="",
                        line=idx,
                        col=0,
                        value_col=m.start("args") + tok_off,
                        value_len=len(tok),
                        raw_text=line,
                        context=context,
                    )
                )
        return out

    # ---------- 工具 ----------

    @staticmethod
    def _brace_inner(line: str) -> tuple[str, int] | None:
        start = line.find("{")
        end = line.rfind("}")
        if start < 0 or end <= start:
            return None
        return line[start + 1 : end], start + 1

    @staticmethod
    def _tokens(text: str) -> list[tuple[str, int]]:
        out: list[tuple[str, int]] = []
        for m in RE_STRING.finditer(text):
            out.append((m.group(0), m.start()))
        stripped = RE_STRING.sub(lambda m: " " * len(m.group(0)), text)
        for m in RE_TOKEN.finditer(stripped):
            out.append((m.group(0), m.start()))
        out.sort(key=lambda t: t[1])
        return out

    @staticmethod
    def _first_token(text: str) -> tuple[str, int] | None:
        tokens = CConfigParser._tokens(text)
        return tokens[0] if tokens else None

    @staticmethod
    def _extract_value(line: str, start: int) -> tuple[str, int, int]:
        """从 start 处截取一个值 token，返回 (值, 起始列, 长度)。"""
        tail = line[start:]
        if not tail.strip():
            return "", 0, 0
        m = RE_TOKEN.search(tail) or RE_STRING.search(tail)
        if not m:
            return "", 0, 0
        token = m.group(0)
        col = start + m.start()
        return token, col, len(token)

    @staticmethod
    def _value_kind(value: str) -> str:
        if not value:
            return "none"
        if re.fullmatch(r"0[xX][0-9A-Fa-f]+|\d+", value):
            return "literal"
        if re.fullmatch(r"[A-Za-z_]\w*", value):
            return "symbolic"
        return "expression"
