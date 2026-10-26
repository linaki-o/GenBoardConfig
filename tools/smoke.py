"""端到端冒烟测试（离屏，无需 GUI 显示）。"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from genboardconfig.app.check_usecase import CheckUseCase  # noqa: E402
from genboardconfig.app.apply_usecase import ApplyUseCase  # noqa: E402
from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
)
from genboardconfig.infra.settings import load_settings  # noqa: E402

sys.path.insert(0, str(ROOT / "tools"))
from sample_gen import build_c, build_excel  # noqa: E402


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="gbc_smoke_"))
    excel = tmp / "gpio_table_sample.xlsx"
    cfile = tmp / "board_config_sample.c"
    build_excel(excel)
    build_c(cfile)

    settings = load_settings()
    settings.set("llm.provider", "mock")
    usecase = build_check_usecase(settings)

    session = Session(excel_path=str(excel), c_path=str(cfile))
    result = usecase.run(session, progress=lambda m, p: None, use_llm=True)

    print("=" * 72)
    print(f"Excel 行数: {result.summary.excel_rows}   C 条目: {result.summary.c_entries}")
    print(f"状态分布: {result.summary.counts}")
    print(f"模型调用: {result.llm_calls}  tokens: {result.llm_tokens}")
    print("=" * 72)
    reqs = {r.id: r for r in result.requirements}
    for res in result.results:
        req = reqs.get(res.requirement_id)
        print(
            f"[{res.status.value:<14}] {req.pin_name_raw:<12} {req.config_key:<22} "
            f"期望={res.expected_value:<8} 实际={res.current_value:<12} "
            f"置信={res.confidence:.2f}  {res.notes}"
        )

    # 应用修改到副本
    apply_uc = ApplyUseCase()
    selected = {
        r.requirement_id
        for r in result.results
        if r.proposed_change.type.value in {"set_macro", "set_struct_field", "set_array_item"}
    }
    print("-" * 72)
    print(f"待应用条目: {sorted(selected)}")
    outcome = apply_uc.apply(session, selected)
    print(f"应用结果: {outcome.message}")
    print(f"备份: {outcome.backup_path}")
    print(outcome.diff)
    if outcome.semantic:
        print(f"复检: 修复 {len(outcome.semantic.fixed)} / 剩余 {len(outcome.semantic.remaining)} / 新增 {len(outcome.semantic.introduced)}")
    print("-" * 72)
    print("修改后文件片段：")
    for line in cfile.read_text(encoding="utf-8").splitlines():
        if "LED3" in line or "KEY2" in line:
            print("   ", line)

    shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
