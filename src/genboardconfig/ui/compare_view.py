"""并排对比视图：左侧 Excel 数据、右侧板级配置条目，按核对关系着色联动。"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ..domain.models import CheckResult, CheckStatus

C_BG = "#f1f5f9"
C_OK_BG = "#f0fdf4"
C_OK_FG = "#15803d"
C_BAD_BG = "#fef2f2"
C_BAD_FG = "#b91c1c"
C_NA_BG = "#f8fafc"
C_LINK_BG = "#fffbeb"
C_LINK_FG = "#b45309"
C_GROUP_BG = "#f1f5f9"      # 分组条带（同一 Excel 行的一组条目）

# 结论严重度：同一条目被多个属性引用时取最严重的一条
VERDICT_SEVERITY = {
    "一致": 0,
    "不适用": 1,
    "未解析": 2,
    "需人工确认": 3,
    "缺失": 4,
    "不一致": 5,
}


class _HighlightModel(QAbstractTableModel):
    """带单元格/行着色的表格模型基类。"""

    def __init__(self, headers: list[str]):
        super().__init__()
        self._headers = headers
        self._rows: list[list[Any]] = []
        self._cell_bg: dict[tuple[int, int], QColor] = {}
        self._cell_fg: dict[tuple[int, int], QColor] = {}
        self._row_bg: dict[int, QColor] = {}
        self._bold: set[tuple[int, int]] = set()

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

    def data(self, index, role=Qt.DisplayRole):  # noqa: N802
        if not index.isValid():
            return None
        r, c = index.row(), index.column()
        if role == Qt.DisplayRole:
            return self._rows[r][c] if c < len(self._rows[r]) else ""
        if role == Qt.BackgroundRole:
            color = self._cell_bg.get((r, c)) or self._row_bg.get(r)
            return QBrush(color) if color else None
        if role == Qt.ForegroundRole:
            color = self._cell_fg.get((r, c))
            return QBrush(color) if color else None
        if role == Qt.FontRole and (r, c) in self._bold:
            font = QFont()
            font.setBold(True)
            return font
        if role == Qt.TextAlignmentRole and c == 0:
            return int(Qt.AlignCenter)
        return None

    def set_highlights(
        self,
        cell_bg: dict[tuple[int, int], QColor] | None = None,
        cell_fg: dict[tuple[int, int], QColor] | None = None,
        row_bg: dict[int, QColor] | None = None,
        bold: set[tuple[int, int]] | None = None,
    ) -> None:
        self._cell_bg = cell_bg or {}
        self._cell_fg = cell_fg or {}
        self._row_bg = row_bg or {}
        self._bold = bold or {}

    def _reset(self, headers: list[str] | None = None) -> None:
        if headers:
            self._headers = headers
        self._rows = []
        self._cell_bg.clear()
        self._cell_fg.clear()
        self._row_bg.clear()
        self._bold.clear()


class ExcelCompareModel(_HighlightModel):
    """左侧：Excel 原始行 + 逐属性核对结论（属性列按档案自适应）。"""

    def __init__(self):
        super().__init__([])
        self._attr_names: list[str] = []
        self._attr_labels: list[str] = []

    def set_result(self, result: CheckResult) -> None:
        self.beginResetModel()
        self._reset(self._build_headers(result))
        self._attr_names, self._attr_labels = self._collect_attrs(result)

        reqs = result.requirements
        res_by_id = {r.requirement_id: r for r in result.results}
        for i, req in enumerate(reqs):
            res = res_by_id.get(req.id)
            attrs = {a.name: a for a in (res.attribute_results if res else [])}
            cells = [req.row_no, req.pin_name_raw, req.net_name or req.config_key]
            for name, col in zip(self._attr_names, self._attr_cols()):
                attr = attrs.get(name)
                if attr is None:
                    cells.append("")
                    continue
                if not attr.checkable:
                    cells.append(attr.expected or "-")
                    self._cell_bg[(i, col)] = QColor(C_NA_BG)
                    continue
                same = attr.status == CheckStatus.MATCH.value
                cells.append(attr.expected)
                self._cell_bg[(i, col)] = QColor(C_OK_BG if same else C_BAD_BG)
                self._cell_fg[(i, col)] = QColor(C_OK_FG if same else C_BAD_FG)
                if not same:
                    self._bold.add((i, col))
            status = res.status.value if res else "-"
            cells.append(status)
            cells.append(res.notes if res else "")
            status_col = len(self._headers) - 2
            if res is not None:
                if res.status == CheckStatus.MISMATCH.value:
                    self._cell_bg[(i, status_col)] = QColor(C_BAD_BG)
                    self._cell_fg[(i, status_col)] = QColor(C_BAD_FG)
                    self._bold.add((i, status_col))
                elif res.status == CheckStatus.AMBIGUOUS.value:
                    self._cell_bg[(i, status_col)] = QColor(C_LINK_BG)
                    self._cell_fg[(i, status_col)] = QColor(C_LINK_FG)
                    self._bold.add((i, status_col))
                elif res.status == CheckStatus.MATCH.value:
                    self._cell_bg[(i, status_col)] = QColor(C_OK_BG)
                    self._cell_fg[(i, status_col)] = QColor(C_OK_FG)
            # 与右表一致的分组条带（按 Excel 行交替）
            if i % 2 == 1:
                self._row_bg[i] = QColor(C_GROUP_BG)
            self._rows.append(cells)
        self.endResetModel()

    def _collect_attrs(self, result: CheckResult) -> tuple[list[str], list[str]]:
        names: list[str] = []
        labels: list[str] = []
        for res in result.results:
            for attr in res.attribute_results:
                if attr.name in names:
                    continue
                names.append(attr.name)
                labels.append(attr.label or attr.name)
        return names, labels

    def _build_headers(self, result: CheckResult) -> list[str]:
        names, labels = self._collect_attrs(result)
        return ["行", "管脚", "网络名"] + labels + ["状态", "差异说明"]

    def _attr_cols(self) -> list[int]:
        return list(range(3, 3 + len(self._attr_names)))


class CCompareModel(_HighlightModel):
    """右侧：板级配置条目。

    每行带「Excel 行」锚点列 —— 同一 Excel 行的 N 个条目（NTK 为 DIR/PP/OUT 三条）
    连续排列且锚点相同，配合分组条带即可与左表逐行对应。
    """

    HEADERS = ["Excel 行", "配置行", "键", "期望值", "实际值", "判定", "定义原文"]

    def __init__(self):
        super().__init__(list(self.HEADERS))
        self._entry_ids: list[str] = []
        self._index_of: dict[str, int] = {}

    def data(self, index, role=Qt.DisplayRole):  # noqa: N802
        if role == Qt.FontRole and (index.row(), index.column()) in self._bold:
            font = QFont("Consolas")
            font.setBold(True)
            return font
        if role == Qt.TextAlignmentRole and index.column() in (0, 1, 5):
            return int(Qt.AlignCenter)
        return super().data(index, role)

    def set_entries(
        self,
        entries,
        index_of: dict[str, int],
        extra: dict[str, dict] | None = None,
        groups: dict[str, tuple[int, int]] | None = None,
    ) -> None:
        """extra: entry_id → {期望值, 判定}；groups: entry_id → (Excel 行号, 组序号)"""
        self.beginResetModel()
        self._reset(list(self.HEADERS))
        self._entry_ids = []
        self._index_of = index_of
        extra = extra or {}
        groups = groups or {}
        for entry in entries:
            info = extra.get(entry.id, {})
            excel_row, _group = groups.get(entry.id, (0, 0))
            self._rows.append(
                [
                    excel_row,
                    entry.line,
                    entry.key,
                    info.get("expected", "-"),
                    entry.value_raw,
                    info.get("verdict", "-"),
                    entry.raw_text.strip(),
                ]
            )
            self._entry_ids.append(entry.id)
        self.endResetModel()

    def row_of_entry(self, entry_id: str) -> int:
        return self._index_of.get(entry_id, -1)


class CompareView(QWidget):
    """左右并排：Excel 数据 ↔ 板级配置条目。"""

    row_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._result: CheckResult | None = None
        self._related_by_req: dict[int, list[str]] = {}
        self._all_entries = []
        self._index_of: dict[str, int] = {}
        self._syncing = False
        self._ordered_ids: list[str] = []
        self._entry_extra: dict[str, dict] = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 4, 6, 6)
        root.setSpacing(6)

        bar = QHBoxLayout()
        bar.setSpacing(10)
        bar.addWidget(QLabel("右侧范围"))
        self.scope_combo = QComboBox()
        self.scope_combo.addItem("仅核对相关的位表单元", "related")
        self.scope_combo.addItem("全部位表单元（PORT_*_DEFAULT_*）", "bit")
        self.scope_combo.addItem("全部条目", "all")
        self.scope_combo.currentIndexChanged.connect(self._refresh_right)
        bar.addWidget(self.scope_combo)

        self.sync_check = QCheckBox("选中 Excel 行时自动定位右侧条目")
        self.sync_check.setChecked(True)
        bar.addWidget(self.sync_check)

        self.legend = QLabel()
        self.legend.setStyleSheet(
            f"color:#64748b;font-size:11px;"
        )
        bar.addWidget(self.legend)
        bar.addStretch(1)
        root.addLayout(bar)

        splitter = QSplitter(Qt.Horizontal)
        self.left = QTableView()
        self.left_model = ExcelCompareModel()
        self.left.setModel(self.left_model)
        self.right = QTableView()
        self.right_model = CCompareModel()
        self.right.setModel(self.right_model)

        for table in (self.left, self.right):
            table.setAlternatingRowColors(False)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.setSelectionMode(QAbstractItemView.ExtendedSelection)
            table.verticalHeader().setVisible(False)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Interactive)
            header.setStretchLastSection(True)

        for col, width in {0: 46, 1: 130, 2: 130, 3: 96, 4: 112, 5: 104, 6: 78}.items():
            self.left.setColumnWidth(col, width)
        for col, width in {0: 64, 1: 64, 2: 210, 3: 96, 4: 78, 5: 86}.items():
            self.right.setColumnWidth(col, width)

        left_panel = self._panel("Excel 数据（HSI）", self.left)
        right_panel = self._panel("板级配置条目（BoardCfg）", self.right)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 5)
        splitter.setSizes([640, 760])
        root.addWidget(splitter, 1)

        self.left.selectionModel().selectionChanged.connect(self._on_left_selection)
        self.right.selectionModel().selectionChanged.connect(self._on_right_selection)
        self._update_legend()

    # ------------------------------------------------------------------
    @staticmethod
    def _panel(title: str, table: QTableView) -> QWidget:
        panel = QFrame()
        panel.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(6, 4, 6, 6)
        label = QLabel(title)
        label.setStyleSheet("font-weight:600;color:#334155;")
        layout.addWidget(label)
        layout.addWidget(table, 1)
        return panel

    def _update_legend(self) -> None:
        self.legend.setText(
            "<span style='background:%s;padding:1px 6px;border-radius:6px'>一致</span> "
            "<span style='background:%s;padding:1px 6px;border-radius:6px'>不一致</span> "
            "<span style='background:%s;padding:1px 6px;border-radius:6px'>需人工确认</span> "
            "<span style='background:%s;padding:1px 6px;border-radius:6px'>不参与核对</span>"
            % (C_OK_BG, C_BAD_BG, C_LINK_BG, C_NA_BG)
        )

    # ------------------------------------------------------------------
    def set_result(self, result: CheckResult | None) -> None:
        self._result = result
        if result is None:
            self.left_model.set_result(CheckResult())
            self.right_model.set_entries([], {})
            return

        self.left_model.set_result(result)

        entries = result.entries
        self._index_of = {e.id: i for i, e in enumerate(entries)}
        self._all_entries = entries

        # 收集「核对相关」的条目与逐行关联（按 Excel 行分组排序）
        ordered_ids: list[str] = []
        seen: set[str] = set()
        related_by_req: dict[int, list[str]] = {}
        req_index = {r.id: i for i, r in enumerate(result.requirements)}
        entry_extra: dict[str, dict] = {}
        entry_severity: dict[str, int] = {}
        entry_group: dict[str, tuple[int, int]] = {}
        for res in result.results:
            idx = req_index.get(res.requirement_id, -1)
            ids: list[str] = []
            excel_row = (
                result.requirements[idx].row_no
                if 0 <= idx < len(result.requirements)
                else 0
            )
            for attr in res.attribute_results:
                targets = [ev.entry_id for ev in attr.evidence]
                change = attr.change
                if change is not None and change.target:
                    targets.append(change.target)
                verdict = {
                    "match": "一致",
                    "mismatch": "不一致",
                    "ambiguous": "需人工确认",
                    "missing": "缺失",
                    "unresolved": "未解析",
                    "not_applicable": "不适用",
                }.get(attr.status.value, attr.status.value)
                severity = VERDICT_SEVERITY.get(verdict, 0)
                for eid in targets:
                    if eid not in self._index_of:
                        continue
                    if eid not in seen:
                        seen.add(eid)
                        ordered_ids.append(eid)
                    if eid not in ids:
                        ids.append(eid)
                    # 同一条目可能被多个属性引用（如方向/输出类型/功能名指向同一条
                    # #define）→ 取最严重的结论，避免被后写的属性覆盖
                    if severity >= entry_severity.get(eid, -1):
                        entry_severity[eid] = severity
                        entry_extra[eid] = {
                            "expected": attr.expected or "-",
                            "verdict": verdict,
                        }
                    # 锚点：条目属于哪个 Excel 行（第几组）
                    entry_group[eid] = (excel_row, idx)
            related_by_req[idx] = ids
        self._related_by_req = related_by_req
        self._ordered_ids = ordered_ids
        self._entry_extra = entry_extra
        self._entry_group = entry_group

        self._refresh_right()

    def _refresh_right(self) -> None:
        if self._result is None:
            return
        scope = self.scope_combo.currentData()
        entries = self._result.entries
        by_id = {e.id: e for e in entries}
        if scope == "related":
            # 按 Excel 行分组排列：同一行的 3 个条目相邻
            selected = [by_id[eid] for eid in self._ordered_ids if eid in by_id]
        elif scope == "bit":
            selected = [e for e in entries if e.table]
        else:
            selected = list(entries)

        index_of = {e.id: i for i, e in enumerate(selected)}
        self.right_model.set_entries(
            selected, index_of, self._entry_extra, self._entry_group
        )

        # 着色：不一致 → 红；一致 → 绿；同一张位表的其它位 → 淡黄（上下文）
        cell_bg: dict[tuple[int, int], QColor] = {}
        cell_fg: dict[tuple[int, int], QColor] = {}
        bold: set[tuple[int, int]] = set()
        row_bg: dict[int, QColor] = {}
        tables_of_bad: set[str] = set()

        for eid, info in self._entry_extra.items():
            r = index_of.get(eid)
            if r is None:
                continue
            bad = info.get("verdict") == "不一致"
            cell_bg[(r, 4)] = QColor(C_BAD_BG if bad else C_OK_BG)
            cell_fg[(r, 4)] = QColor(C_BAD_FG if bad else C_OK_FG)
            cell_bg[(r, 5)] = QColor(C_BAD_BG if bad else C_OK_BG)
            cell_fg[(r, 5)] = QColor(C_BAD_FG if bad else C_OK_FG)
            bold.add((r, 4))
            bold.add((r, 5))
            if bad:
                entry = by_id.get(eid)
                if entry is not None and entry.table:
                    tables_of_bad.add(entry.table)
        # 差异所在位表的其它位 → 淡黄（上下文）
        for r, entry in enumerate(selected):
            if entry.table and entry.table in tables_of_bad:
                cell_bg.setdefault((r, 2), QColor(C_LINK_BG))
        # 分组条带：同一 Excel 行的一组条目用同一底色（交替）
        last_group = None
        shade = False
        for r, entry in enumerate(selected):
            group = self._entry_group.get(entry.id, (0, -1))[1]
            if group != last_group:
                shade = not shade
                last_group = group
            if shade:
                row_bg.setdefault(r, QColor(C_GROUP_BG))
        self.right_model.set_highlights(cell_bg, cell_fg, row_bg, bold)

    # ------------------------------------------------------------------
    def _on_left_selection(self) -> None:
        if not self.sync_check.isChecked() or self._syncing:
            return
        self._syncing = True
        try:
            indexes = self.left.selectionModel().selectedRows()
            if not indexes:
                return
            row = indexes[0].row()
            ids = self._related_by_req.get(row, [])
            if not ids:
                return
            self.right.clearSelection()
            first = None
            flags = (
                self.right.selectionModel().SelectionFlag.Select
                | self.right.selectionModel().SelectionFlag.Rows
            )
            for eid in ids:
                r = self.right_model.row_of_entry(eid)
                if r < 0:
                    continue
                self.right.selectionModel().select(self.right_model.index(r, 0), flags)
                if first is None:
                    first = r
            if first is not None:
                self.right.scrollTo(self.right_model.index(first, 0))
            self.row_selected.emit(row)
        finally:
            self._syncing = False

    def _on_right_selection(self) -> None:
        if not self.sync_check.isChecked() or self._syncing:
            return
        self._syncing = True
        try:
            indexes = self.right.selectionModel().selectedRows()
            if not indexes:
                return
            row_idx = indexes[0].row()
            entry_id = (
                self.right_model._entry_ids[row_idx]
                if row_idx < len(self.right_model._entry_ids)
                else ""
            )
            for row, ids in self._related_by_req.items():
                if entry_id in ids:
                    self.left.selectionModel().clearSelection()
                    self.left.selectRow(row)
                    self.left.scrollTo(self.left_model.index(row, 0))
                    break
        finally:
            self._syncing = False
