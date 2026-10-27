"""离屏截图：渲染主窗口并保存 PNG。

用法：python tools/screenshot.py [ntk|rtk]
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QTimer  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    detect_series,
    profile_for_series,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402
from genboardconfig.ui.main_window import MainWindow  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402

SERIES = (sys.argv[1] if len(sys.argv) > 1 else "ntk").lower()


def _sample_paths(series: str) -> tuple[Path, Path]:
    folder = ROOT / "samples" / series.upper()
    excels = sorted(folder.glob("*.xlsx")) + sorted(folder.glob("*.XLSX"))
    headers = sorted(folder.glob("*.h")) + sorted(folder.glob("*.c"))
    return excels[0], headers[0]


def main() -> int:
    suffix = "" if SERIES == "ntk" else f"_{SERIES}"
    out = ROOT / "docs" / f"screenshot_compare{suffix}.png"
    app = QApplication.instance() or QApplication(sys.argv)
    apply_style(app)
    win = MainWindow()
    win.resize(1600, 960)
    win.show()

    excel, cfile = _sample_paths(SERIES)
    settings = load_settings()
    series = detect_series(cfile)
    profile = profile_for_series(settings, series)
    win.excel_edit.setText(str(excel))
    win.c_edit.setText(str(cfile))
    win.profile = profile
    win.check_usecase = build_check_usecase(settings, profile)
    win.lbl_profile.setText(profile.name)
    win._update_actions()

    win.session.excel_path = str(excel)
    win.session.c_path = str(cfile)
    result = win.check_usecase.run(
        win.session, progress=lambda m, p: None, use_llm=True
    )
    win._on_check_done(result)
    win._select_all_changeable()
    win._preview_changes()

    def grab():
        win.tabs.setCurrentIndex(2)
        app.processEvents()
        view = win.compare_view
        for r in range(view.left_model.rowCount()):
            if view.left_model.data(view.left_model.index(r, len(view.left_model._headers) - 2)) == "mismatch":
                view.left.selectRow(r)
                break
        app.processEvents()
        win.grab().save(str(out))
        print(f"已保存截图：{out}")
        app.quit()

    QTimer.singleShot(600, grab)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
