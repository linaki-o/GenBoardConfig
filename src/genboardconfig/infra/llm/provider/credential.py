"""凭据清洗与脱敏：避免非法请求头、避免密钥泄漏到日志与报告。

HTTP 头值不允许出现 CR/LF（httpx 会抛 ``LocalProtocolError: Illegal header
value``）。用户从网页/文档复制 API Key 时常带尾部换行，因此凡是要放进请求头
的凭据都必须先经过 :func:`clean_credential`。
"""

from __future__ import annotations

import re

REDACTED = "***"


def clean_credential(value: str | None) -> str:
    """去掉首尾空白与 CR/LF，得到可直接放进请求头的凭据。"""
    if not value:
        return ""
    return value.strip().strip("\r\n").strip()


def mask_key(value: str | None) -> str:
    """把密钥显示成脱敏形式（仅保留尾部少量字符）。"""
    text = clean_credential(value)
    if not text:
        return ""
    if len(text) <= 8:
        return REDACTED
    return f"{REDACTED}{text[-4:]}"


def redact(text: str | None, secret: str | None) -> str:
    """从任意文本（异常信息等）中抹掉密钥明文。"""
    result = text or ""
    secret_text = clean_credential(secret)
    if secret_text:
        # 含换行的原始密钥也要一并抹掉
        for raw in {secret_text, (secret or "").strip("\r\n"), secret or ""}:
            raw = raw.strip()
            if len(raw) >= 6:
                result = result.replace(raw, REDACTED)
    # 兜底：形如 sk-xxxx 的令牌片段
    result = re.sub(r"\b(sk-[A-Za-z0-9_\-]{8,})", REDACTED, result)
    return result
