"""真实样例端到端冒烟：HSI Excel + BoardCfg.h。

注意：永远在临时目录的副本上做写回测试，绝不改动 samples/ 下的原文件。
"""

from __future__ import annotations

import glob
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from genboardconfig.app.apply_usecase import ApplyUseCase  # noqa: E402
from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    detect_profile,
    load_profiles,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402


def main() -> int:
    samples = ROOT / "samples" / "NTK"
    excels = [p for p in samples.glob("*.xlsx")]
    headers = [p for p in samples.glob("*.h")] + [p for p in samples.glob("*.c")]
    if not excels or not headers:
        print("未找到样例文件")
        return 1
    excel_src, c_src = excels[0], headers[0]

    tmp = Path(tempfile.mkdtemp(prefix="gbc_real_"))
    excel = tmp / excel_src.name
    cfile = tmp / c_src.name
    shutil.copy2(excel_src, excel)
    shutil.copy2(c_src, cfile)

    settings = load_settings()
    profiles = load_profiles(settings)
    profile = detect_profile(excel, profiles)
    print(f"Excel：{excel_src.name}")
    print(f"C 配置：{c_src.name}")
    print(f"档案：{profile.id if profile else '无（通用模式）'}")
    print("=" * 100)

    uc = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    result = uc.run(session, progress=lambda m, p: None, use_llm=True)

    print(f"Excel 行数 {result.summary.excel_rows}   C 条目 {result.summary.c_entries}")
    print(f"状态分布：{result.summary.counts}")
    stats = result.extra.get("filter_stats") or {}
    if stats:
        used = stats.get("used_field") or stats.get("field")
        values = stats.get("used_values") or stats.get("values")
        tag = "（回退）" if stats.get("fallback") else ""
        print(
            f"行过滤{tag}：{used} ∈ {values} → "
            f"参与 {stats.get('kept')} 行 / 跳过 {stats.get('skipped')} 行 "
            f"（跳过取值分布 {stats.get('skipped_values')}）"
        )
    for w in result.warnings:
        print(f"  警告：{w}")
    print("-" * 100)
    reqs = {r.id: r for r in result.requirements}
    for res in result.results:
        req = reqs.get(res.requirement_id)
        head = f"{req.net_name:<14} {req.pin_name_raw:<14} {res.symbol or '-':<18} {res.status.value:<10}"
        print(head)
        for attr in res.attribute_results:
            mark = " " if attr.status.value in {"match", "not_applicable"} else "*"
            print(
                f"    {mark} {attr.label:<6} 期望 {str(attr.expected or '-'):<10} "
                f"实际 {str(attr.actual or '-'):<22} {attr.status.value:<10} {attr.notes[:60]}"
            )

    print("-" * 100)
    apply_uc = ApplyUseCase()
    selected = {
        r.requirement_id
        for r in result.results
        if r.proposed_change.type.value in {"set_macro", "set_port_bit"}
    }
    print(f"可自动应用条目：{sorted(selected)}")
    outcome = apply_uc.apply(session, selected)
    print(f"应用结果：{outcome.message}")
    if outcome.diff:
        print(outcome.diff)
    if outcome.semantic:
        print(
            f"复检：修复 {len(outcome.semantic.fixed)} / 剩余 {len(outcome.semantic.remaining)}"
            f" / 新增 {len(outcome.semantic.introduced)}"
        )
        for item in outcome.semantic.fixed:
            print(f"   ✔ {item}")
        for item in outcome.semantic.remaining:
            print(f"   ! {item}")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
