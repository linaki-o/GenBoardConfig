"""LLM Provider 抽象：屏蔽各云端 API 差异。"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost: float = 0.0

    @property
    def total(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class LLMRequest:
    system: str = ""
    user: str = ""
    json_schema: dict[str, Any] | None = None
    temperature: float = 0.0
    max_tokens: int = 2048
    model: str = ""


@dataclass
class LLMResponse:
    content: str = ""
    parsed: Any = None
    usage: TokenUsage = field(default_factory=TokenUsage)
    latency_ms: int = 0
    raw: dict[str, Any] = field(default_factory=dict)
    error: str = ""


class LLMProvider(abc.ABC):
    """所有 LLM 后端的统一接口。"""

    name = "base"

    @abc.abstractmethod
    def complete(self, request: LLMRequest) -> LLMResponse: ...

    def health_check(self) -> tuple[bool, str]:
        return True, "ok"
