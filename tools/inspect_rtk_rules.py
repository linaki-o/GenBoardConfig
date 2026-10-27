"""RTK 核对规则可行性分析：量化各层判定分布。"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
rtk_dir = ROOT / "samples" / "RTK"
h_path = next(rtk_dir.glob("*.h"))
x_path = next(rtk_dir.glob("*.XLSX"))

lines = h_path.read_text(encoding="utf-8", errors="replace").split("\n")
re_func = re.compile(r"^//\s*Function\s*:\s*(.+?)\s*$")
re_define = re.compile(r"^#define\s+(_PIN_[A-Z]+\d+)\s+\(\s*(_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*\)")
re_enum = re.compile(r"^\s*(_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*=\s*(0x[0-9A-Fa-f]+|_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*,")

blocks = []
cur = None
for i, line in enumerate(lines, 1):
    m = re_func.match(line)
    if m:
        cur = {"line": i, "function": m.group(1), "members": []}
        blocks.append(cur)
        continue
    if cur is None:
        continue
    m = re_define.match(line)
    if m:
        cur["pad"] = m.group(1)[len("_PIN_"):]
        cur["selected"] = m.group(2)[len(m.group(1)) + 1:]
        cur["define_line"] = i
        cur["off_region"] = m.group(1).endswith("_OFF_REGION")
        continue
    m = re_enum.match(line)
    if m:
        cur["members"].append((m.group(1), m.group(2)))

# 归一化网络名
def norm(s: str) -> str:
    s = re.sub(r"\(.*?\)", " ", s or "")          # 去括号说明
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper()
    return s

by_func = {}
for b in blocks:
    by_func.setdefault(norm(b["function"]), []).append(b)

# Excel
wb = load_workbook(x_path, data_only=True)
ws = wb["HSI"]
rows = []
for r in range(6, ws.max_row + 1):
    g = lambda c: ws.cell(r, c).value  # noqa: E731
    rows.append({
        "row": r,
        "pin_name": str(g(3) or "").strip(),
        "net": str(g(6) or "").strip(),
        "gpio_type": str(g(7) or "").strip().upper(),
        "io_type": str(g(8) or "").strip(),
        "power_on": str(g(9) or "").strip().upper(),
    })

# 类型映射
TYPE_MAP = {
    "IN": {"GPI"},
    "OUT": {"GPO_PP", "GPO_OD"},
    "SCL": {"DDCSCL", "SCL", "EEIICSCL", "IICSCL", "AUDIO_SCL", "TXD_SCL", "RXD_SCL"},
    "SDA": {"DDCSDA", "SDA", "EEIICSDA", "IICSDA", "AUDIO_SDA", "TXD_SDA", "RXD_SDA"},
    "ADC": {"ADC", "A", "ABIAS"},
}
IO_MAP = {"OPEN-DRAIN OUTPUT": "GPO_OD", "PUSH-PULL OUTPUT": "GPO_PP",
          "OPEN DRAIN": "GPO_OD", "PUSH PULL": "GPO_PP"}

def sel_kind(sel: str) -> str:
    return sel.split("_")[0] if sel else ""

def app_func(pin_name: str) -> str:
    parts = [p.strip() for p in pin_name.split("/") if p.strip()]
    app = next((p for p in parts if "(App)" in p), parts[0] if parts else "")
    return norm(app.replace("(App)", ""))

stats = Counter()
detail = []
for r in rows:
    gt = r["gpio_type"]
    if not gt or gt == "NA":
        stats["跳过(GPIO TYPE 为空/NA)"] += 1
        continue
    stats["参与核对"] += 1
    net = r["net"]
    if not net:
        stats["无网络名 → 无法定位 .h 区块"] += 1
        detail.append((r, None, "无网络名"))
        continue
    cand = by_func.get(norm(net))
    if not cand:
        stats[".h 中无该网络名区块 → 缺失"] += 1
        detail.append((r, None, "缺失"))
        continue
    b = cand[0]
    sel = b.get("selected", "")
    kind = sel_kind(sel)
    # L1 类型层
    exp_kinds = TYPE_MAP.get(gt, set())
    type_ok = kind in exp_kinds
    # L1b 输出一致性
    io_key = IO_MAP.get(r["io_type"].upper())
    io_ok = (io_key is None) or (io_key == kind)
    # L2 功能名层
    exp_fn = app_func(r["pin_name"])
    name_ok = exp_fn == norm(sel) or norm(sel) in exp_fn or exp_fn in norm(sel)
    if not type_ok:
        stats["L1 类型不符 → 不一致"] += 1
        verdict = "不一致(类型)"
    elif not io_ok:
        stats["L1b 输出类型不符 → 不一致"] += 1
        verdict = "不一致(开漏/推挽)"
    elif name_ok:
        stats["功能名一致 → 一致"] += 1
        verdict = "一致"
    else:
        stats["功能名不同但类型相符 → 需语义判定"] += 1
        verdict = "歧义(语义)"
    detail.append((r, b, verdict))

print("=== 判定分层统计 ===")
for k, v in stats.most_common():
    print(f"  {k:<34} {v}")

print("\n=== 需语义判定的行（Excel 期望功能 vs .h 实际） ===")
for r, b, verdict in detail:
    if verdict == "歧义(语义)":
        exp_fn = app_func(r["pin_name"])
        print(f"  行{r['row']:<4} {r['net']:<18} 期望={exp_fn:<24} .h={b.get('selected',''):<18} "
              f"pad={b.get('pad')}  G={r['gpio_type']} H={r['io_type']}")

print("\n=== 明确不一致的行 ===")
for r, b, verdict in detail:
    if verdict.startswith("不一致"):
        print(f"  行{r['row']:<4} {r['net']:<18} G={r['gpio_type']:<5} H={r['io_type']:<18} "
              f".h={b.get('selected',''):<14} pad={b.get('pad')}  ({verdict})")

print("\n=== .h 中缺失的网络名 ===")
miss = [(r["row"], r["net"]) for r, b, v in detail if v == "缺失"]
print(" ", miss)
