"""RTK 规则细化：Excel C 列候选功能 vs .h 枚举成员 / 选中项。"""

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
        continue
    m = re_enum.match(line)
    if m:
        cur["members"].append((m.group(1), m.group(2)))


def norm(s: str) -> str:
    s = re.sub(r"\(.*?\)", " ", s or "")
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_").upper()


def strip_pad(name: str, pad: str) -> str:
    p = f"_PIN_{pad}_"
    return name[len(p):] if name.startswith(p) else name


# 抽样对照
for want in ("HDMI2_DET", "HDMI2_HPD", "DP1_HOT_PLUG", "LEDA", "EDID_WP", "PANEL_SCL"):
    b = next((x for x in blocks if norm(x["function"]) == norm(want)), None)
    if not b:
        print(f"--- {want}: 未找到区块")
        continue
    pad = b.get("pad", "?")
    mem = [strip_pad(n, pad) for n, _v in b["members"]]
    print(f"--- {want}  (pad={pad})  选中={b.get('selected')}")
    print(f"    枚举可选功能({len(mem)}): {mem}")

print()
print("=" * 100)
# Excel 侧对照
wb = load_workbook(x_path, data_only=True)
ws = wb["HSI"]
by_func = {}
for b in blocks:
    by_func.setdefault(norm(b["function"]), b)

print("Excel C 列候选功能 与 .h 枚举成员的交集情况（抽样 12 行）")
print(f"{'行':>4} {'网络名':<16} {'G':<5} {'C列候选(App优先)':<40} 枚举含App / 选中功能")
checked = 0
for r in range(6, ws.max_row + 1):
    net = str(ws.cell(r, 6).value or "").strip()
    gt = str(ws.cell(r, 7).value or "").strip().upper()
    pin_name = str(ws.cell(r, 3).value or "").strip()
    if not net or not gt or gt == "NA":
        continue
    b = by_func.get(norm(net))
    if not b:
        continue
    pad = b.get("pad", "?")
    mem = [norm(strip_pad(n, pad)) for n, _v in b["members"]]
    parts = [p.strip() for p in pin_name.split("/") if p.strip()]
    app = next((p for p in parts if "(App)" in p), parts[0] if parts else "")
    app_n = norm(app.replace("(App)", ""))
    hit = any(app_n in m or m in app_n for m in mem)
    sel = b.get("selected", "")
    sel_n = norm(sel)
    sel_in = any(sel_n == m or m in sel_n for m in mem)
    print(f"{r:>4} {net:<16} {gt:<5} {app_n:<40} "
          f"枚举含={hit}  选中={sel} (在枚举内={sel_in})")
    checked += 1
    if checked >= 12:
        break
