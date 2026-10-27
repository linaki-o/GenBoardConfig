"""HSI 档案比对引擎单测（端口位表核对口径）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genboardconfig.domain.hsi import (  # noqa: E402
    HsiEngine,
    chip_pin_text,
    parse_chip_pin,
    parse_trailing_chip_pin,
)
from genboardconfig.domain.models import (  # noqa: E402
    CheckStatus,
    EntryKind,
    ExpectedAttribute,
    GPIORequirement,
)
from genboardconfig.domain.profiles import Profile  # noqa: E402
from genboardconfig.infra.cconfig.parser import CConfigParser  # noqa: E402

PROFILE_PATH = Path(__file__).resolve().parents[1] / "config" / "profiles" / "ntk.yaml"

SAMPLE = """#ifndef SAMPLE_H_
#define SAMPLE_H_

#define PORT_C_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH,  LOW,  LOW, HIGH)
#define PORT_C_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT, OUT,  IN)
#define PORT_C_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW, LOW, HIGH, HIGH,  LOW)
#define PORT_C_DEFAULT_PU      BitsToByte( LOW,  LOW,  LOW,  LOW, LOW,  LOW,  LOW,  LOW)

//Backlight control
#define BACKLIGHT_PORT          STBC_PORT_C//ON_BACKLIGHT
#define BACKLIGHT_BIT           BIT1
#define BACKLIGHT_ACTIVE        HIGH

//Panel power control
#define PANEL_POWER_PORT        STBC_PORT_C
#define PANEL_POWER_BIT         BIT2
#define PANEL_POWER_ACTIVE      HIGH

// USB 检测与背光共用 PC2
#define USBCG1_DET_PORT         STBC_PORT_C
#define USBCG1_DET_BIT          BIT2
#define USBCG1_DET_ACTIVE       HIGH

// PWM 输出
#define BKL_ADIM_PORT           PWM_B
#define BKL_ADIM_POL            HIGH
#define BKL_ADIM_OUTPUT_PIN     PWMB_PIN_PK1

#endif
"""


def _profile() -> Profile:
    return Profile.load(PROFILE_PATH)


def _engine() -> HsiEngine:
    profile = _profile()
    parser = CConfigParser(
        group_cfg=profile.c_cfg("group"), port_table_cfg=profile.c_cfg("port_table")
    )
    return HsiEngine(profile, parser.parse_text(SAMPLE).entries)


def _req(
    pin: str,
    direction: str = "OUT",
    io_type: str = "Push pull",
    power_on: str = "High",
    net: str = "TEST_NET",
):
    profile = _profile()
    values = {
        "direction": direction,
        "io_type": io_type,
        "power_on": power_on,
    }
    attrs = []
    for spec in profile.attributes:
        raw = values.get(spec.name, "")
        attrs.append(
            ExpectedAttribute(
                name=spec.name,
                label=spec.label,
                source_field=spec.from_field,
                value=raw,
                normalized=profile.map_value(spec.name, raw) if raw else "",
                checkable=spec.checkable and bool(raw),
                check=spec.check,
            )
        )
    return GPIORequirement(
        id="R0001",
        sheet="HSI",
        row_no=6,
        pin_name_raw=pin,
        config_key=net,
        net_name=net,
        attributes=attrs,
    )


# ----------------------------------------------------------------------
def test_parse_chip_pin():
    assert parse_chip_pin("PC1") == ("C", 1)
    assert parse_chip_pin("PK1/PWMB") == ("K", 1)
    assert parse_chip_pin("PB6/DPRX1_HPD") == ("B", 6)
    assert chip_pin_text("C", 1) == "PC1"


def test_parse_trailing_chip_pin():
    assert parse_trailing_chip_pin("PSM2_PIN_PK2") == ("K", 2)
    assert parse_trailing_chip_pin("PWMB_PIN_PK1") == ("K", 1)
    assert parse_trailing_chip_pin("BIT3") is None


def test_parser_extracts_port_bit_with_exact_span():
    profile = _profile()
    parser = CConfigParser(
        group_cfg=profile.c_cfg("group"), port_table_cfg=profile.c_cfg("port_table")
    )
    result = parser.parse_text(SAMPLE)
    entry = next(
        e for e in result.entries
        if e.kind == EntryKind.PORT_BIT and e.key == "PORT_C_DEFAULT_OUT[1]"
    )
    assert entry.value_raw == "LOW"
    line = SAMPLE.split("\n")[entry.line - 1]
    assert line[entry.value_col : entry.value_col + entry.value_len] == "LOW"


def test_signal_groups_are_context_only():
    engine = _engine()
    assert "BKL_ADIM" in engine.groups
    assert engine.groups["BKL_ADIM"].derived_pin() == ("K", 1)
    assert engine.signals_on("C", 1) == ["BACKLIGHT"]
    assert engine.signals_on("C", 2) == ["PANEL_POWER", "USBCG1_DET"]


def test_engine_matching_row_is_consistent():
    engine = _engine()
    req = _req("PC1", direction="OUT", io_type="Push pull", power_on="Low")
    result = engine.check([req])[0]
    assert result.symbol == "PC1"
    assert result.status == CheckStatus.MATCH
    assert result.attribute("power_on").status == CheckStatus.MATCH
    assert result.attribute("direction").actual == "OUT"


def test_engine_detects_power_on_mismatch():
    engine = _engine()
    req = _req("PC1", power_on="High")
    result = engine.check([req])[0]
    attr = result.attribute("power_on")
    assert attr.status == CheckStatus.MISMATCH
    assert attr.actual == "LOW"
    assert attr.change is not None
    assert attr.change.type.value == "set_port_bit"
    target = engine.entries_by_id[attr.change.target]
    assert target.key == "PORT_C_DEFAULT_OUT[1]"
    assert target.value_raw == "LOW"


def test_engine_detects_direction_mismatch():
    engine = _engine()
    req = _req("PC1", direction="IN")
    result = engine.check([req])[0]
    attr = result.attribute("direction")
    assert attr.status == CheckStatus.MISMATCH
    assert attr.actual == "OUT"
    assert attr.change.new_value == "IN"


def test_engine_conflict_blocks_auto_edit():
    """同一 (端口,位) 被两行要求且期望值冲突 → 判为歧义且不自动改写。"""
    engine = _engine()
    req_a = _req("PC1", power_on="High")
    req_b = _req("PC1", power_on="Low")
    req_b.id = "R0002"
    results = engine.check([req_a, req_b])
    for res in results:
        attr = res.attribute("power_on")
        assert attr.status == CheckStatus.AMBIGUOUS
        assert attr.change is not None
        assert attr.change.type.value == "none"
        assert "冲突" in attr.change.reason


def test_engine_marks_unparsable_pin():
    engine = _engine()
    req = _req("NOT_A_PIN", power_on="High")
    result = engine.check([req])[0]
    assert result.status == CheckStatus.UNRESOLVED


def test_engine_reports_missing_bit_table():
    engine = _engine()
    req = _req("PF7", power_on="High")
    result = engine.check([req])[0]
    attr = result.attribute("power_on")
    assert attr.status == CheckStatus.MISSING


def test_profile_row_filter():
    profile = _profile()
    assert profile.filter_field == "gpio_type"
    assert profile.filter_values == ["IN", "OUT"]
    assert profile.passes_filter({"gpio_type": "IN"}) is True
    assert profile.passes_filter({"gpio_type": "out"}) is True
    assert profile.passes_filter({"gpio_type": ""}) is False
    assert profile.passes_filter({"gpio_type": "Analog"}) is False


def test_profile_override_switches_filter_column():
    profile = _profile()
    profile.apply_override({"field": "chip_section", "values": ["Output"]})
    assert profile.filter_field == "chip_section"
    assert profile.passes_filter({"chip_section": "Output"}) is True
    assert profile.passes_filter({"gpio_type": "IN"}) is False
