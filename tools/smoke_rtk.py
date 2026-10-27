"""RTK 端到端：Excel(HSI) × PINSHARE 头文件，核对 + 写回（副本上）。

python tools/smoke_rtk.py
"""

from __future__ import annotations

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
    detect_series,
    profile_for_series,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402


def main() -> int:
    rtk = ROOT / "samples" / "RTK"
    excels = list(rtk.glob("*.xlsx")) + list(rtk.glob("*.XLSX"))
    headers = list(rtk.glob("*.h"))
    if not excels or not headers:
        print("未找到 RTK 样例")
        return 1
    excel_src, c_src = excels[0], headers[0]

    tmp = Path(tempfile.mkdtemp(prefix="gbc_rtk_"))
    excel = tmp / excel_src.name
    cfile = tmp / c_src.name
    shutil.copy2(excel_src, excel)
    shutil.copy2(c_src, cfile)

    settings = load_settings()
    series = detect_series(cfile)
    profile = profile_for_series(settings, series)
    print(f"Excel：{excel_src.name}")
    print(f"配置：{c_src.name}")
    print(f"自动识别系列：{series.upper()}  档案：{profile.id}")
    print("=" * 100)

    uc = build_check_usecase(settings, profile)
    session = Session(excel_path=str(excel), c_path=str(cfile))
    result = uc.run(session, progress=lambda m, p: None, use_llm=True)

    print(f"Excel 行数 {result.summary.excel_rows}   状态分布 {result.summary.counts}")
    print(f"模型调用 {result.llm_calls} 次")
    reqs = {r.id: r for r in result.requirements}
    print("-" * 100)
    for res in result.results:
        req = reqs.get(res.requirement_id)
        if res.status.value == "not_applicable":
            continue
        print(f"  {req.net_name:<18} {res.status.value:<9} {res.notes[:80]}")

    print("-" * 100)
    apply_uc = ApplyUseCase()
    selected = {
        r.requirement_id
        for r in result.results
        if r.proposed_change.type.value in {"set_macro"}
    }
    print(f"可自动应用条目：{len(selected)} 项")
    outcome = apply_uc.apply(session, selected)
    print(f"应用结果：{outcome.message}")
    if outcome.diff:
        print(outcome.diff)
    if outcome.semantic:
        print(
            f"复检：修复 {len(outcome.semantic.fixed)} / 剩余 {len(outcome.semantic.remaining)}"
            f" / 新增 {len(outcome.semantic.introduced)}"
        )
        for item in outcome.semantic.remaining:
            print("   !", item)
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
