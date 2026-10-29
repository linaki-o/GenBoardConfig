"""主窗口：文件选择 → 核对 → 审阅 → 应用。"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSortFilterProxyModel, Qt, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QSplitter,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..app.apply_usecase import ApplyOutcome, ApplyUseCase
from ..app.check_usecase import CheckUseCase
from ..app.context import Session
from ..app.report_usecase import ReportUseCase
from ..app.service_factory import (
    build_apply_usecase,
    build_check_usecase,
    detect_series,
    profile_for_series,
)
from ..domain.models import (
    STATUS_LABELS,
    ChangeType,
    CheckStatus,
    MatchResult,
    Source,
)
from ..infra.settings import Settings, load_settings
from .models import ResultTableModel, entries_model, excel_model
from .compare_view import CompareView
from .widgets import DiffView, SidePanel, StatCards
from .workers import Worker

EXCEL_FILTER = "Excel 文件 (*.xlsx *.xlsm);;所有文件 (*.*)"
C_FILTER = "C 源文件 (*.c *.h);;所有文件 (*.*)"


class _DetailRow:
    """详情面板所需的最小行结构。"""

    __slots__ = ("result", "req")

    def __init__(self, result, req):
        self.result = result
        self.req = req


class ResultFilterProxy(QSortFilterProxyModel):
    """按状态 + 关键字过滤核对结果。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.status = ""
        self.keyword = ""
        self.only_changeable = False

    def set_filters(self, status: str = "", keyword: str = "", only_changeable: bool = False) -> None:
        self.status = status
        self.keyword = keyword.strip().lower()
        self.only_changeable = only_changeable
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent) -> bool:  # noqa: N802
        model = self.sourceModel()
        if model is None:
            return True
        row = model.rows()[source_row]
        result: MatchResult = row.result
        if self.status and result.status.value != self.status:
            return False
        if self.only_changeable and result.proposed_change.type.value == "none":
            return False
        if self.keyword:
            haystack = " ".join(
                str(x)
                for x in [
                    result.expected_value,
                    result.current_value,
                    result.notes,
                    row.req.pin_name_raw if row.req else "",
                    row.req.function_name if row.req else "",
                    row.req.config_key if row.req else "",
                    row.req.sheet if row.req else "",
                ]
            ).lower()
            if self.keyword not in haystack:
                return False
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GenBoardConfig · GPIO 配置核对工具")
        self.resize(1560, 940)

        self.settings: Settings = load_settings()
        self.session = Session()
        self.profile = None
        self.check_usecase: CheckUseCase = build_check_usecase(self.settings)
        self.apply_usecase: ApplyUseCase = build_apply_usecase()
        self.report_usecase = ReportUseCase()
        self.worker: Worker | None = None
        self.preview: ApplyOutcome | None = None

        self._build_ui()
        self._build_actions()
        self._update_actions()

    # ------------------------------------------------------------------
    # UI 构建
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 8, 10, 6)
        layout.setSpacing(8)

        layout.addWidget(self._build_topbar())

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._build_center())
        splitter.setStretchFactor(0, 1)
        layout.addWidget(splitter, 1)
        self.setCentralWidget(central)

        self._build_left_dock()
        self._build_right_dock()
        self._build_statusbar()

    def _build_topbar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("topbar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(12, 8, 12, 8)
        row.setSpacing(8)

        row.addWidget(QLabel("GPIO 表"))
        self.excel_edit = QLineEdit()
        self.excel_edit.setPlaceholderText("选择 Excel GPIO 分配表 (*.xlsx)")
        self.excel_edit.setReadOnly(True)
        row.addWidget(self.excel_edit, 2)
        self.btn_excel = QPushButton("浏览…")
        self.btn_excel.clicked.connect(self._pick_excel)
        row.addWidget(self.btn_excel)

        row.addWidget(QLabel("板级配置"))
        self.c_edit = QLineEdit()
        self.c_edit.setPlaceholderText("选择板级 C 配置文件 (*.c)")
        self.c_edit.setReadOnly(True)
        row.addWidget(self.c_edit, 2)
        self.btn_c = QPushButton("浏览…")
        self.btn_c.clicked.connect(self._pick_c)
        row.addWidget(self.btn_c)

        row.addSpacing(12)
        self.btn_check = QPushButton("开始核对")
        self.btn_check.setObjectName("primaryBtn")
        self.btn_check.clicked.connect(self._start_check)
        row.addWidget(self.btn_check)

        self.btn_stop = QPushButton("停止")
        self.btn_stop.clicked.connect(self._stop)
        row.addWidget(self.btn_stop)

        self.btn_preview = QPushButton("预览修改")
        self.btn_preview.clicked.connect(self._preview_changes)
        row.addWidget(self.btn_preview)

        self.btn_apply = QPushButton("应用修改")
        self.btn_apply.setObjectName("dangerBtn")
        self.btn_apply.clicked.connect(self._apply_changes)
        row.addWidget(self.btn_apply)

        self.btn_report = QPushButton("导出报告")
        self.btn_report.clicked.connect(self._export_report)
        row.addWidget(self.btn_report)

        self.btn_settings = QPushButton("设置")
        self.btn_settings.clicked.connect(self._open_settings)
        row.addWidget(self.btn_settings)
        return bar

    def _build_center(self) -> QWidget:
        self.tabs = QTabWidget()

        # —— 核对明细 ——
        page = QWidget()
        v = QVBoxLayout(page)
        v.setContentsMargins(6, 6, 6, 6)
        bar = QHBoxLayout()
        bar.addWidget(QLabel("状态"))
        self.status_combo = QComboBox()
        self.status_combo.addItem("全部", "")
        for value, label in STATUS_LABELS.items():
            self.status_combo.addItem(label, value)
        self.status_combo.currentIndexChanged.connect(self._apply_filters)
        bar.addWidget(self.status_combo)

        bar.addWidget(QLabel("搜索"))
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("管脚 / 功能 / 配置项 / 期望值 …")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.textChanged.connect(self._apply_filters)
        bar.addWidget(self.search_edit, 2)

        self.only_changeable = QCheckBox("仅显示可自动修改")
        self.only_changeable.stateChanged.connect(self._apply_filters)
        bar.addWidget(self.only_changeable)

        self.btn_select_all = QPushButton("全选可修改")
        self.btn_select_all.clicked.connect(self._select_all_changeable)
        bar.addWidget(self.btn_select_all)

        self.btn_clear = QPushButton("清空选择")
        self.btn_clear.clicked.connect(self._clear_selection)
        bar.addWidget(self.btn_clear)
        v.addLayout(bar)

        self.result_model = ResultTableModel(self)
        self.proxy = ResultFilterProxy(self)
        self.proxy.setSourceModel(self.result_model)
        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._table_menu)
        self.table.selectionModel().selectionChanged.connect(self._on_selection)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(13, QHeaderView.Stretch)
        for col, width in {
            0: 40, 2: 70, 3: 48, 4: 110, 5: 56, 6: 90,
            7: 200, 8: 90, 9: 110, 10: 64, 11: 56, 12: 70,
        }.items():
            self.table.setColumnWidth(col, width)
        v.addWidget(self.table, 1)
        self.tabs.addTab(page, "核对明细")

        # —— 差异预览 ——
        diff_page = QWidget()
        dv = QVBoxLayout(diff_page)
        dv.setContentsMargins(6, 6, 6, 6)
        bar2 = QHBoxLayout()
        bar2.addWidget(QLabel("应用前请人工确认每一条变更；写回后会自动执行结构与语义复检。"))
        bar2.addStretch(1)
        self.btn_copy_diff = QPushButton("复制 Diff")
        self.btn_copy_diff.clicked.connect(self._copy_diff)
        bar2.addWidget(self.btn_copy_diff)
        self.btn_export_patch = QPushButton("导出 patch")
        self.btn_export_patch.clicked.connect(self._export_patch)
        bar2.addWidget(self.btn_export_patch)
        dv.addLayout(bar2)
        self.diff_view = DiffView()
        dv.addWidget(self.diff_view, 1)
        self.tabs.addTab(diff_page, "差异预览")

        # —— Excel 数据 ↔ C 条目 并排对比 ——
        self.compare_view = CompareView()
        self.compare_view.row_selected.connect(self._on_compare_row)
        self.tabs.addTab(self.compare_view, "并排对比")
        self.tabs.currentChanged.connect(self._on_tab_changed)

        # —— 日志 ——
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet(
            "QTextEdit{font-family:Consolas,monospace;font-size:12px;background:#0f172a;color:#cbd5e1;border:none;}"
        )
        self.tabs.addTab(self.log_view, "运行日志")
        return self.tabs

    def _build_left_dock(self) -> None:
        dock = QDockWidget("核对概览", self)
        dock.setObjectName("leftDock")
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        self.stat_cards = StatCards()
        self.stat_cards.status_clicked.connect(self._filter_by_status)
        layout.addWidget(self.stat_cards)

        form = QFormLayout()
        self.lbl_total = QLabel("0")
        self.lbl_excel = QLabel("0")
        self.lbl_entries = QLabel("0")
        self.lbl_llm = QLabel("0")
        self.lbl_hash = QLabel("-")
        self.lbl_hash.setWordWrap(True)
        self.lbl_hash.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lbl_profile = QLabel("通用模式")
        self.lbl_profile.setWordWrap(True)
        self.lbl_filter = QLabel("-")
        self.lbl_filter.setWordWrap(True)
        form.addRow("总条目", self.lbl_total)
        form.addRow("Excel 行数", self.lbl_excel)
        form.addRow("C 条目数", self.lbl_entries)
        form.addRow("模型调用", self.lbl_llm)
        form.addRow("核对档案", self.lbl_profile)
        form.addRow("行过滤", self.lbl_filter)
        form.addRow("文件指纹", self.lbl_hash)
        layout.addLayout(form)

        layout.addWidget(QLabel("提示 / 警告"))
        self.warn_view = QTextEdit()
        self.warn_view.setReadOnly(True)
        self.warn_view.setMaximumHeight(160)
        self.warn_view.setStyleSheet(
            "QTextEdit{font-size:11px;background:#fffbeb;border:1px solid #fcd34d;"
            "border-radius:6px;color:#78350f;}"
        )
        layout.addWidget(self.warn_view)
        layout.addStretch(1)

        dock.setWidget(widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.left_dock = dock

    def _build_right_dock(self) -> None:
        dock = QDockWidget("条目详情", self)
        dock.setObjectName("rightDock")
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        self.detail = SidePanel()
        layout.addWidget(self.detail, 1)

        layout.addWidget(QLabel("人工改判（优先于模型结论）"))
        row = QHBoxLayout()
        for status, label in [
            (CheckStatus.MATCH, "一致"),
            (CheckStatus.MISMATCH, "不一致"),
            (CheckStatus.AMBIGUOUS, "歧义"),
            (CheckStatus.NOT_APPLICABLE, "不适用"),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _=False, s=status: self._override_status(s))
            row.addWidget(btn)
        layout.addLayout(row)

        self.override_note = QTextEdit()
        self.override_note.setPlaceholderText("人工备注（可选）")
        self.override_note.setMaximumHeight(70)
        layout.addWidget(self.override_note)
        dock.setWidget(widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.right_dock = dock

    def _build_statusbar(self) -> None:
        self.status_label = QLabel("就绪")
        self.statusBar().addWidget(self.status_label, 1)
        self.progress = QLabel()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(260)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.statusBar().addPermanentWidget(self.progress)
        self.statusBar().addPermanentWidget(self.progress_bar)

    def _build_actions(self) -> None:
        act_settings = QAction("设置", self)
        act_settings.setShortcut(QKeySequence("Ctrl+,"))
        act_settings.triggered.connect(self._open_settings)
        self.addAction(act_settings)
        act_check = QAction("开始核对", self)
        act_check.setShortcut(QKeySequence("Ctrl+R"))
        act_check.triggered.connect(self._start_check)
        self.addAction(act_check)
        act_report = QAction("导出报告", self)
        act_report.setShortcut(QKeySequence("Ctrl+E"))
        act_report.triggered.connect(self._export_report)
        self.addAction(act_report)

        menu = self.menuBar().addMenu("文件")
        menu.addAction(act_check)
        menu.addAction(act_report)
        menu.addSeparator()
        menu.addAction(act_settings)

    # ------------------------------------------------------------------
    # 交互
    # ------------------------------------------------------------------
    def _pick_excel(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "选择 GPIO 分配表", "", EXCEL_FILTER)
        if path:
            self.excel_edit.setText(path)
            self._detect_profile()
            self._update_actions()

    def _detect_profile(self) -> None:
        """按项目系列（设置项 / 板级配置特征）选择核对档案。"""
        series = (self.settings.get("check.series", "auto") or "auto").lower()
        c_path = self.c_edit.text()
        if series == "auto":
            series = detect_series(c_path) if c_path else "ntk"
        profile = profile_for_series(self.settings, series)
        if profile is None:
            self.profile = None
            self.check_usecase = build_check_usecase(self.settings)
            self.lbl_profile.setText("通用模式")
            self.lbl_profile.setToolTip("未匹配到档案，按「一行一配置项」通用规则核对")
            return
        self.profile = profile
        self.check_usecase = build_check_usecase(self.settings, profile)
        self.lbl_profile.setText(f"{profile.name}")
        self.lbl_profile.setToolTip(
            f"档案 id：{profile.id}；系列：{series.upper()}\n"
            f"规则文件：config/profiles/{profile.id}.yaml"
        )
        self._log(f"已识别档案：{profile.name}（{series.upper()}）")

    def _pick_c(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "选择板级配置文件", "", C_FILTER)
        if path:
            self.c_edit.setText(path)
            self._detect_profile()
            self._update_actions()

    def _update_actions(self) -> None:
        ready = bool(self.excel_edit.text()) and bool(self.c_edit.text())
        self.btn_check.setEnabled(ready and (self.worker is None))
        self.btn_stop.setEnabled(self.worker is not None)
        has_result = bool(self.session.check_result.results)
        self.btn_preview.setEnabled(has_result and self.worker is None)
        self.btn_apply.setEnabled(has_result and self.worker is None)
        self.btn_report.setEnabled(has_result)

    def _log(self, text: str) -> None:
        self.log_view.append(text)
        self.log_view.verticalScrollBar().setValue(
            self.log_view.verticalScrollBar().maximum()
        )

    def _start_check(self) -> None:
        if self.worker is not None:
            return
        self.session = Session(excel_path=self.excel_edit.text(), c_path=self.c_edit.text())
        self.result_model.set_result(None)
        self.diff_view.set_diff("")
        self.stat_cards.set_counts({})
        self.tabs.setCurrentIndex(0)
        self._log(f"=== 开始核对 === Excel={self.session.excel_path} C={self.session.c_path}")

        use_llm = bool(self.settings.get("check.use_llm", True))
        provider = self.check_usecase.orchestrator.provider if self.check_usecase.orchestrator else None
        self._log(f"模型后端：{provider.name if provider else '无'}；启用大模型核对：{use_llm}")

        def task(progress):
            return self.check_usecase.run(
                self.session, progress=progress, use_llm=use_llm
            )

        self.worker = Worker(task, self)
        self.worker.progress.connect(self._on_progress)
        self.worker.log.connect(self._log)
        self.worker.completed.connect(self._on_check_done)
        self.worker.failed.connect(self._on_failed)
        self.worker.finished.connect(self._on_worker_finished)
        self._update_actions()
        self.worker.start()

    def _stop(self) -> None:
        if self.worker is not None:
            self.worker.cancel()
            self._log("正在停止…")

    def _on_progress(self, message: str, percent: float) -> None:
        self.status_label.setText(message)
        self.progress_bar.setValue(int(percent * 100))

    def _on_check_done(self, result) -> None:
        if result is None:
            self.status_label.setText("已取消")
            return
        self.result_model.set_result(result)
        self._apply_column_widths()
        self.stat_cards.set_counts(result.summary.counts)
        self.lbl_total.setText(str(result.summary.total))
        self.lbl_excel.setText(str(result.summary.excel_rows))
        self.lbl_entries.setText(str(result.summary.c_entries))
        self.lbl_llm.setText(
            f"{result.llm_calls} 次 / {result.llm_tokens} tokens"
            + (f" / 失败 {result.llm_errors}" if result.llm_errors else "")
        )
        self.lbl_llm.setStyleSheet(
            "color:#dc2626;font-weight:600;" if result.llm_errors else "color:#0f172a;"
        )
        self.lbl_hash.setText(result.c_file_hash[:16] or "-")
        stats = result.extra.get("filter_stats") or {}
        if stats:
            used = stats.get("used_field") or stats.get("field", "")
            values = stats.get("used_values") or stats.get("values", [])
            text = f"{used} ∈ {values}\n参与 {stats.get('kept', 0)} 行 / 跳过 {stats.get('skipped', 0)} 行"
            if stats.get("fallback"):
                text = f"（回退）{text}"
            self.lbl_filter.setText(text)
            self.lbl_filter.setStyleSheet(
                "color:#b45309;" if stats.get("kept", 0) == 0 else "color:#0f172a;"
            )
        else:
            self.lbl_filter.setText("（未启用行过滤）")
            self.lbl_filter.setStyleSheet("color:#0f172a;")
        self.warn_view.setPlainText("\n".join(result.warnings) or "无")
        # 模型交互日志写入「运行日志」，失败原因同时进入警告区
        for event in result.llm_events:
            self._log(f"[模型] {event}")
        model_errors = [e for e in result.llm_events if e.startswith("✗")]
        if model_errors:
            self.warn_view.setPlainText(
                "\n".join(result.warnings + model_errors) or "\n".join(model_errors)
            )
            self.status_label.setText("模型调用失败，残余项需人工确认")
        self.compare_view.set_result(result)
        self._apply_filters()
        self.status_label.setText("核对完成")
        self._log(
            f"核对完成：一致 {result.summary.match}，不一致 {result.summary.mismatches}，"
            f"缺失 {result.summary.missing}，歧义 {result.summary.ambiguous}"
        )

    def _on_failed(self, message: str) -> None:
        self._log(f"错误：{message}")
        self.status_label.setText("出错")
        QMessageBox.critical(self, "核对失败", message)

    def _on_worker_finished(self) -> None:
        self.worker = None
        self.progress_bar.setValue(0)
        self._update_actions()

    # —— 过滤与选择 ——
    def _apply_filters(self) -> None:
        self.proxy.set_filters(
            self.status_combo.currentData() or "",
            self.search_edit.text(),
            self.only_changeable.isChecked(),
        )

    def _filter_by_status(self, status: str) -> None:
        current = self.status_combo.currentData() or ""
        if current == status:
            self.status_combo.setCurrentIndex(0)
            self.stat_cards.clear_selection()
        else:
            idx = self.status_combo.findData(status)
            if idx >= 0:
                self.status_combo.setCurrentIndex(idx)

    def _selected_results(self) -> list[MatchResult]:
        out = []
        for row in self.result_model.rows():
            if row.result.selected:
                out.append(row.result)
        return out

    def _select_all_changeable(self) -> None:
        for row in self.result_model.rows():
            row.result.selected = row.result.proposed_change.type.value != "none"
        self.result_model.set_result(self.session.check_result)
        self._apply_filters()

    def _clear_selection(self) -> None:
        for row in self.result_model.rows():
            row.result.selected = False
        self.result_model.set_result(self.session.check_result)
        self._apply_filters()

    def _on_compare_row(self, row: int) -> None:
        """并排对比视图选中某行 → 右侧详情同步显示。"""
        results = self.session.check_result.results
        if not (0 <= row < len(results)):
            return
        reqs = {r.id: r for r in self.session.check_result.requirements}
        res = results[row]
        self._show_detail(_DetailRow(res, reqs.get(res.requirement_id)))

    def _on_selection(self) -> None:
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return
        src_index = self.proxy.mapToSource(indexes[0])
        row = self.result_model.row_at(src_index)
        if row is None:
            return
        self._show_detail(row)

    def _on_tab_changed(self, index: int) -> None:
        """切到「并排对比」时自动隐藏两侧面板，把整幅宽度让给左右表格。"""
        comparing = index == self.tabs.indexOf(self.compare_view)
        self.left_dock.setVisible(not comparing)
        self.right_dock.setVisible(not comparing)

    def _apply_column_widths(self) -> None:
        """按当前模式设置列宽。"""
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        if self.result_model.profile_mode:
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(self.result_model.columnCount() - 1, QHeaderView.Stretch)
            for col, width in {0: 40, 2: 150, 3: 120, 4: 170}.items():
                self.table.setColumnWidth(col, width)
            for col in range(5, self.result_model.columnCount() - 1):
                self.table.setColumnWidth(col, 150)
        else:
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(13, QHeaderView.Stretch)
            for col, width in {
                0: 40, 2: 70, 3: 48, 4: 110, 5: 56, 6: 90,
                7: 200, 8: 90, 9: 110, 10: 64, 11: 56, 12: 70,
            }.items():
                self.table.setColumnWidth(col, width)

    def _show_detail(self, row) -> None:
        res: MatchResult = row.result
        req = row.req
        lines = []
        if req is not None:
            lines.append(
                f"<b>Excel</b> {req.sheet} 第 {req.row_no} 行<br>"
                f"网络名：{self.detail.mono(req.net_name or req.config_key or '-')}<br>"
                f"引脚：{self.detail.mono(req.pin_name_raw or '-')}<br>"
                f"宏组：{self.detail.mono(res.symbol or '-')}<br>"
            )
        lines.append(
            f"状态：<b>{STATUS_LABELS.get(res.status.value, res.status.value)}</b>"
            f"（来源：{res.source.value}，置信度 {res.confidence:.2f}）<br>"
        )
        if res.notes:
            lines.append(f"说明：{res.notes}<br>")
        if res.attribute_results:
            lines.append("<br><b>逐属性核对</b><table width='100%' cellspacing='0' cellpadding='2'>")
            lines.append(
                "<tr style='background:#e2e8f0'><th>属性</th><th>期望</th>"
                "<th>实际</th><th>结论</th><th>来源</th></tr>"
            )
            source_label = {"llm": "模型", "human": "人工", "deterministic": "规则"}
            for attr in res.attribute_results:
                color = {
                    "mismatch": "#dc2626",
                    "ambiguous": "#ca8a04",
                    "missing": "#ea580c",
                    "match": "#16a34a",
                }.get(attr.status.value, "#0f172a")
                extra = ""
                if attr.llm_confidence:
                    extra = (
                        f"<div style='color:#7c3aed;font-size:11px'>"
                        f"模型判定：{'等效' if attr.llm_equivalent else '不等效'}"
                        f"（置信度 {attr.llm_confidence:.2f}）"
                        f"{('　' + attr.llm_reason) if attr.llm_reason else ''}</div>"
                    )
                note = (
                    f"<div style='color:#64748b;font-size:11px'>{attr.notes}</div>"
                    if attr.notes
                    else ""
                )
                lines.append(
                    f"<tr><td>{attr.label}</td><td>{self.detail.mono(attr.expected or '-')}</td>"
                    f"<td>{self.detail.mono(attr.actual or '-')}</td>"
                    f"<td style='color:{color}'>{attr.status.value}</td>"
                    f"<td>{source_label.get(attr.source.value, attr.source.value)}</td></tr>"
                    f"<tr><td colspan='5'>{extra}{note}</td></tr>"
                )
            lines.append("</table>")
        elif res.evidence:
            lines.append("<b>依据</b><br>")
            for e in res.evidence:
                lines.append(f"<div class='snippet'>L{e.line} {e.snippet}</div>")
        if not res.attribute_results:
            for e in res.evidence:
                lines.append(f"<div class='snippet'>L{e.line} {e.snippet}</div>")
        change = res.proposed_change
        if change.type.value != "none":
            lines.append(
                f"<br><b>建议修改</b> [{change.type.value}] {change.reason}"
            )
        self.detail.show_result("".join(lines))

    def _table_menu(self, pos) -> None:
        from PySide6.QtWidgets import QMenu

        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return
        src_index = self.proxy.mapToSource(indexes[0])
        row = self.result_model.row_at(src_index)
        if row is None:
            return
        menu = QMenu(self)
        for status, label in [
            (CheckStatus.MATCH, "标记为一致"),
            (CheckStatus.MISMATCH, "标记为不一致"),
            (CheckStatus.AMBIGUOUS, "标记为歧义"),
            (CheckStatus.NOT_APPLICABLE, "标记为不适用"),
        ]:
            action = menu.addAction(label)
            action.triggered.connect(lambda _=False, s=status: self._override_status(s))
        menu.addSeparator()
        action = menu.addAction("复制当前行")
        action.triggered.connect(self._copy_row)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _override_status(self, status: CheckStatus) -> None:
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.information(self, "提示", "请先选中一行")
            return
        src_index = self.proxy.mapToSource(indexes[0])
        row = self.result_model.row_at(src_index)
        if row is None:
            return
        res = row.result
        res.status = status
        res.source = Source.HUMAN
        res.confidence = 1.0
        note = self.override_note.toPlainText().strip()
        if note:
            res.notes = note
        if status == CheckStatus.MISMATCH:
            entry = self.session.entries_by_id().get(
                res.matched_entry_ids[0] if res.matched_entry_ids else ""
            )
            if entry is not None:
                res.current_value = entry.value_raw
                res.proposed_change.type = (
                    ChangeType.SET_MACRO
                    if entry.kind.value in {"macro", "macro_func"}
                    else ChangeType.SET_STRUCT_FIELD
                    if entry.kind.value == "struct_field"
                    else ChangeType.SET_ARRAY_ITEM
                    if entry.kind.value == "array_item"
                    else ChangeType.NONE
                )
                res.proposed_change.target = entry.id
                res.proposed_change.old_value = entry.value_raw
                res.proposed_change.new_value = res.expected_value
                res.proposed_change.reason = "人工判定为不一致"
        self.result_model.update_row(src_index.row())
        self.stat_cards.set_counts(self._recount())
        self._show_detail(row)
        self._log(f"人工改判：{res.requirement_id} → {status.value}")

    def _recount(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for row in self.result_model.rows():
            counts[row.result.status.value] = counts.get(row.result.status.value, 0) + 1
        return counts

    def _copy_row(self) -> None:
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return
        src_index = self.proxy.mapToSource(indexes[0])
        row = self.result_model.row_at(src_index)
        if row is None:
            return
        text = "\t".join(
            [
                row.result.status.value,
                row.req.pin_name_raw if row.req else "",
                row.req.config_key if row.req else "",
                row.result.expected_value,
                row.result.current_value,
                row.result.notes,
            ]
        )
        QApplication.clipboard().setText(text)

    # —— 修改 ——
    def _preview_changes(self) -> None:
        if not self.session.check_result.results:
            return
        selected = {r.requirement_id for r in self._selected_results()}
        if not selected:
            QMessageBox.information(
                self, "提示", "请在「应用」列勾选要修改的行（可点「全选可修改」）"
            )
            return
        outcome = self.apply_usecase.preview(self.session, selected)
        self.preview = outcome
        header = (
            f"新增 {outcome.added} 行 / 删除 {outcome.removed} 行"
            + (f"；跳过 {len(outcome.skipped)} 条" if outcome.skipped else "")
        )
        self.diff_view.set_diff(outcome.diff, header)
        self.tabs.setCurrentIndex(1)
        if outcome.skipped:
            self._log("以下条目无法自动修改：\n  " + "\n  ".join(outcome.skipped))
        self._log(f"生成预览：{header}")

    def _apply_changes(self) -> None:
        if not self.session.check_result.results:
            return
        selected = {r.requirement_id for r in self._selected_results()}
        if not selected:
            QMessageBox.information(self, "提示", "请先勾选要修改的行")
            return
        confirm = QMessageBox.question(
            self,
            "确认写回",
            f"即将把 {len(selected)} 处修改写回：\n{self.session.c_path}\n\n"
            "写回前会自动备份，写回后执行结构与语义复检，失败将自动回滚。是否继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        def task(progress):
            progress("写回中 ...", 0.2)
            outcome = self.apply_usecase.apply(self.session, selected)
            progress("完成", 1.0)
            return outcome

        self.worker = Worker(task, self)
        self.worker.progress.connect(self._on_progress)
        self.worker.log.connect(self._log)
        self.worker.completed.connect(self._on_apply_done)
        self.worker.failed.connect(self._on_failed)
        self.worker.finished.connect(self._on_worker_finished)
        self._update_actions()
        self.worker.start()

    def _on_apply_done(self, outcome) -> None:
        if not isinstance(outcome, ApplyOutcome):
            return
        self._log(outcome.message)
        if outcome.backup_path:
            self._log(f"备份文件：{outcome.backup_path}")
        if outcome.semantic:
            for item in outcome.semantic.fixed:
                self._log(f"  已修复：{item}")
            for item in outcome.semantic.remaining:
                self._log(f"  未消除：{item}")
            for item in outcome.semantic.introduced:
                self._log(f"  新增差异：{item}")
        self.diff_view.set_diff(outcome.diff, outcome.message)
        if outcome.rolled_back:
            QMessageBox.warning(self, "已回滚", outcome.message)
        else:
            QMessageBox.information(self, "完成", outcome.message)
        self.status_label.setText(outcome.message)

    def _copy_diff(self) -> None:
        if self.preview and self.preview.diff:
            QApplication.clipboard().setText(self.preview.diff)
            self._log("Diff 已复制到剪贴板")

    def _export_patch(self) -> None:
        if not (self.preview and self.preview.diff):
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "导出 patch", str(Path(self.session.c_path).with_suffix(".patch")), "Patch (*.patch)"
        )
        if path:
            out = self.report_usecase.export_patch(self.session, self.preview.diff, path)
            self._log(f"已导出：{out}")

    def _export_report(self) -> None:
        if not self.session.check_result.results:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "导出核对报告", str(self.session.workdir / "report.html"), "HTML (*.html)"
        )
        if not path:
            return
        diff = self.preview.diff if self.preview else ""
        out = self.report_usecase.export_html(self.session, diff, path)
        csv_out = self.report_usecase.export_csv(self.session, path.with_suffix(".csv"))
        self._log(f"报告已导出：{out} / {csv_out}")
        QMessageBox.information(self, "导出完成", f"{out}\n{csv_out}")

    def _open_settings(self) -> None:
        from .settings_dialog import SettingsDialog

        # 重新从磁盘加载，避免用启动时的旧副本覆盖用户手动改过的配置
        self.settings = load_settings()
        dlg = SettingsDialog(self.settings, self, self.profile)
        if dlg.exec():
            self.settings = dlg.settings
            self.check_usecase = build_check_usecase(self.settings, self.profile)
            self._log("设置已保存")


def main() -> int:
    import sys

    from .style import apply_style

    app = QApplication(sys.argv)
    app.setApplicationName("GenBoardConfig")
    apply_style(app)
    window = MainWindow()
    window.show()
    return app.exec()
