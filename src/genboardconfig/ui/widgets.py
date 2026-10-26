"""自定义控件：状态统计卡、Diff 视图。"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..domain.models import STATUS_LABELS, CheckStatus

CARD_SPECS = [
    (CheckStatus.MATCH.value, "#16a34a", "#f0fdf4"),
    (CheckStatus.MISMATCH.value, "#dc2626", "#fef2f2"),
    (CheckStatus.MISSING.value, "#ea580c", "#fff7ed"),
    (CheckStatus.AMBIGUOUS.value, "#ca8a04", "#fefce8"),
    (CheckStatus.NOT_APPLICABLE.value, "#64748b", "#f8fafc"),
    (CheckStatus.UNRESOLVED.value, "#7c3aed", "#f5f3ff"),
]


class StatCards(QWidget):
    """可点击的状态统计卡片，点击即按状态筛选。"""

    status_clicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._buttons: dict[str, QPushButton] = {}
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        for status, fg, bg in CARD_SPECS:
            btn = QPushButton(self)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumWidth(96)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background:{bg}; border:1px solid {fg}33; border-radius:8px;
                    padding:8px 12px; text-align:left;
                }}
                QPushButton:hover {{ border:1px solid {fg}; }}
                QPushButton:checked {{ border:2px solid {fg}; }}
                """
            )
            btn.clicked.connect(lambda _=False, s=status: self.status_clicked.emit(s))
            self._buttons[status] = btn
            layout.addWidget(btn)
        self.set_counts({})

    def set_counts(self, counts: dict[str, int]) -> None:
        for status, (fg, _bg) in ((s, (c, None)) for s, c, _ in CARD_SPECS):
            n = counts.get(status, 0)
            label = STATUS_LABELS.get(status, status)
            self._buttons[status].setText(f"{label}\n{n}")
            self._buttons[status].setStyleSheet(
                self._buttons[status].styleSheet()
                + f"QPushButton {{ color:{fg}; font-weight:600; }}"
            )

    def clear_selection(self) -> None:
        for btn in self._buttons.values():
            btn.setChecked(False)


class DiffView(QTextEdit):
    """带颜色的 unified diff 视图。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setStyleSheet(
            """
            QTextEdit { font-family: Consolas, 'Courier New', monospace; font-size: 12px;
                        background:#0f172a; color:#cbd5e1; border:none; }
            """
        )

    def set_diff(self, diff: str, header: str = "") -> None:
        if not diff.strip():
            self.setHtml(
                "<div style='color:#64748b;padding:16px'>暂无差异。选择状态为"
                "「不一致」且可自动修改的行后点击「预览修改」。</div>"
            )
            return
        parts = [f"<div style='color:#94a3b8;padding:6px 10px'>{header}</div>"]
        for line in diff.split("\n"):
            escaped = (
                line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )
            if line.startswith("+++") or line.startswith("---"):
                color = "#e2e8f0"
            elif line.startswith("@@"):
                color = "#38bdf8"
            elif line.startswith("+"):
                color = "#4ade80"
            elif line.startswith("-"):
                color = "#f87171"
            else:
                color = "#94a3b8"
            parts.append(f"<div style='color:{color}'>{escaped or ' '}</div>")
        self.setHtml("".join(parts))

    def set_text(self, text: str) -> None:
        self.setPlainText(text)


class SidePanel(QFrame):
    """右侧详情面板。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(self)
        self.title = QLabel("详情")
        self.title.setStyleSheet("font-weight:600;font-size:14px;")
        self.body = QTextEdit()
        self.body.setReadOnly(True)
        self.body.setStyleSheet(
            "QTextEdit{background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;"
            "font-family:Consolas,monospace;font-size:12px;}"
        )
        layout.addWidget(self.title)
        layout.addWidget(self.body)

    def show_result(self, html_body: str) -> None:
        self.body.setHtml(html_body)

    @staticmethod
    def mono(text: str) -> str:
        safe = (
            str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        return f"<code>{safe}</code>"
