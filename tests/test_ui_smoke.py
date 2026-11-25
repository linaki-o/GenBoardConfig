"""UI 构造冒烟：确保各对话框/主窗口在离屏环境下能正常创建。

这类测试的价值：像「设置对话框缺 import」这类只在点击时才暴露的错误，
在这里就能被 pytest 抓到。
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest  # noqa: E402
from PySide6.QtCore import Qt  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.app.service_factory import profile_for_series  # noqa: E402
from genboardconfig.domain.models import CheckResult, CheckSummary  # noqa: E402
from genboardconfig.infra.settings import load_settings  # noqa: E402
from genboardconfig.ui.main_window import GOLDEN_RATIO, MainWindow  # noqa: E402
from genboardconfig.ui.settings_dialog import SettingsDialog  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402


def _app() -> QApplication:
    app = QApplication.instance() or QApplication([])
    apply_style(app)
    return app


def _pump(seconds: float = 2.0) -> None:
    """跑一小段事件循环，让延迟执行的布局调整生效。"""
    app = QApplication.instance()
    deadline = time.time() + seconds
    while time.time() < deadline:
        app.processEvents()
        time.sleep(0.01)


def test_main_window_constructs():
    _app()
    win = MainWindow()
    assert win.tabs.count() >= 4
    assert win.btn_check is not None
    win.close()


def test_left_overview_dock_collapsed_by_default():
    """左侧「核对概览」默认折叠，可经「视图」菜单展开。"""
    _app()
    win = MainWindow()
    win.show()
    _pump(0.2)
    assert win.left_dock.isVisible() is False
    assert win.right_dock.isVisible() is True

    win.act_left_dock.setChecked(True)
    _pump(0.2)
    assert win.left_dock.isVisible() is True

    win.act_left_dock.setChecked(False)
    _pump(0.2)
    assert win.left_dock.isVisible() is False
    win.close()


def test_center_and_detail_panes_use_golden_ratio():
    """中部主表 : 右侧「条目详情」= 黄金比例 φ ≈ 1.618。"""
    _app()
    win = MainWindow()
    win.show()
    _pump(2.0)

    center = win.centralWidget().width()
    right = win.right_dock.width()
    assert right > 0
    assert center / right == pytest.approx(GOLDEN_RATIO, abs=0.05)
    win.close()


def test_result_table_has_no_apply_column():
    """「应用」列已删除，核对明细表第一列是「状态」。"""
    from genboardconfig.domain.models import CheckStatus, MatchResult
    from genboardconfig.ui.models import ResultTableModel

    _app()
    res = MatchResult(requirement_id="R1", status=CheckStatus.MISMATCH)
    model = ResultTableModel()
    model.set_result(
        CheckResult(requirements=[], entries=[], results=[res], summary=CheckSummary(total=1))
    )
    assert model.headerData(0, Qt.Horizontal) == "状态"
    assert model.data(model.index(0, 0), Qt.DisplayRole) == "不一致"
    assert "应用" not in model._headers


def test_apply_targets_mismatch_rows_only():
    """「不一致」的行默认都要修改；其余行不进入写回集合。"""
    from types import SimpleNamespace

    from genboardconfig.app.apply_usecase import ApplyUseCase
    from genboardconfig.domain.models import (
        ChangeType,
        CheckStatus,
        ConfigEntry,
        EntryKind,
        MatchResult,
        ProposedChange,
    )

    entry = ConfigEntry(
        id="E1",
        kind=EntryKind.MACRO_FUNC,
        key="_PIN_PB6",
        value_raw="GPI",
        line=10,
        value_col=12,
        value_len=3,
    )

    def _res(rid, status):
        res = MatchResult(requirement_id=rid, status=status)
        res.proposed_change = ProposedChange(
            type=ChangeType.SET_MACRO,
            target="E1",
            old_value="GPI",
            new_value="GPO_PP",
            reason="期望 GPO_PP",
        )
        return res

    results = [
        _res("R1", CheckStatus.MISMATCH),
        _res("R2", CheckStatus.MATCH),
        _res("R3", CheckStatus.AMBIGUOUS),
    ]
    session = SimpleNamespace(
        check_result=SimpleNamespace(results=results),
        entries_by_id=lambda: {"E1": entry},
    )
    edits, skipped = ApplyUseCase().build_edits(session)
    assert [e.new_value for e in edits] == ["GPO_PP"]      # 只有 R1 被写回
    assert all(not s.startswith(("R2", "R3")) for s in skipped)


def test_settings_dialog_constructs_without_profile():
    _app()
    dlg = SettingsDialog(load_settings(), None, None)
    assert dlg.series_combo.count() >= 3
    dlg.close()


def test_settings_dialog_constructs_with_profile():
    _app()
    settings = load_settings()
    profile = profile_for_series(settings, "rtk")
    assert profile is not None
    dlg = SettingsDialog(settings, None, profile)
    assert dlg.filter_combo.count() >= 2
    dlg.close()
