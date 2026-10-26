"""敏感信息脱敏：送往云端前屏蔽疑似密钥/口令。"""

from __future__ import annotations

import re

DEFAULT_PATTERNS = [
    (r"(?i)(api[_-]?key|secret|password|passwd|token|private[_-]?key)\s*[:=]\s*\"?[^\s\"',;]+", r"\1=***"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", "***PRIVATE KEY***"),
    (r"\b[A-Za-z0-9+/]{40,}={0,2}\b", "***BASE64***"),
]


class Masker:
    def __init__(self, patterns: list[str] | None = None, enabled: bool = True):
        self.enabled = enabled
        compiled = []
        for pattern in patterns or [p for p, _ in DEFAULT_PATTERNS]:
            try:
                compiled.append(re.compile(pattern))
            except re.error:
                continue
        for pattern, replacement in DEFAULT_PATTERNS:
            try:
                compiled.append((re.compile(pattern), replacement))  # type: ignore[arg-type]
            except re.error:
                continue
        self._rules = compiled

    def mask(self, text: str) -> str:
        if not self.enabled or not text:
            return text
        out = text
        for rule in self._rules:
            if isinstance(rule, tuple):
                pattern, replacement = rule
                out = pattern.sub(replacement, out)
            else:
                out = rule.sub("***", out)
        return out
