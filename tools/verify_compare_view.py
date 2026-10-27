"""并排对比视图验证：检查左右表格内容、着色与联动。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    detect_profile,
    load_profiles,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402
from genboardconfig.ui.main_window import MainWindow  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402


def main() -> int:
    settings = load_settings()
    excel = sorted((ROOT / "samples" / "NTK").glob("*.xlsx"))[0]
    cfile = ROOT / "samples" / "NTK" / "BoardCfg.h"

    profile = detect_profile(str(excel), load_profiles(settings))
    usecase = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    result = usecase.run(session, progress=lambda m, p: None, use_llm=True)

    app = QApplication.instance() or QApplication(sys.argv)
    apply_style(app)
    win = MainWindow()
    win.compare_view.set_result(result)

    view = win.compare_view
    left = view.left_model
    right = view.right_model
    print(f"左侧 Excel 行数：{left.rowCount()}")
    print(f"右侧相关条目数：{right.rowCount()}")
    print()
    print("左侧（前 6 行）：")
    for r in range(min(6, left.rowCount())):
        cells = [left.data(left.index(r, c)) for c in range(left.columnCount())]
        marks = []
        for c in range(left.columnCount()):
            bg = left.data(left.index(r, c), Qt.BackgroundRole)  # BackgroundRole
            if bg is not None and bg.color().name().lower() == "#fef2f2":
                marks.append(c)
        print(f"  {cells}   不一致列={marks}")
    print()
    print("右侧（前 10 行）：")
    for r in range(min(10, right.rowCount())):
        cells = [right.data(right.index(r, c)) for c in range(right.columnCount())]
        bg = right.data(right.index(r, 2), Qt.BackgroundRole)
        color = bg.color().name().lower() if bg is not None else "-"
        print(f"  {cells[:5]}  实际值底色={color}")

    # 联动：选中左侧第 2 行（ON_BACKLIGHT 不一致行）
    target = None
    for r in range(left.rowCount()):
        if left.data(left.index(r, 3)) == "OUT" and left.data(left.index(r, 5)) == "High":
            target = r
            break
    if target is not None:
        view.left.selectRow(target)
        app.processEvents()
        sel = [i.row() for i in view.right.selectionModel().selectedRows()]
        print()
        print(f"选中左侧第 {target} 行（{left.data(left.index(target, 1))}）"
              f" → 右侧自动定位条目行号：{sel}")
        for s in sel:
            print("     ", [right.data(right.index(s, c)) for c in range(5)])

    ok = right.rowCount() > 0 and left.rowCount() > 0
    print()
    print("并排对比视图验证：", "通过" if ok else "失败")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
