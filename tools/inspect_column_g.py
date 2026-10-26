"""核查 HSI Sheet 的 G 列（raw XML 级别，绕过 openpyxl）。"""

from __future__ import annotations

import glob
import re
import zipfile
from pathlib import Path

path = glob.glob(r"D:\lk__tool\GenBoardConfig\samples\*.xlsx")[0]
z = zipfile.ZipFile(path)
xml = z.read("xl/worksheets/sheet2.xml").decode("utf-8")  # HSI

print(f"文件：{Path(path).name}")
print(f"HSI sheet2.xml 长度：{len(xml)}")

row6 = re.search(r'<row r="6".*?</row>', xml, re.S)
print()
print("第 6 行原始 XML：")
print(row6.group(0) if row6 else "(无)")

g_cells = re.findall(r'<c r="G(\d+)"', xml)
print()
print("HSI 中出现过的 G 列单元格行号：", g_cells)

non_empty_g = []
for m in re.finditer(r'<c r="G(\d+)"[^>]*>(.*?)</c>', xml, re.S):
    body = m.group(2)
    if "<v>" in body:
        non_empty_g.append((m.group(1), body))
print("其中带取值的：", non_empty_g or "无")
