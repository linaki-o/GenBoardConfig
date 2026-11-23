"""SOP 截图生成：为 docs/sop/*.png 生成带正确中文字体的界面截图。

用法：python tools/sop_screenshot.py
说明：Qt 的 offscreen 平台默认不加载系统字体，中文会渲染成方块；
      这里显式指定 QT_QPA_FONTDIR 指向 Windows 字体目录即可正常显示。
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QPA_FONTDIR", r"C:\Windows\Fonts")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QTimer  # noqa: E402
from PySide6.QtWidgets import QApplication, QMessageBox  # noqa: E402

from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    detect_series,
    profile_for_series,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402
from genboardconfig.ui.main_window import MainWindow  # noqa: E402
from genboardconfig.ui.settings_dialog import SettingsDialog  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402

OUT = ROOT / "docs" / "sop"
OUT.mkdir(parents=True, exist_ok=True)


def _sample_paths(series: str) -> tuple[Path, Path]:
    folder = ROOT / "samples" / series.upper()
    excels = sorted(folder.glob("*.xlsx")) + sorted(folder.glob("*.XLSX"))
    headers = sorted(folder.glob("*.h")) + sorted(folder.glob("*.c"))
    return excels[0], headers[0]


def _build_window(series: str) -> tuple[MainWindow, Path, Path]:
    """建窗口、选文件、跑一次核对（不用大模型）。"""
    settings = load_settings()
    excel, cfile = _sample_paths(series)
    win = MainWindow()
    win.resize(1680, 980)
    win.show()

    profile = profile_for_series(settings, detect_series(cfile))
    win.excel_edit.setText(str(excel))
    win.c_edit.setText(str(cfile))
    win.profile = profile
    win.check_usecase = build_check_usecase(settings, profile)
    win.lbl_profile.setText(profile.name)
    win._update_actions()

    win.session.excel_path = str(excel)
    win.session.c_path = str(cfile)
    result = win.check_usecase.run(
        win.session, progress=lambda m, p: None, use_llm=False
    )
    win._on_check_done(result)
    return win, excel, cfile


def _select_first_mismatch(win: MainWindow) -> None:
    """在核对明细表里选中第一条「不一致」，让右侧详情面板有内容。"""
    for i, row in enumerate(win.result_model.rows()):
        if row.result.status.value == "mismatch":
            src = win.result_model.index(i, 0)
            idx = win.proxy.mapFromSource(src)
            win.table.selectRow(idx.row())
            win.table.scrollTo(idx)
            return


def _shot(widget, name: str) -> None:
    """保存到 docs/sop/（SOP 用），并同步到 docs/ 下的 README 旧文件名。"""
    path = OUT / name
    widget.grab().save(str(path))
    print(f"已保存：{path}")
    legacy = {
        "01_main_detail.png": "screenshot_main.png",
        "02_diff_preview.png": "screenshot_diff.png",
        "03_compare_view.png": "screenshot_compare.png",
        "06_compare_view_rtk.png": "screenshot_compare_rtk.png",
    }.get(name)
    if legacy:
        widget.grab().save(str(ROOT / "docs" / legacy))
        print(f"已同步：docs/{legacy}")


def main() -> int:
    app = QApplication.instance() or QApplication(sys.argv)
    apply_style(app)
    for nm in ("information", "warning", "critical", "question"):
        setattr(QMessageBox, nm, staticmethod(lambda *a, **k: QMessageBox.Ok))

    # —— 1) 主界面（核对明细）——
    win, _excel, _c = _build_window("ntk")
    _select_first_mismatch(win)
    win.tabs.setCurrentIndex(0)
    app.processEvents()
    _shot(win, "01_main_detail.png")

    # —— 2) 差异预览 ——
    win._select_all_changeable()
    win._preview_changes()
    win.tabs.setCurrentIndex(1)
    app.processEvents()
    _shot(win, "02_diff_preview.png")

    # —— 3) 并排对比 ——
    win.tabs.setCurrentIndex(2)
    app.processEvents()
    for r in range(win.compare_view.left_model.rowCount()):
        last = len(win.compare_view.left_model._headers) - 2
        if win.compare_view.left_model.data(
            win.compare_view.left_model.index(r, last)
        ) == "mismatch":
            win.compare_view.left.selectRow(r)
            break
    app.processEvents()
    _shot(win, "03_compare_view.png")

    # —— 4) 运行日志 ——
    win.tabs.setCurrentIndex(3)
    app.processEvents()
    _shot(win, "04_run_log.png")
    win.close()

    # —— 5) 设置对话框 ——
    settings = load_settings()
    profile = profile_for_series(settings, "ntk")
    dlg = SettingsDialog(settings, None, profile)
    dlg.resize(560, 720)
    dlg.show()
    app.processEvents()
    _shot(dlg, "05_settings.png")
    dlg.close()

    # —— 6) RTK 并排对比 ——
    win2, _e2, _c2 = _build_window("rtk")
    win2.tabs.setCurrentIndex(2)
    app.processEvents()
    for r in range(win2.compare_view.left_model.rowCount()):
        last = len(win2.compare_view.left_model._headers) - 2
        if win2.compare_view.left_model.data(
            win2.compare_view.left_model.index(r, last)
        ) == "mismatch":
            win2.compare_view.left.selectRow(r)
            break
    app.processEvents()
    _shot(win2, "06_compare_view_rtk.png")
    win2.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
