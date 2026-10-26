"""领域层单测（脱网）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genboardconfig.domain.matcher import Matcher, significant_tokens
from genboardconfig.domain.normalize import (
    norm_gpio_num,
    norm_key,
    norm_pin,
    norm_value,
    values_equivalent,
)
from genboardconfig.domain.rules import RuleEngine


def test_norm_key_keeps_chinese():
    assert norm_key("管脚名") == "管脚名"
    assert norm_key("GPIO  Number") == "GPIO_NUMBER"


def test_norm_pin_variants():
    for raw in ["GPIO_PC13", "PC13", "pc 13", "PC_13"]:
        assert norm_pin(raw)[0] == "PC13"
    assert norm_pin("GPIOC13")[0] == "C13"
    assert norm_pin("GPIOA_5")[0] == "A5"


def test_norm_gpio_num():
    assert norm_gpio_num("47") == 47
    assert norm_gpio_num("0x2F") == 47
    assert norm_gpio_num("") is None
    assert norm_gpio_num("abc") is None


def test_norm_value_decimalizes_hex():
    assert norm_value("0x2F") == "47"
    assert norm_value(" 48 ") == "48"


def test_values_equivalent_aliases():
    aliases = {"1": ["true", "yes"], "0": ["false", "no"]}
    assert values_equivalent("1", "true", aliases)
    assert not values_equivalent("1", "0", aliases)
    assert values_equivalent("GPIO_PC13", "PC13")


def test_significant_tokens_excludes_generic():
    assert significant_tokens("CONFIG_LED1_GPIO") == {"LED1"}
    assert significant_tokens("GPIO") == set()
    assert significant_tokens("CONFIG_FAN_GPIO") == {"FAN"}


def test_matcher_prefers_exact_config_key():
    matcher = Matcher()
    req = _req(config_key="CONFIG_LED3_GPIO", function="LED3", gpio_num=15)
    entries = [
        _entry("E1", "macro", "CONFIG_LED1_GPIO", "48"),
        _entry("E2", "macro", "CONFIG_LED3_GPIO", "61"),
        _entry("E3", "struct_field", "gpio", "5"),
    ]
    candidates = matcher.candidates(req, entries)
    assert candidates[0].entry.id == "E2"
    assert candidates[0].score >= 0.9


def test_matcher_does_not_match_generic_field():
    matcher = Matcher()
    req = _req(config_key="CONFIG_FAN_GPIO", function="FAN", gpio_num=21)
    entries = [_entry("E1", "struct_field", "gpio", "5")]
    assert matcher.candidates(req, entries) == []


def test_rule_engine_detects_mismatch():
    engine = RuleEngine(confidence_threshold=0.8)
    req = _req(config_key="CONFIG_LED3_GPIO", expected="60")
    entry = _entry("E1", "macro", "CONFIG_LED3_GPIO", "61")
    result = engine.decide(req, _candidates(entry, 1.0), {"E1": entry})
    assert result.status.value == "mismatch"
    assert result.current_value == "61"


def test_rule_engine_treats_pin_name_as_equal():
    engine = RuleEngine(confidence_threshold=0.8)
    req = _req(config_key="CONFIG_BEEP_GPIO", expected="5", pin="GPIO_PB5")
    entry = _entry("E1", "array_item", "BEEP", "GPIO_PB5")
    result = engine.decide(req, _candidates(entry, 0.88), {"E1": entry})
    assert result.status.value == "match"


def test_rule_engine_downgrades_low_confidence():
    engine = RuleEngine(confidence_threshold=0.8)
    req = _req(config_key="CONFIG_X_GPIO", expected="9")
    entry = _entry("E1", "macro", "CONFIG_X_GPIO", "1")
    result = engine.decide(req, _candidates(entry, 0.45), {"E1": entry})
    result = engine.downgrade(result)
    assert result.status.value == "ambiguous"


# ----------------------------------------------------------------------
def _req(config_key: str = "", expected: str = "", function: str = "", gpio_num=None, pin: str = ""):
    from genboardconfig.domain.models import GPIORequirement
    from genboardconfig.domain.normalize import norm_gpio_num, norm_key, norm_pin

    return GPIORequirement(
        id="R1",
        pin_name_raw=pin,
        pin_key=norm_pin(pin)[0],
        gpio_num=gpio_num,
        function_name=function,
        config_key=config_key,
        config_key_norm=norm_key(config_key),
        expected_value=expected,
    )


def _entry(id_: str, kind: str, key: str, value: str):
    from genboardconfig.domain.models import ConfigEntry, EntryKind
    from genboardconfig.domain.normalize import norm_key, norm_value

    return ConfigEntry(
        id=id_,
        kind=EntryKind(kind),
        key=key,
        key_norm=norm_key(key),
        value_raw=value,
        value_normalized=norm_value(value),
        line=10,
    )


def _candidates(entry, score: float):
    from genboardconfig.domain.matcher import Candidate

    return [Candidate(entry=entry, score=score, reason="test")]
