"""全局样式。"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

STYLE_FILE = Path(__file__).resolve().parent.parent / "resources" / "style.qss"

CJK_FONTS = ["Microsoft YaHei UI", "Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "SimSun"]


def apply_style(app: QApplication) -> None:
    font = QFont()
    for name in CJK_FONTS:
        font.setFamily(name)
        if font.exactMatch():
            break
    font.setPointSize(9)
    app.setFont(font)
    if STYLE_FILE.exists():
        app.setStyleSheet(STYLE_FILE.read_text(encoding="utf-8"))
