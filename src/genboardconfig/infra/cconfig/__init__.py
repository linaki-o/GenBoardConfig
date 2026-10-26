"""板级 C 配置解析与编辑。"""

from .editor import TextEdit, apply_edits, write_text
from .parser import CConfigParser, CParseResult, detect_encoding, file_hash

__all__ = [
    "CConfigParser",
    "CParseResult",
    "TextEdit",
    "apply_edits",
    "detect_encoding",
    "file_hash",
    "write_text",
]
