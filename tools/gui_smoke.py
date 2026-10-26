"""GUI 冒烟测试：离屏构造主窗口并跑一次完整核对。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from PySide6.QtWidgets import QApplication  # noqa: E402

from genboardconfig.ui.main_window import MainWindow  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402
from genboardconfig.app.service_factory import build_check_usecase  # noqa: E402
from sample_gen import build_c, build_excel  # noqa: E402


def main() -> int:
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="gbc_gui_"))
    samples = ROOT / "samples"
    excel_src = sorted(samples.glob("*.xlsx"))
    c_src = sorted(samples.glob("*.h")) + sorted(samples.glob("*.c"))
    if excel_src and c_src:
        excel = excel_src[0]
        cfile = c_src[0]
    else:  # 回退到内置样例
        from sample_gen import build_c, build_excel

        excel = tmp / "gpio_table_sample.xlsx"
        cfile = tmp / "board_config_sample.c"
        build_excel(excel)
        build_c(cfile)

    app = QApplication.instance() or QApplication(sys.argv)
    apply_style(app)
    win = MainWindow()
    win.excel_edit.setText(str(excel))
    win.c_edit.setText(str(cfile))
    win._detect_profile()
    # 样例的 GPIO TYPE 列为空 → 用 Chip Section 过滤以走通完整核对链路
    if win.profile is not None:
        win.profile.apply_override(
            {"field": "chip_section", "values": ["Output", "Input"]}
        )
        win.check_usecase = build_check_usecase(win.settings, win.profile)
    win._update_actions()
    win.show()

    win.session.excel_path = str(excel)
    win.session.c_path = str(cfile)
    result = win.check_usecase.run(
        win.session, progress=lambda m, p: None, use_llm=True
    )
    win._on_check_done(result)
    print("表格行数:", win.table.model().rowCount())
    print("档案模式:", win.result_model.profile_mode)
    print("状态卡:", win.stat_cards._buttons["match"].text().replace("\n", " "))

    # 选中可修改行 → 预览
    win._select_all_changeable()
    win._preview_changes()
    print("Diff 行数:", len((win.preview.diff or "").splitlines()) if win.preview else 0)

    # 导出报告
    html = win.report_usecase.export_html(
        win.session, win.preview.diff if win.preview else "", tmp / "report.html"
    )
    csv = win.report_usecase.export_csv(win.session, tmp / "report.csv")
    print("报告:", html, csv)

    # 过滤器
    win.status_combo.setCurrentIndex(1)
    print("过滤后行数:", win.table.model().rowCount())
    win.status_combo.setCurrentIndex(0)

    print("GUI 冒烟测试通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
