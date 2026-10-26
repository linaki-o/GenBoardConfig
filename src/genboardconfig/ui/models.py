"""表格模型：核对结果（通用模式 / 档案模式）、Excel 原始行、C 配置条目。"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QBrush, QColor, QFont

from ..domain.models import (
    STATUS_LABELS,
    AttributeResult,
    CheckResult,
    CheckStatus,
    ConfigEntry,
    GPIORequirement,
)

STATUS_COLORS = {
    CheckStatus.MATCH.value: "#16a34a",
    CheckStatus.MISMATCH.value: "#dc2626",
    CheckStatus.MISSING.value: "#ea580c",
    CheckStatus.AMBIGUOUS.value: "#ca8a04",
    CheckStatus.NOT_APPLICABLE.value: "#64748b",
    CheckStatus.UNRESOLVED.value: "#7c3aed",
}
STATUS_BG = {
    CheckStatus.MATCH.value: "#f0fdf4",
    CheckStatus.MISMATCH.value: "#fef2f2",
    CheckStatus.MISSING.value: "#fff7ed",
    CheckStatus.AMBIGUOUS.value: "#fefce8",
    CheckStatus.NOT_APPLICABLE.value: "#f8fafc",
    CheckStatus.UNRESOLVED.value: "#f5f3ff",
}

GENERIC_HEADERS = [
    "应用", "状态", "Sheet", "行", "管脚", "GPIO", "功能",
    "配置项", "期望值", "当前值", "置信度", "来源", "依据", "说明",
]
PROFILE_HEADERS = ["应用", "状态", "网络名", "引脚", "占用信号"]


class ResultTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows: list[Any] = []
        self._result: CheckResult | None = None
        self._profile_mode = False
        self._attr_labels: list[str] = []
        self._headers = list(GENERIC_HEADERS)

    # ---------- Qt 接口 ----------
    def rowCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):  # noqa: N802
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]
        return section + 1

    def data(self, index: QModelIndex, role=Qt.DisplayRole):  # noqa: N802
        if not index.isValid() or not self._rows:
            return None
        row = self._rows[index.row()]
        res = row.result
        req = row.req
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return Qt.Checked if res.selected else Qt.Unchecked
            return self._display(row, col)
        if role == Qt.TextAlignmentRole:
            if col in (0, 3) or (self._profile_mode and col == 1):
                return int(Qt.AlignCenter)
            return int(Qt.AlignLeft | Qt.AlignVCenter)
        if role == Qt.ForegroundRole:
            if col == 1:
                return QBrush(QColor(STATUS_COLORS.get(res.status.value, "#0f172a")))
            if self._profile_mode and self._attr_col_start <= col < self._attr_col_end:
                attr = self._attr_at(row, col)
                if attr is not None and attr.status == CheckStatus.MISMATCH.value:
                    return QBrush(QColor("#dc2626"))
                if attr is not None and attr.status == CheckStatus.AMBIGUOUS.value:
                    return QBrush(QColor("#ca8a04"))
            elif not self._profile_mode and col == 9 and res.status == CheckStatus.MISMATCH.value:
                return QBrush(QColor("#dc2626"))
        if role == Qt.BackgroundRole and col == 1:
            return QBrush(QColor(STATUS_BG.get(res.status.value, "#ffffff")))
        if role == Qt.FontRole and (col == 4 if self._profile_mode else col == 7):
            return QFont("Consolas")
        if role == Qt.ToolTipRole:
            return self._tooltip(row)
        return None

    def flags(self, index: QModelIndex):  # noqa: N802
        if not index.isValid():
            return Qt.NoItemFlags
        base = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 0:
            return base | Qt.ItemIsUserCheckable
        return base

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):  # noqa: N802
        if not index.isValid() or role != Qt.CheckStateRole or index.column() != 0:
            return False
        res = self._rows[index.row()].result
        res.selected = Qt.CheckState(value) == Qt.Checked
        self.dataChanged.emit(index, index, [Qt.CheckStateRole])
        return True

    # ---------- 数据 ----------
    def set_result(self, result: CheckResult | None) -> None:
        self.beginResetModel()
        self._result = result
        self._rows = []
        self._profile_mode = False
        self._attr_labels = []
        if result is not None:
            reqs = {r.id: r for r in result.requirements}
            for res in result.results:
                self._rows.append(_Row(res, reqs.get(res.requirement_id)))
            if self._rows and self._rows[0].result.attribute_results:
                self._profile_mode = True
                self._attr_labels = [
                    a.label for a in self._rows[0].result.attribute_results
                ]
                self._headers = PROFILE_HEADERS + self._attr_labels + ["说明"]
        if not self._profile_mode:
            self._headers = list(GENERIC_HEADERS)
        self.endResetModel()

    def rows(self) -> list[Any]:
        return list(self._rows)

    def row_at(self, index: QModelIndex):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        return self._rows[index.row()]

    def update_row(self, row: int) -> None:
        if 0 <= row < len(self._rows):
            self.dataChanged.emit(
                self.index(row, 0), self.index(row, len(self._headers) - 1)
            )

    @property
    def profile_mode(self) -> bool:
        return self._profile_mode

    @property
    def _attr_col_start(self) -> int:
        return len(PROFILE_HEADERS)

    @property
    def _attr_col_end(self) -> int:
        return len(PROFILE_HEADERS) + len(self._attr_labels)

    @staticmethod
    def _attr_at(row, col: int) -> AttributeResult | None:
        if not row.result.attribute_results:
            return None
        idx = col - len(PROFILE_HEADERS)
        if 0 <= idx < len(row.result.attribute_results):
            return row.result.attribute_results[idx]
        return None

    # ---------- 展示 ----------
    def _display(self, row, col: int):
        res = row.result
        req = row.req
        if self._profile_mode:
            if col == 1:
                return STATUS_LABELS.get(res.status.value, res.status.value)
            if col == 2:
                return req.net_name or req.config_key if req else ""
            if col == 3:
                return req.pin_name_raw if req else ""
            if col == 4:
                return "、".join(res.signals[:3]) or "-"
            if col == len(self._headers) - 1:
                return res.notes
            attr = self._attr_at(row, col)
            if attr is None:
                return ""
            if not attr.checkable:
                return f"({attr.expected or '-'})"
            if attr.status == CheckStatus.MATCH.value:
                return attr.actual or attr.expected
            if not attr.actual:
                return f"缺失 ← {attr.expected}"
            return f"{attr.expected} → {attr.actual}"

        result = res
        if col == 1:
            return STATUS_LABELS.get(result.status.value, result.status.value)
        if col == 2:
            return req.sheet if req else ""
        if col == 3:
            return req.row_no if req else ""
        if col == 4:
            return req.pin_name_raw if req else ""
        if col == 5:
            return req.gpio_num if req and req.gpio_num is not None else ""
        if col == 6:
            return req.function_name if req else ""
        if col == 7:
            return req.config_key if req else ""
        if col == 8:
            return result.expected_value
        if col == 9:
            return result.current_value
        if col == 10:
            return f"{result.confidence:.2f}"
        if col == 11:
            return {"deterministic": "规则", "llm": "模型", "human": "人工"}.get(
                result.source.value, result.source.value
            )
        if col == 12:
            return f"L{result.evidence[0].line}" if result.evidence else ""
        if col == 13:
            return result.notes
        return ""

    def _tooltip(self, row) -> str:
        res = row.result
        req = row.req
        lines = []
        if req is not None:
            lines.append(f"{req.sheet} 第 {req.row_no} 行")
            if req.remark:
                lines.append(f"备注：{req.remark}")
        if res.notes:
            lines.append(f"说明：{res.notes}")
        for attr in res.attribute_results:
            if attr.status not in {CheckStatus.MATCH.value, CheckStatus.NOT_APPLICABLE.value}:
                lines.append(
                    f"{attr.label}：期望 {attr.expected} / 实际 {attr.actual}（{attr.status.value}）"
                )
        for e in res.evidence:
            lines.append(f"依据 L{e.line}: {e.snippet}")
        return "\n".join(lines)


class _Row:
    __slots__ = ("result", "req")

    def __init__(self, result, req):
        self.result = result
        self.req = req


class GenericTableModel(QAbstractTableModel):
    """通用二维表模型，用于 Excel 原始行与 C 条目。"""

    def __init__(self, headers: list[str], rows: list[list[Any]], parent=None):
        super().__init__(parent)
        self._headers = headers
        self._rows = rows

    def rowCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:  # noqa: N802
        return len(self._headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):  # noqa: N802
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._headers[section]
        return section + 1

    def data(self, index: QModelIndex, role=Qt.DisplayRole):  # noqa: N802
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._rows[index.row()][index.column()]
        if role == Qt.TextAlignmentRole and index.column() == 0:
            return int(Qt.AlignCenter)
        return None

    def set_rows(self, headers: list[str], rows: list[list[Any]]) -> None:
        self.beginResetModel()
        self._headers = headers
        self._rows = rows
        self.endResetModel()


def excel_model(result: CheckResult) -> GenericTableModel:
    if not result.requirements:
        return GenericTableModel(["(无数据)"], [])
    headers = ["ID", "Sheet", "行", "管脚", "网络名", "GPIO", "功能", "配置项", "期望值", "备注"]
    rows = [
        [
            r.id, r.sheet, r.row_no, r.pin_name_raw, r.net_name or r.config_key,
            r.gpio_num, r.function_name, r.config_key, r.expected_value, r.remark,
        ]
        for r in result.requirements
    ]
    return GenericTableModel(headers, rows)


def entries_model(result: CheckResult) -> GenericTableModel:
    headers = ["ID", "类型", "键", "值", "归属", "行", "条件", "原文"]
    rows = [
        [
            e.id, e.kind.value, e.key, e.value_raw, e.owner, e.line,
            e.condition, e.raw_text.strip(),
        ]
        for e in result.entries
    ]
    return GenericTableModel(headers, rows)


def entry_tooltip(entry: ConfigEntry) -> str:
    return f"{entry.key} = {entry.value_raw}\nL{entry.line}  {entry.raw_text.strip()}"
