"""OpenAI 兼容接口 Provider（覆盖 OpenAI / DeepSeek / 通义 / 各类内部网关）。"""

from __future__ import annotations

import json
import re
import time

import httpx

from .base import LLMProvider, LLMRequest, LLMResponse, TokenUsage
from .credential import clean_credential, redact

PRICE_PER_1K = 0.0005  # 粗略估算，可在设置中覆盖


class OpenAICompatibleProvider(LLMProvider):
    name = "openai_compatible"

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str,
        timeout: float = 60.0,
        max_retries: int = 3,
        use_structured_output: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        # 末尾换行等非法字符会让 httpx 抛 Illegal header value，这里统一清洗
        self.api_key = clean_credential(api_key)
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.use_structured_output = use_structured_output

    # ------------------------------------------------------------------
    def complete(self, request: LLMRequest) -> LLMResponse:
        model = request.model or self.model
        payload: dict = {
            "model": model,
            "messages": [
                {"role": "system", "content": request.system},
                {"role": "user", "content": request.user},
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        if self.use_structured_output and request.json_schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": request.json_schema,
            }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        last_error = ""
        for attempt in range(self.max_retries):
            started = time.perf_counter()
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    resp = client.post(
                        f"{self.base_url}/chat/completions", json=payload, headers=headers
                    )
                if resp.status_code >= 400:
                    last_error = redact(
                        f"HTTP {resp.status_code}: {resp.text[:300]}", self.api_key
                    )
                    if resp.status_code in (401, 403, 404):
                        break
                    time.sleep(min(2 ** attempt, 8))
                    continue
                data = resp.json()
                choice = (data.get("choices") or [{}])[0]
                content = (choice.get("message") or {}).get("content")
                usage = data.get("usage", {}) or {}
                return LLMResponse(
                    content=content or "",
                    parsed=self._safe_json(content or ""),
                    usage=TokenUsage(
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0),
                        estimated_cost=(
                            usage.get("prompt_tokens", 0)
                            + usage.get("completion_tokens", 0)
                        )
                        / 1000
                        * PRICE_PER_1K,
                    ),
                    latency_ms=int((time.perf_counter() - started) * 1000),
                    raw=data,
                    finish_reason=str(choice.get("finish_reason") or ""),
                )
            except httpx.LocalProtocolError as exc:
                # 请求头非法（如密钥带换行）：重试无意义，直接报错
                last_error = redact(f"{type(exc).__name__}: {exc}", self.api_key)
                break
            except httpx.TimeoutException as exc:
                # 推理模型生成慢，单次请求可能撞上超时上限（如 8192 token 的思考）
                last_error = redact(
                    f"请求超时（单次上限 {self.timeout:g}s，"
                    f"已尝试 {attempt + 1}/{self.max_retries} 次）："
                    f"{type(exc).__name__}: {exc}",
                    self.api_key,
                )
                time.sleep(min(2 ** attempt, 8))
            except Exception as exc:  # noqa: BLE001
                last_error = redact(f"{type(exc).__name__}: {exc}", self.api_key)
                time.sleep(min(2 ** attempt, 8))
        return LLMResponse(error=last_error or "unknown error")

    @staticmethod
    def _strip_think(text: str) -> str:
        """剥掉推理模型的思考块（<think>…</think>，含未闭合的情况）。"""
        text = re.sub(r"<think>.*?</think>", " ", text, flags=re.S | re.I)
        return re.sub(r"<think>.*", " ", text, flags=re.S | re.I)

    @classmethod
    def _safe_json(cls, content: str):
        if not content:
            return None
        text = cls._strip_think(content).strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        if text.endswith("```"):
            text = text[:-3].strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    return None
            return None

    def health_check(self) -> tuple[bool, str]:
        if not self.api_key:
            return False, "未配置 API Key"
        if not self.base_url:
            return False, "未配置 base_url"
        return True, f"{self.name}:{self.model}"
