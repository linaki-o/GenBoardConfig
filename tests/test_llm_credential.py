"""凭据清洗与脱敏单测。

用户从网页/文档复制 API Key 时常带尾部换行，HTTP 请求头不允许 CR/LF，
httpx 会抛 ``LocalProtocolError: Illegal header value``。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import httpx  # noqa: E402
import pytest  # noqa: E402

from genboardconfig.app.service_factory import resolve_api_key  # noqa: E402
from genboardconfig.infra.llm.provider.credential import (  # noqa: E402
    clean_credential,
    mask_key,
    redact,
)
from genboardconfig.infra.llm.provider.openai_compatible import (  # noqa: E402
    OpenAICompatibleProvider,
)
from genboardconfig.infra.secrets.store import SecretStore  # noqa: E402
from genboardconfig.infra.settings import Settings  # noqa: E402

# 示例密钥（占位串，非真实凭据）：真实密钥带尾部换行时 httpx 会拒绝该请求头
DIRTY_KEY = "sk-cp-EXAMPLEPLACEHOLDER00000000000000000000000000\n\n"


def test_clean_credential_strips_newlines():
    assert clean_credential(DIRTY_KEY) == DIRTY_KEY.strip()
    assert clean_credential("  abc \r\n ") == "abc"
    assert clean_credential(None) == ""
    assert clean_credential("") == ""


def test_provider_strips_api_key():
    provider = OpenAICompatibleProvider(
        base_url="https://example.invalid/v1", api_key=DIRTY_KEY, model="m"
    )
    assert "\n" not in provider.api_key
    assert provider.api_key == DIRTY_KEY.strip()


def test_provider_builds_legal_authorization_header():
    """带换行的密钥清洗后，httpx 必须接受该请求头。"""
    provider = OpenAICompatibleProvider(
        base_url="https://example.invalid/v1", api_key=DIRTY_KEY, model="m"
    )
    request = httpx.Request(
        "POST",
        "https://example.invalid/v1/chat/completions",
        headers={"Authorization": f"Bearer {provider.api_key}"},
    )
    assert request.headers["Authorization"] == f"Bearer {DIRTY_KEY.strip()}"


def test_resolve_api_key_cleans_stored_secret(tmp_path):
    """凭据库里已存脏密钥时，读取即清洗，用户无需重新录入。"""
    store = SecretStore(tmp_path / "secrets.bin")
    store.set("llm_api_key", DIRTY_KEY)
    settings = Settings(data={}, config_dir=tmp_path)
    assert resolve_api_key(settings) == DIRTY_KEY.strip()


def test_resolve_api_key_cleans_yaml_value(tmp_path):
    settings = Settings(data={"llm": {"api_key": "  yaml-key\n"}}, config_dir=tmp_path)
    assert resolve_api_key(settings) == "yaml-key"


def test_redact_removes_secret_from_error_text():
    error = f"LocalProtocolError: Illegal header value b'Bearer {DIRTY_KEY}'"
    masked = redact(error, DIRTY_KEY)
    assert "sk-cp-" not in masked
    assert DIRTY_KEY.strip() not in masked


def test_redact_fallback_masks_token_like_strings():
    """即使不知道密钥本身，形如 sk-xxxx 的片段也不应进日志。"""
    assert "sk-cp-AAAABBBBCCCC" not in redact("failed for sk-cp-AAAABBBBCCCC", "")


def test_redact_keeps_short_values_untouched():
    """过短的片段不做替换，避免误伤普通文本。"""
    assert redact("abc def", "abc") == "abc def"


def test_mask_key_shows_only_tail():
    assert mask_key("sk-1234567890abcdef") == "***cdef"
    assert mask_key("") == ""


def test_provider_does_not_retry_on_illegal_header(monkeypatch):
    """请求头非法属客户端错误，重试无意义，应立即返回。"""
    calls = {"n": 0}

    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            calls["n"] += 1
            raise httpx.LocalProtocolError("Illegal header value b'Bearer x\\n\\n'")

    monkeypatch.setattr(httpx, "Client", _Client)
    provider = OpenAICompatibleProvider(
        base_url="https://example.invalid/v1", api_key=DIRTY_KEY, model="m", max_retries=3
    )
    response = provider.complete(_request())
    assert calls["n"] == 1
    assert "Illegal header value" in response.error
    assert "sk-cp-" not in response.error


def _request():
    from genboardconfig.infra.llm.provider.base import LLMRequest

    return LLMRequest(system="s", user="u")
