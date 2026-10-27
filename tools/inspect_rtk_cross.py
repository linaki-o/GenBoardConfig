"""RTK 样例探查：.h 引脚区块 × Excel HSI 行 的交叉核对。"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
rtk_dir = ROOT / "samples" / "RTK"
h_path = next(rtk_dir.glob("*.h"))
x_path = next(p for p in rtk_dir.glob("*.XLSX")) if list(rtk_dir.glob("*.XLSX")) else next(rtk_dir.glob("*.xlsx"))

text = h_path.read_text(encoding="utf-8", errors="replace")
lines = text.split("\n")

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
        cur["selected_sym"] = m.group(2)
        cur["selected"] = m.group(2)[len(m.group(1)) + 1:]
        cur["define_line"] = i
        continue
    m = re_enum.match(line)
    if m:
        cur["members"].append((m.group(1), m.group(2)))

print(f"{h_path.name}: {len(blocks)} 区块 / {sum(1 for b in blocks if b.get('selected'))} 个带 #define")
kinds = Counter()
for b in blocks:
    sel = b.get("selected")
    if sel:
        kinds[sel.split("_")[0]] += 1
print("选中功能类型：", dict(kinds.most_common()))

# ---- Excel 侧 ----
wb = load_workbook(x_path, data_only=True)
ws = wb["HSI"]
rows = []
for r in range(6, ws.max_row + 1):
    g = lambda c: (ws.cell(r, c).value or "")  # noqa: E731
    rows.append(
        {
            "row": r,
            "pin_no": str(g(1)).strip(),
            "chip_section": str(g(2)).strip(),
            "pin_name": str(g(3)).strip(),
            "gpio_init": str(g(5)).strip(),
            "net": str(g(6)).strip(),
            "gpio_type": str(g(7)).strip().upper(),
            "io_type": str(g(8)).strip(),
            "power_on": str(g(9)).strip().upper(),
            "power_saving": str(g(10)).strip().upper(),
            "power_off": str(g(11)).strip().upper(),
        }
    )
print(f"\nExcel HSI 数据行：{len(rows)}")
print("GPIO TYPE 取值分布：", dict(Counter(r["gpio_type"] for r in rows).most_common()))
print("输出类型取值分布：", dict(Counter(r["io_type"] for r in rows).most_common()))
print("上电电平取值分布：", dict(Counter(r["power_on"] for r in rows).most_common()))
print("GPIO Init(E列) 非空行数：", sum(1 for r in rows if r["gpio_init"]))

# ---- 交叉匹配 ----
by_func = {b["function"].strip().upper(): b for b in blocks}
print("\n=== Excel 网络名 → .h Function 匹配情况 ===")
matched = 0
unmatched = []
for r in rows:
    net = r["net"].strip()
    if not net:
        continue
    key = net.upper()
    b = by_func.get(key)
    if b is None:
        b = by_func.get(key.replace("-", "_"))
    if b is None:
        unmatched.append((r["row"], net))
    else:
        matched += 1
print(f"有网络名的行匹配到 .h 区块：{matched}；未匹配：{len(unmatched)}")
print("未匹配样例：", unmatched[:12])

# 详细对照（前 20 个匹配行）
print("\n=== 逐行对照（Excel 期望 vs .h 实际） ===")
print(f"{'行':>4} {'网络名':<18} {'G':<6} {'H列':<18} {'期望(App)功能':<22} "
      f"{'.h 选中':<16} {'pad':<6} {'一致?'}")
for r in rows[:200]:
    net = r["net"].strip()
    if not net:
        continue
    b = by_func.get(net.upper())
    if not b:
        continue
    names = [x.strip() for x in r["pin_name"].split("/") if x.strip()]
    app = next((n for n in names if "(App)" in n), names[0] if names else "")
    app_clean = app.replace("(App)", "").strip()
    sel = b.get("selected", "-")
    sel_clean = sel.replace("GPO_PP", "PP").replace("GPO_OD", "OD")
    ok = "✓" if app_clean.upper() in sel_clean.upper() or sel_clean.upper() in app_clean.upper() else "✗"
    print(f"{r['row']:>4} {net:<18} {r['gpio_type']:<6} {r['io_type']:<18} {app_clean:<22} "
          f"{sel:<16} {b.get('pad','-'):<6} {ok}")
    if r["row"] > 40:
        break
