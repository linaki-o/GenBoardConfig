"""UI 构造冒烟：确保各对话框/主窗口在离屏环境下能正常创建。

这类测试的价值：像「设置对话框缺 import」这类只在点击时才暴露的错误，
在这里就能被 pytest 抓到。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.app.service_factory import profile_for_series  # noqa: E402
from genboardconfig.infra.settings import load_settings  # noqa: E402
from genboardconfig.ui.main_window import MainWindow  # noqa: E402
from genboardconfig.ui.settings_dialog import SettingsDialog  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402


def _app() -> QApplication:
    app = QApplication.instance() or QApplication([])
    apply_style(app)
    return app


def test_main_window_constructs():
    _app()
    win = MainWindow()
    assert win.tabs.count() >= 4
    assert win.btn_check is not None
    win.close()


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
