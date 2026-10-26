"""HSI 档案：行过滤与逐属性比对的端到端验证。

构造一份「GPIO TYPE 列已填写」的 HSI 表，验证：
- 只处理 HSI Sheet；
- 只处理 GPIO TYPE 列为 IN / OUT 的行；
- 其余行（空值 / 其它取值）被跳过并计入统计；
- 核对目标仅为 PORT_X_DEFAULT_{OUT,DIR,PP,PU} 位表。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from openpyxl import Workbook  # noqa: E402

from genboardconfig.app.context import Session  # noqa: E402
from genboardconfig.app.service_factory import (  # noqa: E402
    build_check_usecase,
    detect_profile,
    load_profiles,
)
from genboardconfig.domain.models import CheckStatus  # noqa: E402
from genboardconfig.infra.settings import load_settings  # noqa: E402

HEADERS = [
    "PIN #", "Chip Section", "PIN Name ", "Description/ Function", "AI",
    "Schematic Function", "GPIO  TYPE(输入输出类别)", "Output PIN 设定类型",
    "Power On", "Power Saving", "Power Off", "F/W Check", "EE Check",
]

# (封装脚位, Chip Section, PIN Name, Description/Function, AI, Schematic Function,
#  GPIO TYPE, Output PIN 设定类型, Power On, Power Saving, Power Off)
ROWS = [
    ("C4", "Output", "PA2", "PA2/ADC6/PWMC", "", "+3V3C_EN", "OUT", "Open Drain", "High", "Low", "Low"),
    ("E14", "Output", "PB6/DPRX1_HPD", "PB6*/DDC_SCL1", "", "DP_HPD", "OUT", "Push pull", "Low", "High", "High"),
    ("F20", "Output", "PC1", "PC1*/CEC1", "", "ON_BACKLIGHT", "OUT", "Push pull", "High", "Low", "Low"),
    ("G11", "Output", "PD1", "PD1*/PWMB", "", "+1VC_EN", "OUT", "Open Drain", "High", "Low", "Low"),
    ("F4", "Output", "PD2", "PD2*/PWMC", "", "EE_SCL", "OUT", "Open Drain", "High", "Low", "Low"),
    ("F13", "Output", "PE1", "PE1*/IIS_OB_MCLK", "", "EE_WP", "OUT", "Open Drain", "High", "High", "High"),
    ("F16", "Output", "PE2", "PE2*/IIC_SCL6", "", "LED_Y_C", "OUT", "Open Drain", "Low", "Low", "High"),
    ("E17", "Output", "PE5", "PE5*/DP1_HPD", "", "HDMI1_HPD", "OUT", "Open Drain", "High", "Low", "Low"),
    ("E3", "Output", "PF0", "PF0*/INTE0", "", "DDR_1.5V_EN", "OUT", "Open Drain", "High", "High", "Low"),
    ("G21", "Output", "PK1/PWMB", "PK1*/UTX5", "", "BL_ADIM", "OUT", "Push pull", "HIGH", "Low", "Low"),
    # ↓ 以下三类应被过滤掉
    ("A1", "Input", "PG3", "PG3*/ADC", "", "KEY_IN", "IN", "NA", "Low", "Low", "Low"),      # IN → 应参与
    ("A2", "Input", "PG4", "PG4*/ADC", "", "ADC_IN", "", "NA", "Low", "Low", "Low"),        # 空 → 应跳过
    ("A3", "Input", "PG5", "PG5*/ADC", "", "OTHER", "Analog", "NA", "Low", "Low", "Low"),   # 其它取值 → 应跳过
]


def build_excel(path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "HSI"
    ws["A1"] = "Hardware_Software_Interface Setting & Check"
    ws["A3"] = "Note: ..."
    ws.append(HEADERS)
    for row in ROWS:
        ws.append(list(row) + ["PASS", "PASS"])
    # 干扰 Sheet：不应参与
    other = wb.create_sheet("Other Requirements")
    other.append(["Check Item"])
    other.append(["与 GPIO 无关的检查项"])
    wb.save(path)


def main() -> int:
    tmp = Path(__file__).resolve().parent.parent / "samples" / "_tmp_filter_test"
    tmp.mkdir(parents=True, exist_ok=True)
    excel = tmp / "hsi_with_gpio_type.xlsx"
    build_excel(excel)

    settings = load_settings()
    profile = detect_profile(str(excel), load_profiles(settings))
    print(f"档案：{profile.id}（目标 Sheet：{profile.excel_sheet}）")
    print(f"行过滤：{profile.filter_field} ∈ {profile.filter_values}")
    print("-" * 96)

    usecase = build_check_usecase(settings, profile)
    session = Session(
        excel_path=str(excel), c_path=str(ROOT / "samples" / "BoardCfg.h")
    )
    result = usecase.run(session, progress=lambda m, p: None, use_llm=True)

    stats = result.extra.get("filter_stats") or {}
    print(f"过滤列已映射：{stats.get('mapped')}")
    print(
        f"参与 {stats.get('kept')} 行 / 跳过 {stats.get('skipped')} 行 "
        f"（跳过取值分布 {stats.get('skipped_values')}）"
    )
    print(f"状态分布：{result.summary.counts}")
    print("-" * 96)
    reqs = {r.id: r for r in result.requirements}
    for res in result.results:
        req = reqs[res.requirement_id]
        diffs = [
            f"{a.label}: 期望{a.expected}/实际{a.actual}"
            for a in res.attribute_results
            if a.status == CheckStatus.MISMATCH
        ]
        print(f"  {req.net_name:<14} {req.pin_name_raw:<14} {res.status.value:<9} {'；'.join(diffs)}")

    ok = True
    kept_pins = {reqs[r.requirement_id].pin_name_raw for r in result.results}
    if "PG4" in kept_pins or "PG5" in kept_pins:
        print("!! 非 IN/OUT 行被错误纳入")
        ok = False
    if "PG3" not in kept_pins:
        print("!! IN 行未被纳入")
        ok = False
    print("-" * 96)
    print("过滤行为验证：", "通过" if ok else "失败")
    print(f"（临时文件：{excel}）")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
