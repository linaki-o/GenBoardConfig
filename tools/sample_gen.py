"""生成脱敏样例数据：GPIO 分配 Excel + 板级 C 配置。

用法：python tools/sample_gen.py [输出目录]
"""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

HEADER = ["管脚名", "GPIO号", "功能", "配置项", "期望值", "芯片实例", "极性", "备注"]
ROWS = [
    ("GPIO_PC13", 13, "LED1", "CONFIG_LED1_GPIO", 48, "GPIOA", "低有效", "电源指示灯"),
    ("GPIO_PC14", 14, "LED2", "CONFIG_LED2_GPIO", 49, "GPIOA", "高有效", "状态指示灯"),
    ("GPIO_PC15", 15, "LED3", "CONFIG_LED3_GPIO", 60, "GPIOA", "高有效", "心跳灯，期望与配置不一致"),
    ("GPIO_PA12", 12, "KEY1", "CONFIG_KEY1_GPIO", 12, "GPIOB", "低有效", "复位键"),
    ("GPIO_PA13", 13, "KEY2", "CONFIG_KEY2_GPIO", 14, "GPIOB", "低有效", "配置与期望不一致"),
    ("GPIO_PB5", 5, "BEEP", "CONFIG_BEEP_GPIO", 5, "GPIOB", "高有效", "蜂鸣器，配置项缺失"),
    ("GPIO_PB6", 6, "PWR_EN", "CONFIG_PWR_EN_GPIO", 6, "GPIOB", "高有效", "电源使能"),
    ("GPIO_PD7", 7, "RESET", "CONFIG_RESET_GPIO", 5, "GPIOC", "低有效", "外部复位"),
    ("GPIO_PD8", 8, "FAN", "CONFIG_FAN_GPIO", 21, "GPIOC", "高有效", "风扇使能，配置缺失"),
    ("GPIO_PD9", 9, "LED4", "CONFIG_LED4_GPIO", 22, "GPIOC", "高有效", "调试灯，配置缺失"),
    ("GPIO_PE1", 1, "SD_DET", "CONFIG_SD_DET_GPIO", 1, "GPIOD", "低有效", "SD 卡检测"),
    ("GPIO_PE2", 2, "USB_EN", "CONFIG_USB_EN_GPIO", 2, "GPIOD", "高有效", "USB 使能"),
]

C_SOURCE = """/*
 * 板级 GPIO 配置（样例，脱敏）
 * 文件：board_config.c
 */

#include "board.h"
#include "board_gpio.h"

#define CONFIG_LED1_GPIO            48
#define CONFIG_LED2_GPIO            49
#define CONFIG_LED3_GPIO            61
#define CONFIG_KEY1_GPIO            12
#define CONFIG_KEY2_GPIO            13
#define CONFIG_PWR_EN_GPIO          6
#define CONFIG_LED1_ACTIVE_LOW      1
#define CONFIG_LED1_MUX             GPIO_MUX_A

/* GPIO 复用表：功能名 -> 引脚 */
struct board_gpio led_map[] = {
    { "LED1", GPIO_PC13 },
    { "LED2", GPIO_PC14 },
    { "KEY1", GPIO_PA12 },
    { "KEY2", GPIO_PA13 },
    { "BEEP", GPIO_PB5  },
};

/* 单实例配置 */
struct board_gpio reset_cfg = {
    .name    = "RESET",
    .gpio    = 5,
    .active  = GPIO_ACTIVE_LOW,
    .pull    = GPIO_PULL_UP,
};

void board_gpio_init(void)
{
    gpio_config(GPIO_PC13, LED1, GPIO_ACTIVE_LOW);
    gpio_config(GPIO_PC14, LED2, GPIO_ACTIVE_HIGH);
    gpio_config(GPIO_PA12, KEY1, GPIO_ACTIVE_LOW);
    gpio_config(GPIO_PB5,  BEEP, GPIO_ACTIVE_HIGH);
}
"""


def build_excel(path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "GPIO 分配"
    ws["A1"] = "XX 主板 GPIO 分配表（脱敏样例）"
    ws["A1"].font = Font(bold=True, size=13)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADER))
    ws["A1"].alignment = Alignment(horizontal="center")

    ws.append(HEADER)
    for cell in ws[2]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="334155")
        cell.alignment = Alignment(horizontal="center")
    for row in ROWS:
        ws.append(list(row))
    for idx, width in enumerate([14, 10, 12, 24, 12, 12, 12, 30], start=1):
        ws.column_dimensions[chr(64 + idx)].width = width
    ws.freeze_panes = "A3"
    wb.save(path)


def build_c(path: Path) -> None:
    path.write_text(C_SOURCE, encoding="utf-8")


def main() -> int:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "samples"
    out_dir.mkdir(parents=True, exist_ok=True)
    excel = out_dir / "gpio_table_sample.xlsx"
    cfile = out_dir / "board_config_sample.c"
    build_excel(excel)
    build_c(cfile)
    print(f"已生成：\n  {excel}\n  {cfile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
