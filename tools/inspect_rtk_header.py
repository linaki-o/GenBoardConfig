"""RTK 样例探查：.h（PINSHARE）结构解析 v2。"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = next((ROOT / "samples" / "RTK").glob("*.h"))
text = path.read_text(encoding="utf-8", errors="replace")
lines = text.split("\n")
print(f"文件：{path.name}  行数：{len(lines)}")

re_func = re.compile(r"^//\s*Function\s*:\s*(.+?)\s*$")
re_define = re.compile(r"^#define\s+(_PIN_[A-Z]+\d+)\s+\(\s*(_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*\)")
re_enum = re.compile(r"^\s*(_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*=\s*(0x[0-9A-Fa-f]+|_PIN_[A-Z]+\d+_[A-Za-z0-9_]+)\s*,")

blocks = []
cur = None
for i, line in enumerate(lines, 1):
    m = re_func.match(line)
    if m:
        cur = {"line": i, "function": m.group(1), "members": [], "define": None}
        blocks.append(cur)
        continue
    if cur is None:
        continue
    m = re_define.match(line)
    if m:
        cur["define"] = (m.group(1), m.group(2))
        cur["pad"] = m.group(1)[len("_PIN_"):]
        cur["selected"] = m.group(2)[len(m.group(1)) + 1:]
        continue
    m = re_enum.match(line)
    if m:
        cur["members"].append((m.group(1), m.group(2)))

print(f"解析到 {len(blocks)} 个引脚区块；带 #define 的 {sum(1 for b in blocks if b.get('define'))}")

kinds = Counter()
for b in blocks:
    sel = b.get("selected")
    if not sel:
        continue
    pad = b["pad"]
    kinds[sel[len(pad) + 1:].split("_")[0] if sel.startswith(pad + "_") else "?"] += 1
print("选中功能类型分布：", dict(kinds.most_common()))

mem_kinds = Counter()
for b in blocks:
    pad = b.get("pad")
    for name, _v in b["members"]:
        tail = name[len(pad) + 1:] if pad and name.startswith(pad + "_") else "?"
        mem_kinds[tail.split("_")[0]] += 1
print("枚举成员类型 Top15：", dict(mem_kinds.most_common(15)))

# 名称里含 App / GPIO / NC 的成员
print()
print("=== 含特殊关键字的枚举成员 ===")
special = Counter()
for b in blocks:
    pad = b.get("pad") or ""
    for name, _v in b["members"]:
        tail = name[len(pad) + 1:] if name.startswith(pad + "_") else name
        for kw in ("GPIO", "GPI", "GPO", "PWM", "NC", "TEST", "SCL", "SDA", "UART", "IRQ", "HPD", "DET"):
            if kw in tail:
                special[kw] += 1
print(dict(special.most_common()))

print()
print("=== 无 #define 的区块样例（首个与 3 个中间） ===")
no_def = [b for b in blocks if not b.get("define")]
for b in no_def[:4]:
    print(f"  L{b['line']} Function={b['function']}  成员数={len(b['members'])}")
    for name, val in b["members"][:6]:
        print(f"        {name} = {val}")

print()
print("=== 特殊行：非注释、非 enum 的其它内容 ===")
other = []
for i, line in enumerate(lines, 1):
    s = line.strip()
    if not s or s.startswith("//") or s.startswith("*") or s.startswith("/*"):
        continue
    if re_define.match(line) or re_enum.match(line):
        continue
    if s.startswith("}") or s.startswith("{") or s.startswith("typedef"):
        continue
    other.append((i, s[:90]))
for i, s in other[:25]:
    print(f"  {i:5d}: {s}")
print(f"  ... 共 {len(other)} 行")
