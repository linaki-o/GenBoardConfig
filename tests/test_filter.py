"""行过滤（HSI Sheet + GPIO TYPE=IN/OUT）端到端单测。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from openpyxl import Workbook  # noqa: E402

from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    profile_for_series,
)
from genboardconfig.domain.models import CheckStatus  # noqa: E402
from genboardconfig.infra.settings import load_settings  # noqa: E402

HEADERS = [
    "PIN #", "Chip Section", "PIN Name ", "Description/ Function", "AI",
    "Schematic Function", "GPIO  TYPE(输入输出类别)", "Output PIN 设定类型",
    "Power On", "Power Saving", "Power Off", "F/W Check", "EE Check",
]
ROWS = [
    ("C4", "Output", "PA2", "PA2/ADC6/PWMC", "", "+3V3C_EN", "OUT", "Open Drain", "High", "Low", "Low"),
    ("F20", "Output", "PC1", "PC1*/CEC1", "", "ON_BACKLIGHT", "OUT", "Push pull", "High", "Low", "Low"),
    ("A1", "Input", "PG3", "PG3*/ADC", "", "KEY_IN", "IN", "NA", "Low", "Low", "Low"),
    ("A2", "Input", "PG4", "PG4*/ADC", "", "ADC_IN", "", "NA", "Low", "Low", "Low"),
    ("A3", "Input", "PG5", "PG5*/ADC", "", "OTHER", "Analog", "NA", "Low", "Low", "Low"),
]

C_FILE = """#define PORT_A_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH,  LOW)
#define PORT_A_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT,  IN,  IN)
#define PORT_A_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW, HIGH,  LOW,  LOW,  LOW)
#define PORT_A_DEFAULT_PU      BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_C_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH,  LOW,  LOW, HIGH)
#define PORT_C_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT, OUT,  IN)
#define PORT_C_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW, LOW, HIGH, HIGH,  LOW)
#define PORT_C_DEFAULT_PU      BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_G_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH,  LOW)
#define PORT_G_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT,  IN,  IN)
#define PORT_G_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
#define PORT_G_DEFAULT_PU      BitsToByte( LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW,  LOW)
"""


def _build_excel(path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "HSI"
    ws["A1"] = "Hardware_Software_Interface Setting & Check"
    ws.append(HEADERS)
    for row in ROWS:
        ws.append(list(row) + ["PASS", "PASS"])
    other = wb.create_sheet("Other Requirements")
    other.append(["Check Item"])
    other.append(["与 GPIO 无关"])
    wb.save(path)


def _run(tmp_path: Path):
    excel = tmp_path / "hsi.xlsx"
    cfile = tmp_path / "BoardCfg.h"
    _build_excel(excel)
    cfile.write_text(C_FILE, encoding="utf-8")

    settings = load_settings()
    profile = profile_for_series(settings, "ntk")
    usecase = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    return profile, usecase.run(session, progress=lambda m, p: None, use_llm=False)


def test_only_in_out_rows_are_checked(tmp_path: Path):
    profile, result = _run(tmp_path)
    assert profile.excel_sheet == "HSI"
    stats = result.extra["filter_stats"]
    assert stats["mapped"] is True
    assert stats["kept"] == 3          # 2 个 OUT + 1 个 IN
    assert stats["skipped"] == 2       # 空 + Analog
    pins = {r.pin_name_raw for r in result.requirements}
    assert pins == {"PA2", "PC1", "PG3"}
    assert "PG4" not in pins and "PG5" not in pins


def test_fallback_column_used_when_primary_is_empty(tmp_path: Path):
    """GPIO TYPE 列全空时，自动回退到备用列（Chip Section）。"""
    excel = tmp_path / "hsi.xlsx"
    cfile = tmp_path / "BoardCfg.h"
    wb = Workbook()
    ws = wb.active
    ws.title = "HSI"
    ws.append(HEADERS)
    ws.append(["C4", "Output", "PA2", "PA2/ADC6", "", "+3V3C_EN", "", "Open Drain", "High", "Low", "Low", "PASS", "PASS"])
    ws.append(["A1", "Input", "PG3", "PG3/ADC", "", "KEY_IN", "", "NA", "Low", "Low", "Low", "PASS", "PASS"])
    wb.save(excel)
    cfile.write_text(C_FILE, encoding="utf-8")

    settings = load_settings()
    profile = profile_for_series(settings, "ntk")
    usecase = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    result = usecase.run(session, progress=lambda m, p: None, use_llm=False)

    stats = result.extra["filter_stats"]
    assert stats["fallback"] is True
    assert stats["used_field"] == "chip_section"
    assert stats["kept"] == 2
    assert result.summary.excel_rows == 2
    # 方向属性同步切换到备用列 → 仍参与判定
    direction = result.results[0].attribute("direction")
    assert direction.status == CheckStatus.MATCH
    assert direction.expected == "Output"
    assert any("备用列" in w for w in result.warnings)


def test_only_port_bit_tables_are_compared(tmp_path: Path):
    _profile, result = _run(tmp_path)
    # 结果只应引用 PORT_*_DEFAULT_* 条目
    referenced = {
        e.key
        for res in result.results
        for attr in res.attribute_results
        for e in result.entries
        if e.id in {ev.entry_id for ev in attr.evidence}
    }
    assert referenced, "应有位表证据"
    assert all(key.startswith("PORT_") for key in referenced), referenced


def test_na_value_is_not_judged(tmp_path: Path):
    _profile, result = _run(tmp_path)
    reqs = {r.id: r for r in result.requirements}
    key_row = next(r for r in result.results if reqs[r.requirement_id].pin_name_raw == "PG3")
    io_type = key_row.attribute("io_type")
    assert io_type.status == CheckStatus.NOT_APPLICABLE
    assert "NA" in (io_type.expected or "") or io_type.expected == "NA"
    assert "NA" in io_type.notes


def test_pull_up_is_ignored(tmp_path: Path):
    """PORT_X_DEFAULT_PU 暂时忽略：不出现在核对属性中，也不产生证据引用。"""
    _profile, result = _run(tmp_path)
    for res in result.results:
        assert res.attribute("pull_up") is None
    referenced = {
        e.key
        for res in result.results
        for attr in res.attribute_results
        for e in result.entries
        if e.id in {ev.entry_id for ev in attr.evidence}
    }
    assert not any("_DEFAULT_PU" in key for key in referenced), referenced


def test_only_three_attributes_are_checked(tmp_path: Path):
    """核对属性恰为 方向(G) / 输出类型(H) / 上电电平(I) 三项。"""
    _profile, result = _run(tmp_path)
    for res in result.results:
        names = [a.name for a in res.attribute_results]
        assert names == ["direction", "io_type", "power_on"], names
