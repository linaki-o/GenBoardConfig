"""RTK 核对规则量化（修正类型判定后）。"""

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

blocks, cur = [], None
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


GENERIC = {"GPI", "GPO_PP", "GPO_OD"}
by_func = {}
for b in blocks:
    by_func.setdefault(norm(b["function"]), b)

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
        "io_type": str(g(8) or "").strip().upper(),
        "power_on": str(g(9) or "").strip().upper(),
    })

stats = Counter()
rows_out = []
for r in rows:
    gt, net = r["gpio_type"], r["net"]
    if gt in ("", "NA"):
        stats["0 跳过（G列空/NA）"] += 1
        continue
    if not net:
        stats["1 跳过（无网络名）"] += 1
        continue
    b = by_func.get(norm(net))
    if b is None:
        stats["2 .h 无该网络名区块 → 缺失/待确认"] += 1
        rows_out.append((r, None, "缺失", ""))
        continue
    pad = b.get("pad", "?")
    sel = b.get("selected", "")
    mem = [norm(strip_pad(n, pad)) for n, _v in b["members"]]
    parts = [p.strip() for p in r["pin_name"].split("/") if p.strip()]
    app = next((p for p in parts if "(App)" in p), parts[0] if parts else "")
    app_n = norm(app.replace("(App)", ""))

    # 功能名是否在 .h 枚举中可用
    app_available = any(app_n == m or app_n in m or m in app_n for m in mem)
    # .h 实际选中的功能（归一）
    sel_n = norm(sel)
    if sel in GENERIC:
        elec_ok = (
            (gt == "IN" and sel == "GPI")
            or (gt == "OUT" and sel in {"GPO_PP", "GPO_OD"})
        )
        io_expect = {"OPEN-DRAIN OUTPUT": "GPO_OD", "PUSH-PULL OUTPUT": "GPO_PP"}.get(r["io_type"])
        io_ok = io_expect is None or io_expect == sel
        if not elec_ok:
            stats["3 方向/类型不符 → 不一致"] += 1
            verdict = "不一致(方向/类型)"
        elif not io_ok:
            stats["4 开漏/推挽不符 → 不一致"] += 1
            verdict = "不一致(开漏/推挽)"
        else:
            stats["5 通用GPIO实现，电气符合 → 一致"] += 1
            verdict = "一致(通用GPIO实现)"
        detail = f".h={sel}"
    else:
        # 专用功能
        if app_n and (app_n == sel_n or app_n in sel_n or sel_n in app_n):
            stats["6 专用功能且功能名一致 → 一致"] += 1
            verdict = "一致(功能名一致)"
        else:
            stats["7 专用功能但名称/类别待语义判定 → 歧义"] += 1
            verdict = "歧义(语义)"
        detail = f".h={sel}"
    rows_out.append((r, b, verdict, detail))

print("=== RTK 核对分层统计 ===")
for k, v in sorted(stats.items()):
    print(f"  {k:<38} {v}")

print("\n=== 明确不一致（可直接脚本判定） ===")
for r, b, v, d in rows_out:
    if v.startswith("不一致"):
        print(f"  行{r['row']:<4} {r['net']:<18} G={r['gpio_type']:<5} H={r['io_type']:<19} {d:<12} pad={b.get('pad')}")

print("\n=== 需语义判定（专用功能但与 Excel (App) 名不一致） ===")
for r, b, v, d in rows_out:
    if v == "歧义(语义)":
        parts = [p.strip() for p in r["pin_name"].split("/") if p.strip()]
        app = next((p for p in parts if "(App)" in p), parts[0] if parts else "")
        print(f"  行{r['row']:<4} {r['net']:<18} 期望(App)={app.replace('(App)',''):<22} {d:<16} G={r['gpio_type']}")

print("\n=== 缺失清单（G列有值但 .h 无对应区块） ===")
miss = [(r["row"], r["net"], r["gpio_type"]) for r, b, v, d in rows_out if v == "缺失"]
for row, net, gt in miss:
    print(f"  行{row:<4} {net:<22} G={gt}")
