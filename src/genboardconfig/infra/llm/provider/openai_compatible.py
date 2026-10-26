"""OpenAI 兼容接口 Provider（覆盖 OpenAI / DeepSeek / 通义 / 各类内部网关）。"""

from __future__ import annotations

import json
import re
import time

import httpx

from .base import LLMProvider, LLMRequest, LLMResponse, TokenUsage

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
        self.api_key = api_key
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
                    last_error = f"HTTP {resp.status_code}: {resp.text[:300]}"
                    if resp.status_code in (401, 403, 404):
                        break
                    time.sleep(min(2 ** attempt, 8))
                    continue
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {}) or {}
                return LLMResponse(
                    content=content,
                    parsed=self._safe_json(content),
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
                )
            except Exception as exc:  # noqa: BLE001
                last_error = f"{type(exc).__name__}: {exc}"
                time.sleep(min(2 ** attempt, 8))
        return LLMResponse(error=last_error or "unknown error")

    @staticmethod
    def _safe_json(content: str):
        if not content:
            return None
        text = content.strip()
        fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.S)
        if fence:
            text = fence.group(1)
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
