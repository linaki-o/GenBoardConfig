"""解析与写回单测。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from genboardconfig.infra.cconfig.editor import TextEdit, apply_edits
from genboardconfig.infra.cconfig.parser import CConfigParser
from genboardconfig.infra.excel.reader import ExcelParser
from genboardconfig.infra.validate.structure import check_structure

SAMPLE_C = """#include "board.h"

#define CONFIG_LED1_GPIO   48
#define CONFIG_LED2_GPIO   49

struct board_gpio led_map[] = {
    { "LED1", GPIO_PC13 },
    { "LED2", GPIO_PC14 },
};

struct board_gpio reset_cfg = {
    .name   = "RESET",
    .gpio   = 5,
};

void board_gpio_init(void)
{
    gpio_config(GPIO_PC13, LED1, GPIO_ACTIVE_LOW);
}
"""


def _parser() -> CConfigParser:
    return CConfigParser()


def test_parse_macros_struct_fields_and_array_items():
    result = _parser().parse_text(SAMPLE_C)
    keys = {e.key for e in result.entries}
    assert "CONFIG_LED1_GPIO" in keys
    assert "gpio" in keys
    assert "LED1" in keys
    assert "board_gpio_init" in keys
    values = {e.key: e.value_raw for e in result.entries}
    assert values["CONFIG_LED1_GPIO"] == "48"
    assert values["LED1"] == "GPIO_PC13"


def test_entry_locations_are_exact():
    result = _parser().parse_text(SAMPLE_C)
    macro = next(e for e in result.entries if e.key == "CONFIG_LED1_GPIO")
    assert macro.line == 3
    line = SAMPLE_C.split("\n")[macro.line - 1]
    assert line[macro.value_col : macro.value_col + macro.value_len] == "48"


def test_apply_edits_preserves_other_content():
    result = _parser().parse_text(SAMPLE_C)
    macro = next(e for e in result.entries if e.key == "CONFIG_LED1_GPIO")
    new_text = apply_edits(
        SAMPLE_C, [TextEdit(line=macro.line, col=macro.value_col, length=macro.value_len, new_value="60")]
    )
    assert "#define CONFIG_LED1_GPIO   60" in new_text
    assert new_text.count("\n") == SAMPLE_C.count("\n")


def test_structure_check_detects_unbalanced_braces():
    assert check_structure(SAMPLE_C).ok
    assert not check_structure("void f() {\n").ok
    assert not check_structure('#define X "abc\n').ok


def test_excel_parser_finds_header_below_title(tmp_path: Path):
    from openpyxl import Workbook

    path = tmp_path / "t.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.append(["某某主板 GPIO 分配表"])
    ws.append(["管脚名", "GPIO号", "功能", "配置项", "期望值"])
    ws.append(["GPIO_PC13", 13, "LED1", "CONFIG_LED1_GPIO", 48])
    wb.save(path)

    parser = ExcelParser(
        {
            "fields": {
                "pin_name": ["管脚", "管脚名"],
                "gpio_num": ["gpio号"],
                "function": ["功能"],
                "config_key": ["配置项"],
                "expected_value": ["期望值"],
            },
            "header_hint_keywords": ["管脚", "gpio", "功能", "配置", "期望"],
        }
    )
    result = parser.parse(path)
    assert len(result.requirements) == 1
    req = result.requirements[0]
    assert req.pin_name_raw == "GPIO_PC13"
    assert req.gpio_num == 13
    assert req.expected_value == "48"
    assert req.row_no == 3
