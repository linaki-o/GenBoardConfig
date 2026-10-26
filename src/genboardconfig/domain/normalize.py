"""归一化：把 Excel 文本与 .c 文本统一到可比较的规范形式。"""

from __future__ import annotations

import re
from typing import Any

_NON_ALNUM = re.compile(r"[^\w]+", re.UNICODE)
_LEAD_GPIO = re.compile(r"^GPIO(?![A-Z0-9])", re.IGNORECASE)
_PIN_PORT = re.compile(r"^([A-Z]{1,2})[_\-]?(\d+)$")
_PIN_GPIO = re.compile(r"^GPIO([A-Z])[_\-]?(\d+)$")
_HEX = re.compile(r"^0[xX]([0-9A-Fa-f]+)$")
_INT = re.compile(r"^[+-]?\d+$")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_key(value: Any) -> str:
    """配置项/宏名归一化：大小写、下划线、连字符、厂商前缀差异。"""
    text = clean_text(value).upper()
    text = _NON_ALNUM.sub("_", text).strip("_")
    text = re.sub(r"_{2,}", "_", text)
    return text

def strip_config_prefix(key_norm: str) -> str:
    for prefix in ("CONFIG_", "BOARD_", "SOC_"):
        if key_norm.startswith(prefix):
            return key_norm[len(prefix):]
    return key_norm


def norm_pin(value: Any) -> tuple[str, str]:
    """返回 (pin_key, controller)。

    GPIO_PC13 / PC13 / pc 13 / PC_13 → ('PC13', '')
    GPIOA_5                        → ('A5', '')
    GPIOC13                        → ('C13', '')
    纯数字                         → ('13', '')
    """
    text = clean_text(value).upper().replace(" ", "")
    if not text:
        return "", ""
    text = text.replace("-", "_")
    m = _PIN_GPIO.match(text)
    if m:
        return f"{m.group(1)}{m.group(2)}", ""
    body = _LEAD_GPIO.sub("", text).lstrip("_")
    m = _PIN_PORT.match(body)
    if m:
        return f"{m.group(1)}{m.group(2)}", ""
    if body.isdigit():
        return body, ""
    return body, ""


def norm_gpio_num(value: Any) -> int | None:
    text = clean_text(value).upper()
    if not text:
        return None
    m = _HEX.match(text)
    if m:
        return int(m.group(1), 16)
    if _INT.match(text):
        return int(text)
    m = re.search(r"(?:^|[^0-9A-Z])(0[xX][0-9A-Fa-f]+|\d+)(?:[^0-9A-Z]|$)", text)
    if m:
        tok = m.group(1)
        if tok.lower().startswith("0x"):
            return int(tok, 16)
        return int(tok)
    return None


def norm_value(value: Any, value_aliases: dict[str, list[str]] | None = None) -> str:
    """把配置值归一化为可比较的字符串；数值统一为十进制。"""
    text = clean_text(value)
    if not text:
        return ""
    if value_aliases:
        for canonical, variants in value_aliases.items():
            if text.lower() == canonical.lower() or any(
                text.lower() == v.lower() for v in variants
            ):
                return canonical
    num = norm_gpio_num(text)
    if num is not None and re.fullmatch(r"[0-9A-Fa-fxX]+", text):
        return str(num)
    return text.strip().upper()


def values_equivalent(
    expected: str,
    current: str,
    aliases: dict[str, list[str]] | None = None,
) -> bool:
    """判断期望值与当前值是否语义等价。"""
    if not expected:
        return False
    if not current:
        return False
    e = norm_value(expected, aliases)
    c = norm_value(current, aliases)
    if e == c:
        return True
    exp_num = norm_gpio_num(e)
    cur_num = norm_gpio_num(c)
    if exp_num is not None and cur_num is not None and exp_num == cur_num:
        return True
    exp_pin, _ = norm_pin(e)
    cur_pin, _ = norm_pin(c)
    if exp_pin and cur_pin and exp_pin == cur_pin:
        return True
    if aliases:
        for canonical, variants in aliases.items():
            group = {canonical.lower()} | {v.lower() for v in variants}
            if (e.lower() in group) and (c.lower() in group):
                return True
    return False
