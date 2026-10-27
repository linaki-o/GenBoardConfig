"""设置对话框：模型、阈值、批量、密钥。"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..app.service_factory import SECRET_KEY_NAME, secret_store
from ..infra.settings import Settings


class SettingsDialog(QDialog):
    def __init__(self, settings: Settings, parent=None, profile=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumWidth(520)
        self.settings = settings
        self.profile = profile

        root = QVBoxLayout(self)

        proj_box = QGroupBox("项目")
        pform = QFormLayout(proj_box)
        self.series_combo = QComboBox()
        self.series_combo.addItem("自动检测（按板级配置文件特征）", "auto")
        self.series_combo.addItem("NTK 系列（Novatek 端口位表）", "ntk")
        self.series_combo.addItem("RTK 系列（Realtek 引脚复用表）", "rtk")
        sidx = self.series_combo.findData(settings.get("check.series", "auto"))
        self.series_combo.setCurrentIndex(max(0, sidx))
        pform.addRow("项目系列", self.series_combo)
        pnote = QLabel(
            "NTK：核对 PORT_X_DEFAULT_OUT/DIR/PP 端口位表；"
            "RTK：核对 #define _PIN_<PAD> (_PIN_<PAD>_<FUNC>) 引脚复用。"
        )
        pnote.setWordWrap(True)
        pnote.setStyleSheet("color:#64748b;font-size:11px;")
        pform.addRow("", pnote)
        root.addWidget(proj_box)

        if profile is not None:
            root.addWidget(self._build_filter_box(profile))

        llm_box = QGroupBox("大模型")
        form = QFormLayout(llm_box)
        self.provider_combo = QComboBox()
        self.provider_combo.addItem("离线 Mock（无需密钥，用于演示/回归）", "mock")
        self.provider_combo.addItem("OpenAI 兼容（OpenAI / DeepSeek / 通义 / 自建网关）", "openai_compatible")
        self.provider_combo.addItem("Anthropic（预留）", "anthropic")
        idx = self.provider_combo.findData(settings.get("llm.provider", "mock"))
        self.provider_combo.setCurrentIndex(max(0, idx))
        form.addRow("后端", self.provider_combo)

        self.base_url = QLineEdit(settings.get("llm.base_url", ""))
        form.addRow("Base URL", self.base_url)
        self.model = QLineEdit(settings.get("llm.model", ""))
        form.addRow("模型", self.model)

        self.api_key = QLineEdit(secret_store(settings).get(SECRET_KEY_NAME))
        self.api_key.setEchoMode(QLineEdit.Password)
        self.api_key.setPlaceholderText("留空则使用设置文件中的 llm.api_key")
        form.addRow("API Key", self.api_key)

        self.temperature = QLineEdit(str(settings.get("llm.temperature", 0.0)))
        form.addRow("temperature", self.temperature)
        self.batch = QSpinBox()
        self.batch.setRange(1, 200)
        self.batch.setValue(int(settings.get("llm.max_batch_size", 20)))
        form.addRow("每批条数", self.batch)
        self.retries = QSpinBox()
        self.retries.setRange(0, 10)
        self.retries.setValue(int(settings.get("llm.max_retries", 3)))
        form.addRow("重试次数", self.retries)
        self.structured = QCheckBox("请求端 JSON Schema 约束输出")
        self.structured.setChecked(bool(settings.get("llm.use_structured_output", True)))
        form.addRow("", self.structured)
        root.addWidget(llm_box)

        check_box = QGroupBox("核对策略")
        cform = QFormLayout(check_box)
        self.threshold = QLineEdit(str(settings.get("check.confidence_threshold", 0.8)))
        cform.addRow("置信度阈值", self.threshold)
        self.use_llm = QCheckBox("启用大模型核对（关闭则仅用规则判定）")
        self.use_llm.setChecked(bool(settings.get("check.use_llm", True)))
        cform.addRow("", self.use_llm)
        self.mask = QCheckBox("送往云端前脱敏敏感信息")
        self.mask.setChecked(bool(settings.get("privacy.mask_sensitive", True)))
        cform.addRow("", self.mask)
        root.addWidget(check_box)

        note = QLabel(
            "提示：API Key 通过 Windows DPAPI 加密后保存在 config/secrets.bin，"
            "不会写入 YAML、日志或报告。设置将写入 config/settings.local.yaml。"
        )
        note.setWordWrap(True)
        note.setStyleSheet("color:#64748b;font-size:11px;")
        root.addWidget(note)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

    def _build_filter_box(self, profile) -> QGroupBox:
        """行过滤设置：只核对指定列取指定值的行。"""
        box = QGroupBox(f"行过滤（档案：{profile.name}）")
        form = QFormLayout(box)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("（不过滤，全部行）", "")
        for field_name in profile.columns:
            self.filter_combo.addItem(field_name, field_name)
        idx = self.filter_combo.findData(profile.filter_field)
        self.filter_combo.setCurrentIndex(max(0, idx))
        form.addRow("过滤列", self.filter_combo)

        self.filter_values = QLineEdit(", ".join(profile.filter_values))
        self.filter_values.setPlaceholderText("如 IN, OUT")
        form.addRow("取值", self.filter_values)

        hint = QLabel(
            "仅核对「过滤列」取值命中「取值」的行；修改后保存到 "
            "config/settings.local.yaml，不影响档案文件本身。"
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color:#64748b;font-size:11px;")
        form.addRow("", hint)
        return box

    def _save(self) -> None:
        s = self.settings
        s.set("llm.provider", self.provider_combo.currentData())
        s.set("llm.base_url", self.base_url.text().strip())
        s.set("llm.model", self.model.text().strip())
        try:
            s.set("llm.temperature", float(self.temperature.text() or 0))
            s.set("check.confidence_threshold", float(self.threshold.text() or 0.8))
        except ValueError:
            QMessageBox.warning(self, "参数错误", "temperature / 置信度阈值必须是数字")
            return
        s.set("llm.max_batch_size", self.batch.value())
        s.set("llm.max_retries", self.retries.value())
        s.set("llm.use_structured_output", self.structured.isChecked())
        s.set("check.use_llm", self.use_llm.isChecked())
        s.set("privacy.mask_sensitive", self.mask.isChecked())
        s.set("check.series", self.series_combo.currentData() or "auto")
        if self.profile is not None:
            values = [
                v.strip()
                for v in self.filter_values.text().replace("，", ",").split(",")
                if v.strip()
            ]
            s.set(
                f"profiles.{self.profile.id}.row_filter",
                {
                    "field": self.filter_combo.currentData() or "",
                    "values": values,
                },
            )
        s.save_local()
        if self.api_key.text():
            secret_store(s).set(SECRET_KEY_NAME, self.api_key.text())
            s.set("llm.api_key", "")
        self.accept()
