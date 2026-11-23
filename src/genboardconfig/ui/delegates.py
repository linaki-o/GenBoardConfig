"""表格绘制委托：选中行只加重边框，不覆盖模型的状态配色。

Qt 默认会给选中单元格绘制系统高亮色（蓝），把模型通过 BackgroundRole /
ForegroundRole 标出的红、绿状态色整片盖掉，干扰判读。

这里的做法是：绘制时先去掉选中态（``State_Selected``），让单元格按模型配色
正常渲染；模型没给底色的单元格改用该行原本的底色（白 / 交替浅灰），避免落到
系统高亮蓝；最后自行给整行描一圈粗边框表示选中。
"""

from __future__ import annotations

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QBrush, QColor, QPalette, QPen
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
)

SELECT_BORDER = "#1d4ed8"
BORDER_WIDTH = 2


class RowBorderDelegate(QStyledItemDelegate):
    """选中行以加重边框标示，而不是用底色覆盖状态色。"""

    def paint(self, painter, option, index) -> None:
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        selected = bool(option.state & QStyle.State_Selected)
        # initStyleOption 会用控件状态覆盖 opt.state，所以必须在其后再去掉选中态：
        # QSS 的 ::item:selected 与系统高亮色都不会生效，单元格保留模型配色
        opt.state &= ~QStyle.State_Selected
        if selected and opt.backgroundBrush.style() == Qt.NoBrush:
            # 模型未给底色 → 用该行本来的底色，避免落到系统高亮蓝
            opt.backgroundBrush = self._row_brush(option, index)
        widget = opt.widget
        style = widget.style() if widget is not None else QApplication.style()
        style.drawControl(QStyle.CE_ItemViewItem, opt, painter, widget)

        if not selected:
            return
        view = self._view(option)
        rect = self._row_rect(view, index) if view is not None else option.rect
        if not rect.isValid():
            return
        painter.save()
        pen = QPen(QColor(SELECT_BORDER))
        pen.setWidth(BORDER_WIDTH)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(rect.adjusted(1, 1, -2, -2))
        painter.restore()

    # ------------------------------------------------------------------
    def _view(self, option) -> QAbstractItemView | None:
        """取宿主表格视图（委托的父对象即视图）。"""
        for candidate in (
            self.parent(),
            getattr(option.widget, "parent", lambda: None)(),
            option.widget,
        ):
            if isinstance(candidate, QAbstractItemView):
                return candidate
        return None

    def _row_brush(self, option, index) -> QBrush:
        """该行本来的底色：交替行取浅灰，其余取白。"""
        view = self._view(option)
        if view is None:
            return QBrush(QColor("#ffffff"))
        palette = view.palette()
        if view.alternatingRowColors() and (index.row() & 1):
            return QBrush(palette.color(QPalette.AlternateBase))
        return QBrush(palette.color(QPalette.Base))

    def _row_rect(self, view: QAbstractItemView, index) -> QRect:
        """选中行在视口中的整体矩形：从首个可见列到末个可见列。"""
        rect = view.visualRect(index)
        model = view.model()
        if model is None:
            return rect
        header = view.horizontalHeader()
        width = max(1, view.viewport().width())
        first = header.visualIndexAt(1) if header is not None else 0
        last = header.visualIndexAt(width - 1) if header is not None else -1
        if first < 0:
            first = 0
        if last < 0:
            last = model.columnCount() - 1
        left_rect = view.visualRect(model.index(index.row(), first))
        right_rect = view.visualRect(model.index(index.row(), last))
        if not left_rect.isValid() or not right_rect.isValid():
            return rect
        return QRect(
            left_rect.left(),
            rect.top(),
            right_rect.right() - left_rect.left() + 1,
            rect.height(),
        )
