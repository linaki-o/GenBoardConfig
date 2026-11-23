"""选中行样式：不得用底色覆盖状态列的红/绿配色，只用加重边框标示。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QPA_FONTDIR", r"C:\Windows\Fonts")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt  # noqa: E402
from PySide6.QtGui import QBrush, QColor  # noqa: E402
from PySide6.QtWidgets import QApplication, QTableView  # noqa: E402

from genboardconfig.ui.delegates import RowBorderDelegate  # noqa: E402
from genboardconfig.ui.style import apply_style  # noqa: E402

MISMATCH_BG = "#fee2e2"
MATCH_BG = "#dcfce7"


class _Model(QAbstractTableModel):
    """两行：一致 / 不一致；状态列带模型底色与文字色。"""

    def rowCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return 2

    def columnCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return ["一致", "不一致", "网络名"][index.column()]
        if role == Qt.BackgroundRole and index.column() == 0:
            return QBrush(QColor(MISMATCH_BG if index.row() else MATCH_BG))
        if role == Qt.ForegroundRole and index.column() == 0:
            return QBrush(QColor("#dc2626" if index.row() else "#16a34a"))
        return None


def _app() -> QApplication:
    app = QApplication.instance() or QApplication([])
    apply_style(app)
    return app


def _table() -> QTableView:
    view = QTableView()
    view.setModel(_Model())
    view.setSelectionBehavior(QTableView.SelectRows)
    view.setItemDelegate(RowBorderDelegate(view))
    view.resize(360, 120)
    view.show()
    QApplication.instance().processEvents()
    return view


def _cell_color(view: QTableView, row: int, col: int) -> QColor:
    img = view.viewport().grab().toImage()
    rect = view.visualRect(view.model().index(row, col))
    return QColor(img.pixel(rect.topLeft().x() + 3, rect.topLeft().y() + 3))


def test_selected_row_keeps_model_background():
    """选中行不得被系统高亮蓝覆盖，状态列底色保持模型给出的颜色。"""
    _app()
    view = _table()
    view.selectRow(1)
    QApplication.instance().processEvents()
    assert _cell_color(view, 1, 0).name() == MISMATCH_BG


def test_selected_row_keeps_model_foreground():
    """状态列文字色也必须保持模型给出的红/绿（文字有抗锯齿，按色调判定）。"""
    _app()
    view = _table()
    view.selectRow(1)
    QApplication.instance().processEvents()
    img = view.viewport().grab().toImage()
    rect = view.visualRect(view.model().index(1, 0))
    # 只看单元格内部（排除描边像素）
    inner = rect.adjusted(3, 3, -3, -3)
    reddish = 0
    blueish = 0
    for x in range(inner.left(), inner.right()):
        for y in range(inner.top(), inner.bottom()):
            c = QColor(img.pixel(x, y))
            if c.red() > 140 and c.green() < 110 and c.blue() < 110:
                reddish += 1
            if c.blue() > 140 and c.red() < 110 and c.green() < 130:
                blueish += 1
    assert reddish > 0, "状态列的红色文字丢失"
    assert blueish == 0, "状态列出现了系统高亮蓝"


def test_uncolored_cells_are_not_highlighted_blue():
    """没有模型底色的单元格不得变成系统高亮蓝。"""
    _app()
    view = _table()
    view.selectRow(1)
    QApplication.instance().processEvents()
    assert _cell_color(view, 1, 2).name() != "#308cc6"


def test_selected_row_draws_border():
    """选中行应出现加重边框（深蓝色描边）。"""
    _app()
    view = _table()
    view.selectRow(1)
    QApplication.instance().processEvents()
    img = view.viewport().grab().toImage()
    rect = view.visualRect(view.model().index(1, 0))
    blue = 0
    for x in range(rect.left(), rect.right()):
        for y in (rect.top() + 1, rect.bottom() - 1):
            c = QColor(img.pixel(x, y))
            if c.blue() > 120 and c.red() < 90 and c.green() < 90:
                blue += 1
    assert blue > 0, "选中行未绘制边框"
