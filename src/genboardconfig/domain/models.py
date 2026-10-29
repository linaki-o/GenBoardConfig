"""领域模型：全流程共用的数据契约。"""

from __future__ import annotations

import enum
from typing import Any

from pydantic import BaseModel, Field


class CheckStatus(str, enum.Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    MISSING = "missing"
    AMBIGUOUS = "ambiguous"
    NOT_APPLICABLE = "not_applicable"
    UNRESOLVED = "unresolved"


class EntryKind(str, enum.Enum):
    MACRO = "macro"
    MACRO_FUNC = "macro_func"
    STRUCT_FIELD = "struct_field"
    ARRAY_ITEM = "array_item"
    CALL_ARG = "call_arg"
    PORT_BIT = "port_bit"        # 端口位表中的单个位（BitsToByte 的一个实参）
    RTK_BLOCK = "rtk_block"      # RTK：引脚复用区块 _PIN_<PAD>(_PIN_<PAD>_<FUNC>)
    UNKNOWN = "unknown"


class ChangeType(str, enum.Enum):
    SET_MACRO = "set_macro"
    SET_STRUCT_FIELD = "set_struct_field"
    SET_ARRAY_ITEM = "set_array_item"
    SET_PORT_BIT = "set_port_bit"     # 改写端口位表中的某一位
    INSERT_BLOCK = "insert_block"
    NONE = "none"


class Source(str, enum.Enum):
    DETERMINISTIC = "deterministic"
    LLM = "llm"
    HUMAN = "human"


STATUS_LABELS: dict[str, str] = {
    CheckStatus.MATCH: "一致",
    CheckStatus.MISMATCH: "不一致",
    CheckStatus.MISSING: "缺失",
    CheckStatus.AMBIGUOUS: "歧义",
    CheckStatus.NOT_APPLICABLE: "不适用",
    CheckStatus.UNRESOLVED: "未解析",
}


class GPIORequirement(BaseModel):
    """Excel 中一行的归一化结果。"""

    id: str
    sheet: str = ""
    row_no: int = 0
    pin_name_raw: str = ""
    pin_key: str = ""
    gpio_num: int | None = None
    function_name: str = ""
    config_key: str = ""
    config_key_norm: str = ""
    expected_value: str = ""
    expected_normalized: str = ""
    chip_instance: str = ""
    polarity: str = ""
    pull: str = ""
    mux: str = ""
    bom_ref: str = ""
    remark: str = ""
    raw: dict[str, str] = Field(default_factory=dict)
    parse_status: str = "ok"
    # —— 档案模式（HSI）：一行多个待核对属性 ——
    net_name: str = ""
    attributes: list["ExpectedAttribute"] = Field(default_factory=list)

    def attribute(self, name: str) -> "ExpectedAttribute | None":
        for attr in self.attributes:
            if attr.name == name:
                return attr
        return None


class ExpectedAttribute(BaseModel):
    """一行中的一个待核对属性。"""

    name: str
    label: str = ""
    source_field: str = ""
    value: str = ""              # Excel 原文
    normalized: str = ""         # 归一化后的期望语义值
    checkable: bool = True
    check: str = "none"          # port_bit | info | none
    note: str = ""               # 附加说明（如 Excel 标注 NA）


class ConfigEntry(BaseModel):
    """.c 文件中解析出的一个配置项（含精确落点）。"""

    id: str
    kind: EntryKind = EntryKind.UNKNOWN
    key: str = ""
    key_norm: str = ""
    value_raw: str = ""
    value_normalized: str = ""
    value_kind: str = "literal"       # literal | symbolic | expression | none
    owner: str = ""                   # 所属结构体/数组/宏分组
    file: str = ""
    line: int = 0                    # 1-based
    col: int = 0                     # 0-based 列偏移
    value_col: int = 0               # 值在行内的列偏移（改写用）
    value_len: int = 0
    raw_text: str = ""
    context: str = ""                # 供模型参考的上下文摘要
    # —— 档案模式 ——
    comment: str = ""                # 宏行尾注释
    condition: str = ""              # 条件编译上下文（#if ...），无条件为空
    group: str = ""                  # 所属宏组前缀，如 DIG1_HPD
    role: str = ""                   # 组内角色：port / bit / active
    port: str = ""                   # 端口字母，如 C
    bit: int | None = None           # 位号
    table: str = ""                  # 位表名，如 PORT_C_DEFAULT_OUT
    function: str = ""               # RTK：区块对应的原理图网络名
    members: list[str] = Field(default_factory=list)   # RTK：该 pad 可选的复用功能


class Evidence(BaseModel):
    entry_id: str = ""
    line: int = 0
    snippet: str = ""


class ProposedChange(BaseModel):
    type: ChangeType = ChangeType.NONE
    target: str = ""                 # entry_id
    old_value: str = ""
    new_value: str = ""
    reason: str = ""
    applied: bool = False
    error: str = ""


class MatchResult(BaseModel):
    requirement_id: str
    status: CheckStatus = CheckStatus.UNRESOLVED
    confidence: float = 0.0
    matched_entry_ids: list[str] = Field(default_factory=list)
    current_value: str = ""
    expected_value: str = ""
    evidence: list[Evidence] = Field(default_factory=list)
    proposed_change: ProposedChange = Field(default_factory=ProposedChange)
    source: Source = Source.DETERMINISTIC
    notes: str = ""
    selected: bool = True            # 是否纳入修改
    candidate_count: int = 0
    # —— 档案模式：逐属性结论 ——
    attribute_results: list["AttributeResult"] = Field(default_factory=list)
    symbol: str = ""                 # 定位用引脚，如 PC1
    signals: list[str] = Field(default_factory=list)   # 占用该引脚的信号（上下文）

    def attribute(self, name: str) -> "AttributeResult | None":
        for attr in self.attribute_results:
            if attr.name == name:
                return attr
        return None


class AttributeResult(BaseModel):
    """单个属性的核对结论。"""

    name: str
    label: str = ""
    expected: str = ""
    normalized: str = ""      # 归一化后的期望语义值
    actual: str = ""
    status: CheckStatus = CheckStatus.UNRESOLVED
    checkable: bool = True
    confidence: float = 0.0
    evidence: list[Evidence] = Field(default_factory=list)
    change: ProposedChange | None = None
    source: Source = Source.DETERMINISTIC
    notes: str = ""
    # —— 模型复核痕迹 ——
    llm_equivalent: bool | None = None   # 模型判定是否等效
    llm_confidence: float = 0.0          # 模型置信度
    llm_reason: str = ""                 # 模型给出的理由


class CheckSummary(BaseModel):
    total: int = 0
    counts: dict[str, int] = Field(default_factory=dict)
    mismatches: int = 0
    missing: int = 0
    ambiguous: int = 0
    match: int = 0
    not_applicable: int = 0
    unresolved: int = 0
    excel_rows: int = 0
    c_entries: int = 0
    duration_ms: int = 0


class CheckResult(BaseModel):
    requirements: list[GPIORequirement] = Field(default_factory=list)
    entries: list[ConfigEntry] = Field(default_factory=list)
    results: list[MatchResult] = Field(default_factory=list)
    summary: CheckSummary = Field(default_factory=CheckSummary)
    excel_path: str = ""
    c_path: str = ""
    c_file_hash: str = ""
    column_mapping: dict[str, str] = Field(default_factory=dict)
    llm_calls: int = 0
    llm_tokens: int = 0
    llm_errors: int = 0
    llm_events: list[str] = Field(default_factory=list)   # 模型交互日志（请求/响应/错误）
    warnings: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)
