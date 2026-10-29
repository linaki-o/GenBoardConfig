"""并排对比视图单测（离屏）。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtCore import Qt  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    profile_for_series,
)
from genboardconfig.domain.models import CheckStatus  # noqa: E402
from genboardconfig.infra.settings import load_settings  # noqa: E402
from genboardconfig.ui.compare_view import CompareView  # noqa: E402

C_FILE = """#define PORT_C_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH,  LOW,  LOW, HIGH)
#define PORT_C_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT, OUT,  IN)
#define PORT_C_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW, LOW, HIGH, HIGH,  LOW)
#define PORT_A_DEFAULT_OUT     BitsToByte(HIGH, HIGH, HIGH, HIGH, HIGH, HIGH, HIGH,  LOW)
#define PORT_A_DEFAULT_DIR     BitsToByte( IN,  IN,  IN,  IN, IN, OUT,  IN,  IN)
#define PORT_A_DEFAULT_PP      BitsToByte( LOW,  LOW,  LOW,  LOW, HIGH,  LOW,  LOW,  LOW)
"""


def _make_result(tmp_path: Path):
    from openpyxl import Workbook

    excel = tmp_path / "hsi.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "HSI"
    ws.append(
        [
            "PIN #", "Chip Section", "PIN Name ", "Description/ Function", "AI",
            "Schematic Function", "GPIO  TYPE(输入输出类别)", "Output PIN 设定类型",
            "Power On", "Power Saving", "Power Off", "F/W Check", "EE Check",
        ]
    )
    ws.append(["C4", "Output", "PA2", "PA2/ADC6", "", "+3V3C_EN", "OUT", "Open Drain", "High", "Low", "Low", "PASS", "PASS"])
    ws.append(["F20", "Output", "PC1", "PC1*/CEC1", "", "ON_BACKLIGHT", "OUT", "Push pull", "High", "Low", "Low", "PASS", "PASS"])
    wb.save(excel)
    cfile = tmp_path / "BoardCfg.h"
    cfile.write_text(C_FILE, encoding="utf-8")

    settings = load_settings()
    profile = profile_for_series(settings, "ntk")
    usecase = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    return usecase.run(session, progress=lambda m, p: None, use_llm=False)


def _app() -> QApplication:
    return QApplication.instance() or QApplication([])


def test_compare_view_shows_both_sides(tmp_path: Path):
    _app()
    result = _make_result(tmp_path)
    view = CompareView()
    view.set_result(result)
    assert view.left_model.rowCount() == 2          # Excel 行
    assert view.right_model.rowCount() == 6          # 2 行 × 3 属性
    # 右侧按 Excel 行分组：DIR → PP → OUT
    keys = [
        view.right_model.data(view.right_model.index(r, 1))
        for r in range(view.right_model.rowCount())
    ]
    assert keys[0].endswith("_DIR[2]")
    assert keys[1].endswith("_PP[2]")
    assert keys[2].endswith("_OUT[2]")


def test_mismatch_is_colored_red(tmp_path: Path):
    _app()
    result = _make_result(tmp_path)
    view = CompareView()
    view.set_result(result)

    # 左侧：PC1 行的上电电平(I)单元格应为红底
    row = next(
        r for r in range(view.left_model.rowCount())
        if view.left_model.data(view.left_model.index(r, 1)) == "PC1"
    )
    bg = view.left_model.data(view.left_model.index(row, 5), Qt.BackgroundRole)
    assert bg is not None and bg.color().name().lower() == "#fef2f2"

    # 右侧：对应 OUT 单元格的「实际值」与「判定」为红底
    idx = next(
        r for r in range(view.right_model.rowCount())
        if view.right_model.data(view.right_model.index(r, 1)).endswith("_OUT[1]")
    )
    assert view.right_model.data(view.right_model.index(idx, 4)) == "不一致"
    bg = view.right_model.data(view.right_model.index(idx, 3), Qt.BackgroundRole)
    assert bg is not None and bg.color().name().lower() == "#fef2f2"


def test_selection_links_both_sides(tmp_path: Path):
    app = _app()
    result = _make_result(tmp_path)
    view = CompareView()
    view.set_result(result)
    view.show()

    view.left.selectRow(0)
    app.processEvents()
    selected = [i.row() for i in view.right.selectionModel().selectedRows()]
    assert sorted(selected) == [0, 1, 2]      # 该行的 3 个条目


# ----------------------------------------------------------------------
# 回归：同一 .h 条目被多个属性引用时，右表「判定」必须取最严重的一条
# （RTK 的一行有 方向/类别、输出类型、功能名 三个属性指向同一条 #define，
#   其中「功能名」是标注型（一致），不能覆盖前面的「不一致」）
# ----------------------------------------------------------------------
RTK_SAMPLE = """//---------------------------------------------------------------------------
// Function : LEDG
//---------------------------------------------------------------------------
#define _PIN_H4                  (_PIN_H4_GPI)

typedef enum
{
    _PIN_H4_GPI = 0x00,
    _PIN_H4_GPO_PP = 0x01,
    _PIN_H4_GPO_OD = 0x02,
    _PIN_H4_PWM_IN = 0x03,
    _PIN_H4_NC = _PIN_H4_GPO_PP,
} EnumPinshareInfoPINH4;
"""


def test_rtk_right_pane_keeps_worst_verdict(tmp_path: Path):
    from openpyxl import Workbook

    from genboardconfig.domain.profiles import Profile

    profile = Profile.load(
        Path(__file__).resolve().parents[1] / "config" / "profiles" / "rtk.yaml"
    )
    excel = tmp_path / "hsi.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "HSI"
    ws.append(
        [
            "PIN #", "Chip Section", "PIN Name ", "Description/ Function", "AI",
            "Schematic Function", "GPIO  TYPE(输入输出类别)", "Output PIN 设定类型",
            "Power On", "Power Saving", "Power Off", "F/W Check", "EE Check",
        ]
    )
    ws.append(["G5", "Output", "PWM_IN / PWM_2 / GPIO", "desc", "", "LEDG", "OUT",
               "Open-Drain Output", "Low", "Low", "High", "PASS", "PASS"])
    wb.save(excel)
    cfile = tmp_path / "pinshare.h"
    cfile.write_text(RTK_SAMPLE, encoding="utf-8")

    settings = load_settings()
    usecase = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    result = usecase.run(session, progress=lambda m, p: None, use_llm=False)

    row = result.results[0]
    assert row.status == CheckStatus.MISMATCH
    # 三个属性指向同一条 entry
    assert len({ev.entry_id for a in row.attribute_results for ev in a.evidence}) == 1

    _app()
    view = CompareView()
    view.set_result(result)
    assert view.right_model.rowCount() == 1
    verdict = view.right_model.data(view.right_model.index(0, 4))
    assert verdict == "不一致", f"右表判定应为不一致，实际 {verdict}"
