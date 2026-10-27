"""RTK 档案核对引擎（Realtek 引脚复用表）。

层级（依据 docs/comparison_rules_rtk.md 与评审确认）：
  L0 行筛选   —— G 列「GPIO TYPE」非空的行全部参与
  L1 电气属性 —— 通用 GPIO(GPI/GPO_PP/GPO_OD) 与 Excel 的方向/开漏推挽比对
  L2 功能名   —— 专用功能名与 Excel (App) 功能名；不一致时交大模型判定等效
  L3 存在性   —— .h 中无该网络名区块 → 不核对（评审结论）
  L4 噪声     —— Excel 模板占位符 / 专用功能域的网络名直接跳过
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import (
    AttributeResult,
    ChangeType,
    CheckStatus,
    ConfigEntry,
    EntryKind,
    Evidence,
    GPIORequirement,
    MatchResult,
    ProposedChange,
    Source,
)
from .planner import aggregate_attribute_changes
from .profiles import Profile

GENERIC_FAMILY = {"GPI": "IN", "GPO_PP": "OUT", "GPO_OD": "OUT"}


def norm_text(text: str) -> str:
    """网络名/功能名归一化：去括号说明、去分隔符、转大写。"""
    cleaned = re.sub(r"\(.*?\)", " ", text or "")
    return re.sub(r"[^A-Z0-9]+", "_", cleaned.upper()).strip("_")


def app_function(pin_name: str) -> str:
    """取 Excel「PIN Name」列中带 (App) 标记的功能名（无则取第一项）。"""
    parts = [p.strip() for p in (pin_name or "").split("/") if p.strip()]
    app = next((p for p in parts if "(App)" in p), parts[0] if parts else "")
    return norm_text(app.replace("(App)", ""))


@dataclass
class RtkEngine:
    profile: Profile
    entries: list[ConfigEntry]

    def __post_init__(self) -> None:
        self.by_function: dict[str, ConfigEntry] = {}
        for entry in self.entries:
            if entry.kind != EntryKind.RTK_BLOCK:
                continue
            key = norm_text(entry.function)
            if key:
                self.by_function.setdefault(key, entry)
        cfg = self.profile.c_config or {}
        self.generic_gpio = {str(v).upper() for v in (cfg.get("generic_gpio") or [])}
        self.expected_gpio = {
            str(k).upper(): str(v).upper() for k, v in (cfg.get("expected_gpio") or {}).items()
        }
        self.expected_io = {
            str(k).upper(): str(v).upper() for k, v in (cfg.get("expected_io") or {}).items()
        }
        self.function_category: dict[str, list[str]] = {
            str(k).upper(): [str(v).upper() for v in vs]
            for k, vs in (cfg.get("function_category") or {}).items()
        }
        self.skip_patterns = [
            re.compile(p, re.IGNORECASE) for p in (cfg.get("skip_net_patterns") or [])
        ]
        self.missing_action = str(cfg.get("missing_action") or "skip")
        self.llm_equivalence = bool(cfg.get("llm_function_equivalence", True))
        self.llm_threshold = float(cfg.get("llm_confidence_threshold", 0.7))

    # ------------------------------------------------------------------
    def check(self, requirements: list[GPIORequirement]) -> list[MatchResult]:
        return [self._check_one(req) for req in requirements]

    def _check_one(self, req: GPIORequirement) -> MatchResult:
        net = (req.net_name or req.config_key or "").strip()
        result = MatchResult(
            requirement_id=req.id,
            expected_value=req.expected_value,
            source=Source.DETERMINISTIC,
            notes="",
        )

        # L4 噪声
        for pattern in self.skip_patterns:
            if pattern.search(net):
                result.status = CheckStatus.NOT_APPLICABLE
                result.notes = f"「{net}」命中噪声规则（{pattern.pattern}），不纳入核对"
                self._fill_skipped(result, req)
                return result

        # L3 存在性
        entry = self.by_function.get(norm_text(net))
        if entry is None:
            if self.missing_action == "skip":
                result.status = CheckStatus.NOT_APPLICABLE
                result.notes = f"板级配置中未定义「{net}」，按规则不纳入核对"
                self._fill_skipped(result, req)
                return result
            result.status = CheckStatus.MISSING
            result.notes = f"板级配置中未定义「{net}」"
            self._fill_skipped(result, req)
            return result

        selected = (entry.value_raw or "").upper()
        result.symbol = entry.owner or entry.key
        result.evidence = [
            Evidence(entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip())
        ]

        elec = self._check_electrical(req, entry, selected)
        io = self._check_io_type(req, entry, selected)
        result.attribute_results = [elec, io]

        # L2 功能名
        name_attr = self._check_function_name(req, entry, selected)
        if name_attr is not None:
            result.attribute_results.append(name_attr)

        checkable = [a for a in result.attribute_results if a.checkable]
        result.status = max(
            (a.status for a in checkable),
            key=lambda s: {
                CheckStatus.MATCH.value: 0,
                CheckStatus.NOT_APPLICABLE.value: 1,
                CheckStatus.UNRESOLVED.value: 2,
                CheckStatus.AMBIGUOUS.value: 3,
                CheckStatus.MISSING.value: 4,
                CheckStatus.MISMATCH.value: 5,
            }.get(s, 0),
        )
        result.confidence = min((a.confidence for a in checkable), default=0.6)

        diffs = [
            f"{a.label}：期望 {a.expected}，实际 {a.actual}"
            for a in result.attribute_results
            if a.status == CheckStatus.MISMATCH.value
        ]
        notes = f"{entry.owner} 复用功能 {selected}"
        if entry.function:
            notes += f"（网络名 {entry.function}）"
        if diffs:
            notes += "；" + "；".join(diffs)
        else:
            notes += "；电气属性与 Excel 期望一致"
        result.notes = notes
        aggregate_attribute_changes(result)
        return result

    # ------------------------------------------------------------------
    def _fill_skipped(self, result: MatchResult, req: GPIORequirement) -> None:
        for attr in req.attributes:
            result.attribute_results.append(
                AttributeResult(
                    name=attr.name,
                    label=attr.label,
                    expected=attr.value,
                    normalized=attr.normalized,
                    actual="",
                    status=CheckStatus.NOT_APPLICABLE,
                    checkable=False,
                    confidence=0.5,
                    notes=result.notes,
                )
            )

    def _expected_gpio(self, req: GPIORequirement) -> tuple[str, str]:
        """返回 (期望的通用 GPIO 类型, 期望来源说明)。"""
        gpio_type = self._attr_value(req, "gpio_type").upper()
        io_type = self._attr_value(req, "io_type").upper()
        # 输出类型列只对输出类信号有效
        if gpio_type == "OUT" and io_type and io_type in self.expected_io:
            return self.expected_io[io_type], f"由输出类型「{io_type}」决定"
        if gpio_type in self.expected_gpio:
            return self.expected_gpio[gpio_type], f"由方向/类别「{gpio_type}」决定"
        return "", ""

    def _attr_value(self, req: GPIORequirement, field_name: str) -> str:
        for attr in req.attributes:
            if attr.source_field == field_name:
                return (attr.value or "").strip()
        return ""

    def _category_of(self, selected: str) -> str:
        """专用功能 → 电气类别。"""
        for category, tokens in self.function_category.items():
            for token in tokens:
                if token in selected:
                    return category
        return ""

    # ------------------------------------------------------------------
    def _check_electrical(
        self, req: GPIORequirement, entry: ConfigEntry, selected: str
    ) -> AttributeResult:
        gpio_type = self._attr_value(req, "gpio_type")
        expected_norm = self._profile_value(req, "gpio_type")
        expected = (expected_norm or gpio_type).upper()
        label = "方向/类别"

        if selected in self.generic_gpio:
            target, why = self._expected_gpio(req)
            if not target:
                return AttributeResult(
                    name="elec_type",
                    label=label,
                    expected=gpio_type,
                    actual=selected,
                    status=CheckStatus.NOT_APPLICABLE,
                    checkable=False,
                    confidence=0.5,
                    notes="Excel 未给出可判定的方向/输出类型",
                )
            if selected == target:
                return AttributeResult(
                    name="elec_type",
                    label=label,
                    expected=gpio_type,
                    normalized=expected,
                    actual=selected,
                    status=CheckStatus.MATCH,
                    checkable=True,
                    confidence=0.95,
                    evidence=[
                        Evidence(
                            entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip()
                        )
                    ],
                    notes=f"{why}，配置为 {selected}",
                )
            change = self._plan_gpio_change(entry, selected, target, req)
            return AttributeResult(
                name="elec_type",
                label=label,
                expected=gpio_type,
                normalized=expected,
                actual=selected,
                status=CheckStatus.MISMATCH,
                checkable=True,
                confidence=0.92,
                evidence=[
                    Evidence(
                        entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip()
                    )
                ],
                change=change,
                notes=f"期望 {target}（{why}），配置为 {selected}",
            )

        # 专用功能
        app = app_function(req.pin_name_raw)
        if app and app == norm_text(selected):
            return AttributeResult(
                name="elec_type",
                label=label,
                expected=gpio_type,
                normalized=expected,
                actual=selected,
                status=CheckStatus.MATCH,
                checkable=True,
                confidence=0.95,
                evidence=[
                    Evidence(
                        entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip()
                    )
                ],
                notes=f"配置使用专用功能 {selected}，与 Excel 期望功能一致",
            )
        category = self._category_of(selected)
        if not category:
            return AttributeResult(
                name="elec_type",
                label=label,
                expected=gpio_type,
                normalized=expected,
                actual=selected,
                status=CheckStatus.AMBIGUOUS,
                checkable=True,
                confidence=0.5,
                evidence=[
                    Evidence(
                        entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip()
                    )
                ],
                notes=f"配置使用专用功能 {selected}，其电气类别需人工/模型确认",
            )
        if category == expected or (expected == "OUT" and category == "OUT"):
            return AttributeResult(
                name="elec_type",
                label=label,
                expected=gpio_type,
                normalized=expected,
                actual=selected,
                status=CheckStatus.MATCH,
                checkable=True,
                confidence=0.85,
                evidence=[
                    Evidence(
                        entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip()
                    )
                ],
                notes=f"配置使用专用功能 {selected}（类别 {category}），与 Excel 期望相符",
            )
        change = self._plan_generic_change(entry, selected, req, why="期望通用 GPIO")
        return AttributeResult(
            name="elec_type",
            label=label,
            expected=gpio_type,
            normalized=expected,
            actual=selected,
            status=CheckStatus.MISMATCH,
            checkable=True,
            confidence=0.8,
            evidence=[
                Evidence(entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip())
            ],
            change=change,
            notes=f"配置使用专用功能 {selected}（类别 {category}），与期望 {expected} 不符",
        )

    def _check_io_type(
        self, req: GPIORequirement, entry: ConfigEntry, selected: str
    ) -> AttributeResult:
        io_type = self._attr_value(req, "io_type")
        gpio_type = self._attr_value(req, "gpio_type").upper()
        if not io_type:
            return AttributeResult(
                name="io_type",
                label="输出类型",
                expected="",
                actual=selected if selected in self.generic_gpio else "",
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.6,
                notes="Excel 未填输出类型（仅输出类信号需填）",
            )
        if gpio_type and gpio_type != "OUT":
            return AttributeResult(
                name="io_type",
                label="输出类型",
                expected=io_type,
                normalized=self._profile_value(req, "io_type"),
                actual=selected,
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.6,
                notes=f"该行方向为 {gpio_type}（非输出），输出类型列不适用",
            )
        if selected not in self.generic_gpio:
            return AttributeResult(
                name="io_type",
                label="输出类型",
                expected=io_type,
                normalized=self._profile_value(req, "io_type"),
                actual=selected,
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.6,
                notes=f"配置使用专用功能 {selected}，开漏/推挽由功能本身决定",
            )
        target = self.expected_io.get(io_type.upper(), "")
        if not target:
            return AttributeResult(
                name="io_type",
                label="输出类型",
                expected=io_type,
                actual=selected,
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.5,
                notes="未登记的输出类型取值",
            )
        same = selected == target
        change = None if same else self._plan_gpio_change(entry, selected, target, req)
        return AttributeResult(
            name="io_type",
            label="输出类型",
            expected=io_type,
            normalized=self._profile_value(req, "io_type"),
            actual=selected,
            status=CheckStatus.MATCH if same else CheckStatus.MISMATCH,
            checkable=True,
            confidence=0.92,
            evidence=[
                Evidence(entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip())
            ],
            change=change,
            notes=(
                f"期望 {target}，配置为 {selected}"
                if not same
                else f"配置为 {selected}，与期望一致"
            ),
        )

    def _check_function_name(
        self, req: GPIORequirement, entry: ConfigEntry, selected: str
    ) -> AttributeResult | None:
        """L2：专用功能名与 Excel (App) 功能名不一致 → 交模型判定。"""
        if not self.llm_equivalence:
            return None
        app = app_function(req.pin_name_raw)
        if not app:
            return None
        if app == norm_text(selected):
            return None
        if selected in self.generic_gpio:
            # 通用 GPIO 实现专用功能 → 电气一致即算一致（评审结论），此处仅作标注
            return AttributeResult(
                name="function_name",
                label="功能名",
                expected=app,
                actual=selected,
                status=CheckStatus.MATCH,
                checkable=False,
                confidence=0.75,
                evidence=[
                    Evidence(
                        entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip()
                    )
                ],
                notes=f"以通用 GPIO（{selected}）实现「{app}」，电气属性一致，标注说明",
            )
        return AttributeResult(
            name="function_name",
            label="功能名",
            expected=app,
            actual=selected,
            status=CheckStatus.AMBIGUOUS,
            checkable=True,
            confidence=0.5,
            evidence=[
                Evidence(entry_id=entry.id, line=entry.line, snippet=entry.raw_text.strip())
            ],
            notes=f"Excel 期望功能「{app}」，配置为「{selected}」，需模型判定是否等效",
        )

    # ------------------------------------------------------------------
    def _profile_value(self, req: GPIORequirement, field_name: str) -> str:
        for attr in req.attributes:
            if attr.source_field == field_name:
                return attr.normalized
        return ""

    def _plan_gpio_change(
        self,
        entry: ConfigEntry,
        selected: str,
        target: str,
        req: GPIORequirement,
    ) -> ProposedChange:
        """通用 GPIO 家族内的切换（GPI↔GPO_*、GPO_PP↔GPO_OD）可直接写回。"""
        return ProposedChange(
            type=ChangeType.SET_MACRO,
            target=entry.id,
            old_value=selected,
            new_value=target,
            reason=(
                f"L{entry.line} {entry.owner}：期望 {target}，实际 {selected}（改 #define 右值）"
            ),
        )

    def _plan_generic_change(
        self,
        entry: ConfigEntry,
        selected: str,
        req: GPIORequirement,
        why: str,
    ) -> ProposedChange:
        """专用功能 → 通用 GPIO 的切换影响硬件行为，仅给建议不自动改。"""
        target, _ = self._expected_gpio(req)
        return ProposedChange(
            type=ChangeType.NONE,
            target="",
            old_value=selected,
            new_value=target,
            reason=(
                f"L{entry.line} {entry.owner}：{why}（期望 {target or '通用 GPIO'}，"
                "当前为专用功能，改动影响硬件行为，需人工确认）"
            ),
        )
