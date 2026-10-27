"""语义复检：修改后重新解析并核对，确认差异消除且未引入新差异。"""

from __future__ import annotations

from dataclasses import dataclass, field

from ...domain.hsi import HsiEngine
from ...domain.models import CheckResult, CheckStatus
from ...domain.profiles import Profile
from ..cconfig.parser import CConfigParser


@dataclass
class SemanticReport:
    level: str = "pass"        # pass | warn | fail
    fixed: list[str] = field(default_factory=list)
    introduced: list[str] = field(default_factory=list)
    remaining: list[str] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)


def recheck(
    new_text: str,
    before: CheckResult,
    parser: CConfigParser | None = None,
    encoding: str = "utf-8",
    newline: str = "\n",
    profile: Profile | None = None,
    overrides: dict[str, str] | None = None,
) -> SemanticReport:
    """在内存中重新解析并与期望对比。"""
    parser = parser or CConfigParser()
    report = SemanticReport()

    after = parser.parse_text(new_text, encoding=encoding, newline=newline)

    if profile is not None:
        return _recheck_profile(report, after, before, profile, overrides)

    after_by_key: dict[str, list] = {}
    for entry in after.entries:
        after_by_key.setdefault(entry.key_norm, []).append(entry)

    before_status = {r.requirement_id: r for r in before.results}
    for req in before.requirements:
        old = before_status.get(req.id)
        if old is None:
            continue
        entries = after_by_key.get(req.config_key_norm, [])
        current = entries[0].value_raw if entries else ""
        still_bad = not current or current.strip().upper() != req.expected_value.strip().upper()
        was_bad = old.status in {CheckStatus.MISMATCH, CheckStatus.MISSING}
        if was_bad and not still_bad:
            report.fixed.append(f"{req.id} {req.config_key or req.function_name}")
        elif was_bad and still_bad:
            report.remaining.append(
                f"{req.id} {req.config_key or req.function_name}: 期望 {req.expected_value}，实际 {current or '(缺失)'}"
            )
        if old.status == CheckStatus.MATCH and still_bad and entries:
            report.introduced.append(
                f"{req.id} {req.config_key or req.function_name}: 原本一致，修改后变为 {current}"
            )

    if report.remaining:
        report.level = "warn"
        report.messages.append(f"仍有 {len(report.remaining)} 条差异未消除")
    if report.introduced:
        report.level = "fail"
        report.messages.append(f"引入了 {len(report.introduced)} 条新差异")
    return report


def _make_engine(profile: Profile, entries):
    """按档案类型构造核对引擎。"""
    if profile.c_cfg("kind") == "pinshare":
        from ...domain.rtk import RtkEngine

        return RtkEngine(profile, entries)
    from ...domain.hsi import HsiEngine

    return HsiEngine(profile, entries)


def _recheck_profile(
    report: SemanticReport,
    after,
    before: CheckResult,
    profile: Profile,
    overrides: dict[str, str] | None,
) -> SemanticReport:
    """档案模式：重跑逐属性核对，按属性比较前后状态。"""
    engine = _make_engine(profile, after.entries)
    new_results = engine.check(before.requirements)
    old_by_id = {r.requirement_id: r for r in before.results}
    reqs = {r.id: r for r in before.requirements}

    for res in new_results:
        old = old_by_id.get(res.requirement_id)
        if old is None:
            continue
        req = reqs.get(res.requirement_id)
        label = req.net_name if req and req.net_name else res.requirement_id
        new_attrs = {a.name: a for a in res.attribute_results}
        for old_attr in old.attribute_results:
            new_attr = new_attrs.get(old_attr.name)
            if new_attr is None:
                continue
            name = f"{label}·{old_attr.label}"
            if old_attr.status == CheckStatus.MISMATCH:
                if new_attr.status == CheckStatus.MATCH:
                    report.fixed.append(name)
                else:
                    report.remaining.append(
                        f"{name}: 期望 {old_attr.expected}，实际 {new_attr.actual or '(缺失)'}"
                    )
            elif old_attr.status == CheckStatus.MATCH and new_attr.status == CheckStatus.MISMATCH:
                report.introduced.append(
                    f"{name}: 原本一致，修改后变为 {new_attr.actual}"
                )

    if report.remaining:
        report.level = "warn"
        report.messages.append(f"仍有 {len(report.remaining)} 条差异未消除")
    if report.introduced:
        report.level = "fail"
        report.messages.append(f"引入了 {len(report.introduced)} 条新差异")
    return report
