"""结构校验：括号/宏/数组/字符串的完整性。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    level: str = "pass"          # pass | warn | fail
    messages: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.level != "fail"


def check_structure(text: str) -> ValidationReport:
    messages: list[str] = []
    depth = 0
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    escape = False
    pairs = {"}": "{", ")": "("}
    stack: list[tuple[str, int]] = []

    for line_no, line in enumerate(text.replace("\r\n", "\n").split("\n"), start=1):
        in_line_comment = False
        for ch in line:
            if escape:
                escape = False
                continue
            if ch == "\\":
                if in_string or in_char:
                    escape = True
                continue
            if in_line_comment:
                continue
            if in_block_comment:
                if ch == "*" and line.endswith("*/"):
                    in_block_comment = False
                continue
            if in_string:
                if ch == '"':
                    in_string = False
                continue
            if in_char:
                if ch == "'":
                    in_char = False
                continue
            if ch == "/" and line.lstrip().startswith("//"):
                in_line_comment = True
                break
            if ch == '"':
                in_string = True
            elif ch == "'":
                in_char = True
            elif ch in "({":
                stack.append((ch, line_no))
            elif ch in ")}":
                if not stack:
                    messages.append(f"L{line_no}: 多余的 '{ch}'")
                    return ValidationReport("fail", messages)
                opener, opener_line = stack.pop()
                if opener != pairs[ch]:
                    messages.append(
                        f"L{line_no}: '{ch}' 与 L{opener_line} 的 '{opener}' 不匹配"
                    )
                    return ValidationReport("fail", messages)
        if in_string:
            messages.append(f"L{line_no}: 字符串字面量未闭合")
        if in_block_comment:
            messages.append(f"L{line_no}: 块注释未闭合")
        in_string = False
        in_char = False

    for opener, opener_line in stack:
        messages.append(f"L{opener_line}: '{opener}' 未闭合")
    if messages:
        return ValidationReport("fail", messages)

    # 宏定义完整性
    for line_no, line in enumerate(text.replace("\r\n", "\n").split("\n"), start=1):
        stripped = line.strip()
        if stripped.startswith("#define") and stripped.count("(") != stripped.count(")"):
            return ValidationReport("fail", [f"L{line_no}: 宏定义括号不配对"])
        if stripped.startswith("#define") and not re.search(r"#\s*define\s+\w+", stripped):
            return ValidationReport("fail", [f"L{line_no}: 宏定义缺少宏名"])
    return ValidationReport("pass", messages)

