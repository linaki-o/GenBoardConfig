"""功能名等效性复核（RTK L2）的模型交互回归测试。

覆盖三类线上事故：
1. 推理模型把思考过程写在 ``<think>…</think>`` 里，JSON 答案在其后甚至被截断
2. ``finish_reason=length``（输出被 max_tokens 截断）此前被静默吞掉，
   界面只能显示「模型未给出结论」
3. 一次送太多条目 + 可选功能清单里的测试脚噪声，会把模型的输出预算耗光
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import httpx  # noqa: E402

from genboardconfig.app.check_usecase import CheckUseCase  # noqa: E402
from genboardconfig.infra.llm.orchestrator import LLMOrchestrator  # noqa: E402
from genboardconfig.infra.llm.prompt_repo import PromptRepo  # noqa: E402
from genboardconfig.infra.llm.provider.base import (  # noqa: E402
    LLMProvider,
    LLMRequest,
    LLMResponse,
    TokenUsage,
)
from genboardconfig.infra.llm.provider.openai_compatible import (  # noqa: E402
    OpenAICompatibleProvider,
)

ROOT = Path(__file__).resolve().parents[1]


def _item(rid: str = "R0010") -> dict:
    return {
        "requirement_id": rid,
        "net_name": "BL_ADIM",
        "excel_function": "PWM_2",
        "header_function": "PWM2_PP",
        "pad": "109",
        "excel_gpio_type": "OUT",
        "excel_description": "PWM_2/USB_SPI_CEB1_0_5/TCON[6]/GPIO",
        "options": ["GPI", "GPO_PP", "PWM2_PP"],
    }


class _StubProvider(LLMProvider):
    """按顺序返回预设响应的假 Provider。"""

    name = "stub"

    def __init__(self, responses: list[LLMResponse]):
        super().__init__()
        self.model = "stub-model"
        self.responses = list(responses)
        self.calls: list[LLMRequest] = []

    def complete(self, request: LLMRequest) -> LLMResponse:
        self.calls.append(request)
        idx = min(len(self.calls) - 1, len(self.responses) - 1)
        return self.responses[idx]


def _orchestrator(provider) -> LLMOrchestrator:
    return LLMOrchestrator(
        provider=provider,
        prompt_repo=PromptRepo(ROOT / "config"),
        masker=None,
        review_batch_size=3,
        review_max_tokens=8192,
    )


def _ok_response(ids: list[str]) -> LLMResponse:
    payload = {
        "results": [
            {
                "requirement_id": rid,
                "equivalent": True,
                "confidence": 0.9,
                "reason": "同一功能",
                "electrical_match": True,
                "electrical_reason": "方向一致",
            }
            for rid in ids
        ]
    }
    return LLMResponse(
        content=json.dumps(payload, ensure_ascii=False),
        parsed=payload,
        usage=TokenUsage(prompt_tokens=10, completion_tokens=10),
        finish_reason="stop",
    )


# ----------------------------------------------------------------------
# 1. 推理模型的 <think> 块
# ----------------------------------------------------------------------
def test_safe_json_strips_think_block():
    payload = {"results": [{"requirement_id": "R0010", "equivalent": True}]}
    content = (
        "<think>先看 R0010：PWM_2 与 PWM2_PP 是别名 {不是 JSON}\n推理结束</think>\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    assert OpenAICompatibleProvider._safe_json(content) == payload


def test_safe_json_handles_think_plus_fenced_json():
    content = "<think>思考</think>\n```json\n{\"results\": []}\n```"
    assert OpenAICompatibleProvider._safe_json(content) == {"results": []}


def test_safe_json_returns_none_for_truncated_think():
    """思考未结束就被截断时没有 JSON，必须返回 None 而不是半截对象。"""
    assert OpenAICompatibleProvider._safe_json("<think>想到一半…{") is None


# ----------------------------------------------------------------------
# 2. finish_reason 透传
# ----------------------------------------------------------------------
def test_provider_reports_finish_reason(monkeypatch):
    class _Resp:
        status_code = 200
        text = ""

        def json(self):
            return {
                "choices": [
                    {
                        "message": {"content": '{"results": []}'},
                        "finish_reason": "length",
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 20},
            }

    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            return _Resp()

    monkeypatch.setattr(httpx, "Client", _Client)
    provider = OpenAICompatibleProvider(
        base_url="https://example.invalid/v1", api_key="k", model="m"
    )
    response = provider.complete(LLMRequest(system="s", user="u"))
    assert response.finish_reason == "length"
    assert response.parsed == {"results": []}


def test_provider_reports_timeout_clearly(monkeypatch):
    """推理模型生成慢撞上超时上限时，错误信息要说明是超时而不是泛化异常。"""

    class _Client:
        def __init__(self, *a, **k):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def post(self, *a, **k):
            raise httpx.ReadTimeout("The read operation timed out")

    monkeypatch.setattr(httpx, "Client", _Client)
    monkeypatch.setattr(time, "sleep", lambda *a, **k: None)
    provider = OpenAICompatibleProvider(
        base_url="https://example.invalid/v1",
        api_key="k",
        model="m",
        timeout=1.5,
        max_retries=2,
    )
    response = provider.complete(LLMRequest(system="s", user="u"))
    assert "请求超时" in response.error
    assert "1.5" in response.error
    assert "2" in response.error


# ----------------------------------------------------------------------
# 3. 分批 / 截断原因上报 / 噪声过滤
# ----------------------------------------------------------------------
def test_review_functions_splits_into_small_batches():
    """5 条拆成 3+2 两次请求，避免一次输出过长被截断。"""
    provider = _StubProvider([_ok_response(["R1", "R2", "R3"]), _ok_response(["R4", "R5"])])
    orch = _orchestrator(provider)
    items = [_item(f"R{i}") for i in range(1, 6)]
    verdicts = orch.review_functions(items)

    assert len(provider.calls) == 2
    assert len(json.loads(provider.calls[0].user)["items"]) == 3
    assert len(json.loads(provider.calls[1].user)["items"]) == 2
    assert set(verdicts) == {"R1", "R2", "R3", "R4", "R5"}
    # 输出预算必须给足，否则推理模型思考阶段就被截断
    assert provider.calls[0].max_tokens == 8192


def test_review_functions_reports_truncation_reason():
    """输出被 max_tokens 截断时，必须留下真实原因而不是静默返回空。"""
    provider = _StubProvider(
        [
            LLMResponse(
                content="<think>还在思考就被截断了…",
                parsed=None,
                finish_reason="length",
            )
        ]
    )
    orch = _orchestrator(provider)
    verdicts = orch.review_functions([_item("R1")])

    assert verdicts == {}
    assert any("截断" in m for m in orch.stats.messages)
    assert "截断" in orch.review_failure("R1")
    assert any(e.startswith("✗") for e in orch.stats.events)


def test_review_functions_reports_unparsable_output():
    provider = _StubProvider([LLMResponse(content="这不是 JSON", parsed=None)])
    orch = _orchestrator(provider)
    orch.review_functions([_item("R1")])
    assert any("无法解析" in m for m in orch.stats.messages)
    assert "无法解析" in orch.review_failure("R1")


def test_review_functions_marks_items_without_verdict():
    """模型只回答了一部分时，未回答的条目也要有原因。"""
    provider = _StubProvider([_ok_response(["R1"])])
    orch = _orchestrator(provider)
    orch.review_functions([_item("R1"), _item("R2")])
    assert orch.review_failure("R1") == ""
    assert "未对" in orch.review_failure("R2")


def test_useful_options_filters_test_pins():
    """测试脚噪声要从送模型的清单里去掉，既省 token 也缩短推理。"""
    members = [
        "GPI",
        "GPO_PP",
        "GPO_OD",
        "PWM2_PP",
        "TCON11",
        "TEST12B_OUT0",
        "TEST4B_OUT1",
        "NC",
    ]
    assert CheckUseCase._useful_options(members) == [
        "GPI",
        "GPO_PP",
        "GPO_OD",
        "PWM2_PP",
        "TCON11",
        "NC",
    ]


def test_useful_options_keeps_real_functions_only():
    assert CheckUseCase._useful_options(["TEST12B_OUT0", "TEST12B_OUT10"]) == []
