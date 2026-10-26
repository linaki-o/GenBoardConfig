"""临时验证：把行过滤列切到 chip_section，检查端口位表链路是否通。"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    detect_profile,
    load_profiles,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402


def main() -> int:
    settings = load_settings()
    excel = glob.glob(str(ROOT / "samples" / "*.xlsx"))[0]
    cfile = str(ROOT / "samples" / "BoardCfg.h")
    profile = detect_profile(excel, load_profiles(settings))

    uc = build_check_usecase(settings, profile)
    session = Session(excel_path=excel, c_path=cfile)
    result = uc.run(session, progress=lambda m, p: None, use_llm=True)
    print("【按 GPIO TYPE 列过滤】")
    print("  参与核对行数:", result.summary.excel_rows)
    for w in result.warnings:
        print("  警告:", w)
    print("  过滤统计:", result.extra.get("filter_stats"))

    print()
    print("【临时把过滤列切到 chip_section，验证端口位表链路】")
    profile.row_filter = {
        "field": "chip_section",
        "values": ["Output", "Input"],
        "empty_hint": "",
    }
    uc2 = build_check_usecase(settings, profile)
    session2 = Session(excel_path=excel, c_path=cfile)
    result2 = uc2.run(session2, progress=lambda m, p: None, use_llm=True)
    print("  参与核对行数:", result2.summary.excel_rows, "状态:", result2.summary.counts)
    reqs = {r.id: r for r in result2.requirements}
    for res in result2.results:
        req = reqs[res.requirement_id]
        bad = [
            f"{a.label}: 期望{a.expected}/实际{a.actual}"
            for a in res.attribute_results
            if a.status.value == "mismatch"
        ]
        print(f"  {req.pin_name_raw:<14} {res.status.value:<9} {'；'.join(bad)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
