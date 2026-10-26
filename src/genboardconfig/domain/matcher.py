"""匹配引擎：为每条 Excel 需求在 .c 条目中寻找候选关联。"""

from __future__ import annotations

from dataclasses import dataclass

from .models import ConfigEntry, GPIORequirement
from .normalize import norm_gpio_num, norm_key, norm_pin, strip_config_prefix

CANDIDATE_THRESHOLD = 0.35

# 这些词在几乎所有配置项名里都出现，不能作为匹配依据
GENERIC_TOKENS = {
    "GPIO", "PIN", "PINS", "NUM", "NUMBER", "IO", "PORT", "CFG", "CONFIG",
    "BOARD", "SOC", "VAL", "VALUE", "EN", "ENABLE", "ACTIVE", "MUX", "PULL",
    "LEVEL", "MODE", "CTRL", "CONTROL", "SET", "DEFAULT",
}


def significant_tokens(key_norm: str) -> set[str]:
    """提取配置项名中具有区分度的词。"""
    return {
        token
        for token in key_norm.split("_")
        if token and token not in GENERIC_TOKENS and len(token) > 1
    }



def stripped_overlap(req_key: str, ent_key: str) -> bool:
    """去前缀后是否完全一致（要求有足够区分度）。"""
    a = strip_config_prefix(req_key)
    b = strip_config_prefix(ent_key)
    if not a or not b:
        return False
    if a == b:
        return True
    return bool(significant_tokens(a) & significant_tokens(b))


@dataclass
class Candidate:
    entry: ConfigEntry
    score: float
    reason: str


class Matcher:
    """确定性候选匹配：配置项名 > 功能名 > 管脚名 > GPIO 号。"""

    def __init__(self, config_key_aliases: dict[str, list[str]] | None = None):
        self.config_key_aliases = {
            norm_key(k): [norm_key(v) for v in vs]
            for k, vs in (config_key_aliases or {}).items()
        }

    def _key_variants(self, key_norm: str) -> set[str]:
        variants = {key_norm, strip_config_prefix(key_norm)}
        for base, alts in self.config_key_aliases.items():
            group = {base, strip_config_prefix(base)} | set(alts)
            if key_norm in group:
                variants |= group
        return {v for v in variants if v}

    def score(self, req: GPIORequirement, entry: ConfigEntry) -> tuple[float, str]:
        best = 0.0
        reasons: list[str] = []

        req_key = req.config_key_norm
        if req_key:
            variants = self._key_variants(req_key)
            ent_key = entry.key_norm
            req_sig = significant_tokens(req_key)
            ent_sig = significant_tokens(ent_key)
            if ent_key and ent_key in variants:
                best = max(best, 1.0)
                reasons.append("配置项名精确匹配")
            elif ent_key and req_sig and ent_sig and (req_sig & ent_sig):
                best = max(best, 0.88)
                reasons.append("配置项名关键词匹配")
            elif ent_key and stripped_overlap(req_key, ent_key):
                best = max(best, 0.8)
                reasons.append("配置项名（去前缀）匹配")

        func = norm_key(req.function_name)
        if func:
            haystack = norm_key(f"{entry.key} {entry.owner} {entry.context}")
            if func in haystack:
                best = max(best, 0.66)
                reasons.append("功能名匹配")

        if req.pin_key:
            ent_pin, _ = norm_pin(entry.value_raw)
            hay = norm_key(f"{entry.value_raw} {entry.context}")
            if ent_pin and ent_pin == req.pin_key:
                best = max(best, 0.72)
                reasons.append("引脚名匹配")
            elif req.pin_key in hay:
                best = max(best, 0.6)
                reasons.append("引脚名出现在条目中")

        if req.gpio_num is not None:
            ent_num = norm_gpio_num(entry.value_raw)
            if ent_num is not None and ent_num == req.gpio_num:
                best = max(best, 0.45)
                reasons.append("GPIO 编号匹配（弱）")
            elif ent_num is not None and req.gpio_num != ent_num:
                best = max(best, 0.25)

        if req.chip_instance:
            hay = norm_key(f"{entry.key} {entry.owner} {entry.context}")
            if norm_key(req.chip_instance) in hay:
                best = max(best, 0.4)
                reasons.append("芯片实例匹配")

        return best, "；".join(reasons) if reasons else "无明显特征"

    def candidates(
        self, req: GPIORequirement, entries: list[ConfigEntry]
    ) -> list[Candidate]:
        scored: list[Candidate] = []
        for entry in entries:
            score, reason = self.score(req, entry)
            if score >= CANDIDATE_THRESHOLD:
                scored.append(Candidate(entry=entry, score=score, reason=reason))
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored
