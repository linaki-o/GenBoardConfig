"""离屏截图：渲染主窗口并保存 PNG，便于无显示环境检查界面。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import QTimer  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.ui.main_window import MainWindow  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402
from genboardconfig.app.service_factory import build_check_usecase  # noqa: E402


def main() -> int:
    out = ROOT / "docs" / "screenshot_main.png"
    app = QApplication.instance() or QApplication(sys.argv)
    apply_style(app)
    win = MainWindow()
    win.resize(1600, 960)
    win.show()

    excels = sorted((ROOT / "samples").glob("*.xlsx"))
    headers = sorted((ROOT / "samples").glob("*.h")) + sorted((ROOT / "samples").glob("*.c"))
    if excels and headers:
        excel = excels[0]
        cfile = headers[0]
        win.excel_edit.setText(str(excel))
        win.c_edit.setText(str(cfile))
        win._detect_profile()
        win._update_actions()
        win.session.excel_path = str(excel)
        win.session.c_path = str(cfile)
        result = win.check_usecase.run(
            win.session, progress=lambda m, p: None, use_llm=True
        )
        win._on_check_done(result)
        win._select_all_changeable()
        win._preview_changes()

    shots: list[tuple[str, int]] = [
        (str(ROOT / "docs" / "screenshot_main.png"), 0),
        (str(ROOT / "docs" / "screenshot_compare.png"), 2),
        (str(ROOT / "docs" / "screenshot_diff.png"), 1),
    ]

    def grab():
        for path, tab in shots:
            win.tabs.setCurrentIndex(tab)
            app.processEvents()
            if tab == 2:
                # 选中一个不一致的行，展示联动效果
                view = win.compare_view
                for r in range(view.left_model.rowCount()):
                    if view.left_model.data(view.left_model.index(r, 6)) == "mismatch":
                        view.left.selectRow(r)
                        break
                app.processEvents()
            win.grab().save(path)
            print(f"已保存截图：{path}")
        app.quit()

    QTimer.singleShot(600, grab)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
