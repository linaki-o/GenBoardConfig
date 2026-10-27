"""RTK 样例结构探查：Excel 侧。"""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
path = next((ROOT / "samples" / "RTK").glob("*.XLSX")) or next(
    (ROOT / "samples" / "RTK").glob("*.xlsx")
)
print("文件：", path.name)

wb = load_workbook(path, data_only=True)
print("SHEETS:", wb.sheetnames)
for ws in wb.worksheets:
    print("=" * 110)
    print(f"--- {ws.title} dims={ws.dimensions} rows={ws.max_row} cols={ws.max_column}")
    for r in range(1, min(ws.max_row, 24) + 1):
        vals = []
        for c in range(1, min(ws.max_column, 14) + 1):
            v = ws.cell(r, c).value
            if v is not None:
                text = str(v).replace("\n", " ")[:38]
                vals.append(f"{ws.cell(r, c).coordinate}={text}")
        if vals:
            print(f"R{r}: " + " | ".join(vals))
