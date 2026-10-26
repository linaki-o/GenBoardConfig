"""HSI 档案比对引擎（v0.3 · 端口位表核对）。

核对范围（依据评审要求收敛）：
- C 侧只核对 ``PORT_<X>_DEFAULT_{OUT,DIR,PP,PU}`` 端口位表；
- Excel 只核对「GPIO TYPE」列为 IN/OUT 的行；
- 引脚直接取自 Excel 的「PIN Name」列，**不再依赖配置中的信号宏组**；
  信号宏组只作为「该引脚被哪些信号占用」的上下文展示。

比对依据见 docs/comparison_rules.md。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

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
from .normalize import norm_key
from .profiles import Profile

# 行状态严重度（数值越大越严重）
SEVERITY = {
    CheckStatus.MATCH: 0,
    CheckStatus.NOT_APPLICABLE: 1,
    CheckStatus.UNRESOLVED: 2,
    CheckStatus.AMBIGUOUS: 3,
    CheckStatus.MISSING: 4,
    CheckStatus.MISMATCH: 5,
}

RE_CHIP_PIN = re.compile(r"^P?([A-Z]{1,2})[_\-]?([0-9]+)$")
RE_TRAILING_CHIP_PIN = re.compile(r"(?:^|_)(P[A-Z]{1,2}[0-9]+)$")


def parse_chip_pin(text: str) -> tuple[str, int] | None:
    """把 `PC1` / `PK1/PWMB` / `PB6` 解析为 (端口, 位号)。"""
    raw = (text or "").strip().upper().replace(" ", "")
    if not raw:
        return None
    head = raw.split("/")[0]
    m = RE_CHIP_PIN.match(head)
    if not m:
        return None
    return m.group(1), int(m.group(2))


def chip_pin_text(port: str, bit: int | None) -> str:
    """统一成 Excel 记法：端口 C + 位 1 → `PC1`。"""
    if not port or bit is None:
        return ""
    return f"P{port}{bit}"


def parse_trailing_chip_pin(value: str) -> tuple[str, int] | None:
    """从 `PSM2_PIN_PK2` / `PWMB_PIN_PK1` 之类取值中解析出 (端口, 位号)。"""
    raw = (value or "").strip().upper()
    if not raw:
        return None
    m = RE_TRAILING_CHIP_PIN.search(raw)
    if not m:
        return None
    return parse_chip_pin(m.group(1))


@dataclass
class SymbolGroup:
    """配置中的一个信号宏组（仅用于上下文展示：哪些信号占用某个引脚）。"""

    prefix: str
    ports: list[ConfigEntry] = field(default_factory=list)
    bits: list[ConfigEntry] = field(default_factory=list)
    actives: list[ConfigEntry] = field(default_factory=list)

    @staticmethod
    def _primary(entries: list[ConfigEntry]) -> ConfigEntry | None:
        if not entries:
            return None
        unconditional = [e for e in entries if not e.condition]
        return (unconditional or entries)[0]

    @property
    def port(self) -> ConfigEntry | None:
        return self._primary(self.ports)

    @property
    def bit(self) -> ConfigEntry | None:
        return self._primary(self.bits)

    @property
    def active(self) -> ConfigEntry | None:
        return self._primary(self.actives)

    def variants(self, role: str) -> list[ConfigEntry]:
        return {"port": self.ports, "bit": self.bits, "active": self.actives}.get(role, [])

    @property
    def comments(self) -> list[str]:
        return [
            e.comment
            for e in (self.port, self.bit, self.active)
            if e is not None and e.comment
        ]

    def conditional_note(self) -> str:
        notes = []
        for role, entries in (
            ("PORT", self.ports),
            ("BIT", self.bits),
            ("ACTIVE", self.actives),
        ):
            if len(entries) > 1:
                detail = "；".join(
                    f"L{e.line} {e.value_raw}" + (f" [{e.condition}]" if e.condition else "")
                    for e in entries
                )
                notes.append(f"{role} 有 {len(entries)} 处定义：{detail}")
        return "；".join(notes)

    def derived_pin(self) -> tuple[str, int | None]:
        port = ""
        bit: int | None = None
        if self.port is not None:
            port = self.port.port
        if self.bit is not None:
            bit = self.bit.bit
            if self.bit.port:
                port = self.bit.port
        return port, bit


class HsiEngine:
    """按 HSI 档案核对 Excel 行与板级端口位表。"""

    def __init__(self, profile: Profile, entries: Iterable[ConfigEntry]):
        self.profile = profile
        self.entries = list(entries)
        self.entries_by_id = {e.id: e for e in self.entries}
        self.port_bits: dict[tuple[str, str, int], ConfigEntry] = {}
        self.groups: dict[str, SymbolGroup] = {}
        self._index()

    # ---------- 索引 ----------
    def _index(self) -> None:
        for entry in self.entries:
            if entry.kind == EntryKind.PORT_BIT and entry.table:
                self.port_bits[(entry.table, entry.port, entry.bit or 0)] = entry
                continue
            if not entry.group or not entry.role:
                continue
            group = self.groups.setdefault(entry.group, SymbolGroup(prefix=entry.group))
            if entry.role == "port":
                group.ports.append(entry)
            elif entry.role == "bit":
                group.bits.append(entry)
            elif entry.role == "active":
                group.actives.append(entry)

    def port_bit(self, table_attr: str, port: str, bit: int) -> ConfigEntry | None:
        table = f"PORT_{port}_DEFAULT_{table_attr}"
        return self.port_bits.get((table, port, bit))

    def signals_on(self, port: str, bit: int) -> list[str]:
        """占用该引脚的信号组（上下文展示用）。"""
        users = []
        for prefix, group in self.groups.items():
            gport, gbit = group.derived_pin()
            if gport == port and gbit == bit:
                users.append(prefix)
        return sorted(users)

    # ---------- 核对 ----------
    def check(self, requirements: list[GPIORequirement]) -> list[MatchResult]:
        results = [self._check_one(req) for req in requirements]
        self._guard_conflicts(results)
        return results

    def _check_one(self, req: GPIORequirement) -> MatchResult:
        pin = parse_chip_pin(req.pin_name_raw)
        result = MatchResult(
            requirement_id=req.id,
            expected_value=req.expected_value,
            source=Source.DETERMINISTIC,
            notes="",
        )
        if pin is None:
            result.status = CheckStatus.UNRESOLVED
            result.notes = f"无法从「{req.pin_name_raw}」解析出芯片引脚（端口,位号）"
            for attr in req.attributes:
                result.attribute_results.append(
                    AttributeResult(
                        name=attr.name,
                        label=attr.label,
                        expected=attr.value,
                        normalized=attr.normalized,
                        actual="",
                        status=CheckStatus.UNRESOLVED,
                        checkable=attr.checkable,
                        confidence=0.0,
                        notes=result.notes,
                    )
                )
            return result

        port, bit = pin
        result.symbol = chip_pin_text(port, bit)
        signals = self.signals_on(port, bit)
        result.signals = signals
        for attr in req.attributes:
            result.attribute_results.append(
                self._check_attribute(attr, port, bit, signals)
            )
        result.status = self._worst(result.attribute_results, CheckStatus.MATCH)
        result.confidence = min(
            (a.confidence for a in result.attribute_results if a.checkable),
            default=0.6,
        )
        diffs = [
            f"{a.label}：期望 {a.expected}，实际 {a.actual}"
            for a in result.attribute_results
            if a.status == CheckStatus.MISMATCH
        ]
        notes = f"引脚 {result.symbol}（{port} 端口第 {bit} 位）"
        if signals:
            notes += f"；占用信号：{'、'.join(signals[:4])}"
        notes += "；" + ("；".join(diffs) if diffs else "核对项全部一致")
        result.notes = notes
        return result

    def _check_attribute(
        self,
        attr,
        port: str,
        bit: int,
        signals: list[str],
    ) -> AttributeResult:
        kind = getattr(attr, "check", "none")
        table_attr = self._table_attr(attr.name)

        # 只读属性：展示配置现状，不参与判定
        if kind == "info":
            entry = self.port_bit(table_attr, port, bit) if table_attr else None
            if entry is None:
                return AttributeResult(
                    name=attr.name,
                    label=attr.label,
                    expected=attr.value or "-",
                    actual="",
                    status=CheckStatus.NOT_APPLICABLE,
                    checkable=False,
                    confidence=0.5,
                    notes=f"缺少端口位表 PORT_{port}_DEFAULT_{table_attr}",
                )
            return AttributeResult(
                name=attr.name,
                label=attr.label,
                expected=attr.value or "-",
                normalized=attr.normalized,
                actual=entry.value_raw,
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.9,
                evidence=[
                    Evidence(
                        entry_id=entry.id,
                        line=entry.line,
                        snippet=entry.raw_text.strip(),
                    )
                ],
                notes=f"配置现状（不参与判定）：PORT_{port}_DEFAULT_{table_attr}[{bit}]",
            )

        if kind == "none" or not attr.value or not attr.checkable:
            return AttributeResult(
                name=attr.name,
                label=attr.label,
                expected=attr.value,
                normalized=attr.normalized,
                actual="",
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.5,
                notes=attr.note or "不在核对范围（板级端口位表无对应项）",
            )

        if table_attr is None:
            return AttributeResult(
                name=attr.name,
                label=attr.label,
                expected=attr.value,
                normalized=attr.normalized,
                actual="",
                status=CheckStatus.NOT_APPLICABLE,
                checkable=False,
                confidence=0.5,
                notes="该属性未配置核对来源",
            )

        entry = self.port_bit(table_attr, port, bit)
        if entry is None:
            return AttributeResult(
                name=attr.name,
                label=attr.label,
                expected=attr.value,
                normalized=attr.normalized,
                actual="",
                status=CheckStatus.MISSING,
                checkable=True,
                confidence=0.6,
                notes=f"缺少端口位表 PORT_{port}_DEFAULT_{table_attr}",
            )

        actual = entry.value_raw
        same = self._same(attr, actual)
        change = None
        if not same:
            change = ProposedChange(
                type=ChangeType.SET_PORT_BIT,
                target=entry.id,
                old_value=entry.value_raw,
                new_value=attr.normalized,
                reason=(
                    f"L{entry.line} {entry.table}[{bit}]：期望 {attr.value}，实际 {entry.value_raw}"
                ),
            )
        return AttributeResult(
            name=attr.name,
            label=attr.label,
            expected=attr.value,
            normalized=attr.normalized,
            actual=actual,
            status=CheckStatus.MATCH if same else CheckStatus.MISMATCH,
            checkable=True,
            confidence=0.95,
            evidence=[
                Evidence(
                    entry_id=entry.id,
                    line=entry.line,
                    snippet=entry.raw_text.strip(),
                )
            ],
            change=change,
            notes=f"PORT_{port}_DEFAULT_{table_attr}[{bit}]",
        )

    # ---------- 冲突保护 ----------
    def _guard_conflicts(self, results: list[MatchResult]) -> None:
        """同一 (位表, 端口, 位, 属性) 被多行要求且期望值冲突 → 禁止自动改写。"""
        if not self.profile.c_cfg("conflict_guard", default=True):
            return
        buckets: dict[tuple[str, str, int, str], list[AttributeResult]] = {}
        for res in results:
            pin = parse_chip_pin(res.symbol)
            if pin is None:
                continue
            port, bit = pin
            for attr in res.attribute_results:
                if not attr.checkable or not attr.expected:
                    continue
                table_attr = self._table_attr(attr.name)
                if table_attr is None:
                    continue
                key = (table_attr, port, bit, attr.name)
                buckets.setdefault(key, []).append(attr)

        for (table_attr, port, bit, attr_name), attrs in buckets.items():
            values = {a.normalized for a in attrs if a.normalized}
            if len(values) <= 1:
                continue
            for attr in attrs:
                attr.status = CheckStatus.AMBIGUOUS
                attr.change = ProposedChange(
                    type=ChangeType.NONE,
                    target="",
                    old_value=attr.actual,
                    new_value=attr.normalized,
                    reason=(
                        f"PORT_{port}_DEFAULT_{table_attr}[{bit}] 被多行要求且期望值冲突"
                        f"（{'、'.join(sorted(values))}），需人工确认后再改写"
                    ),
                )

    # ---------- 工具 ----------
    def _table_attr(self, attr_name: str) -> str | None:
        source = self.profile.c_cfg("attribute_source", default={}) or {}
        node = source.get(attr_name)
        if isinstance(node, dict):
            return node.get("table")
        return None

    def _same(self, attr, actual: str) -> bool:
        if not attr.normalized:
            return True
        expected = attr.normalized
        value = (actual or "").strip().upper()
        if expected == value:
            return True
        push_pull = {"HIGH", "PP", "PUSH_PULL", "PUSHPULL"}
        open_drain = {"LOW", "OD", "OPEN_DRAIN", "OPENDRAIN"}
        if expected in push_pull and value in push_pull:
            return True
        if expected in open_drain and value in open_drain:
            return True
        direction = {"OUT": {"OUT", "OUTPUT"}, "IN": {"IN", "INPUT"}}
        for key, values in direction.items():
            if expected == key and value in values:
                return True
        return False

    @staticmethod
    def _worst(
        results: list[AttributeResult], default: CheckStatus
    ) -> CheckStatus:
        checkable = [r for r in results if r.checkable]
        if not checkable:
            return default
        return max((r.status for r in checkable), key=lambda s: SEVERITY.get(s, 0))
