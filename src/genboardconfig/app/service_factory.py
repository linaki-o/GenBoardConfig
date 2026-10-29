"""服务工厂：按配置装配各层依赖。"""

from __future__ import annotations

import re
from pathlib import Path

from ..infra.llm.orchestrator import LLMOrchestrator
from ..infra.llm.masker import Masker
from ..infra.llm.prompt_repo import PromptRepo
from ..infra.llm.provider.base import LLMProvider
from ..infra.llm.provider.mock import MockProvider
from ..infra.llm.provider.openai_compatible import OpenAICompatibleProvider
from ..infra.secrets.store import SecretStore
from ..infra.settings import Settings
from .apply_usecase import ApplyUseCase
from .check_usecase import CheckUseCase, build_matcher, build_planner, build_rules

SECRET_KEY_NAME = "llm_api_key"


def secret_store(settings: Settings) -> SecretStore:
    return SecretStore(Path(settings.config_dir) / "secrets.bin")


def resolve_api_key(settings: Settings) -> str:
    store = secret_store(settings)
    key = store.get(SECRET_KEY_NAME)
    if key:
        return key
    return settings.get("llm.api_key", "") or ""


def load_profiles(settings: Settings) -> list:
    from ..domain.profiles import Profile

    directory = Path(settings.config_dir) / "profiles"
    profiles = Profile.load_dir(directory)
    if not settings.get("check.use_profiles", True):
        return []
    return profiles


def detect_profile(excel_path: str | Path, profiles: list) -> object | None:
    """按 Sheet 名（其次表头关键字）自动选择档案。"""
    if not profiles:
        return None
    try:
        from openpyxl import load_workbook

        wb = load_workbook(Path(excel_path), read_only=True, data_only=True)
        try:
            sheet_names = list(wb.sheetnames)
        finally:
            wb.close()
    except Exception:  # noqa: BLE001
        return None
    for profile in profiles:
        if not profile.excel_sheet:
            continue
        if profile.match_sheet(profile.excel_sheet) and profile.excel_sheet in sheet_names:
            return profile
    for name in sheet_names:
        for profile in profiles:
            if profile.excel_sheet and profile.excel_sheet.lower() == name.lower():
                return profile
    return None


def build_provider(settings: Settings) -> LLMProvider:
    provider = (settings.get("llm.provider", "mock") or "mock").lower()
    if provider == "mock":
        return MockProvider()
    if provider in {"openai_compatible", "openai", "deepseek", "qwen", "custom"}:
        return OpenAICompatibleProvider(
            base_url=settings.get("llm.base_url", ""),
            api_key=resolve_api_key(settings),
            model=settings.get("llm.model", ""),
            timeout=float(settings.get("llm.timeout_seconds", 60)),
            max_retries=int(settings.get("llm.max_retries", 3)),
            use_structured_output=bool(settings.get("llm.use_structured_output", True)),
        )
    if provider == "anthropic":
        # 预留：切换为 AnthropicProvider（需额外依赖）
        return MockProvider()
    return MockProvider()


def build_orchestrator(settings: Settings) -> LLMOrchestrator:
    repo = PromptRepo(settings.config_dir)
    masker = Masker(enabled=bool(settings.get("privacy.mask_sensitive", True)))
    return LLMOrchestrator(
        provider=build_provider(settings),
        prompt_repo=repo,
        masker=masker,
        temperature=float(settings.get("llm.temperature", 0.0)),
        batch_size=int(settings.get("llm.max_batch_size", 20)),
    )


# 系列 → 档案 id（保留旧档案名作为别名）
SERIES_PROFILES = {"ntk": ("ntk", "hsi"), "rtk": ("rtk",)}


def profile_for_series(settings: Settings, series: str) -> object | None:
    """按项目系列取档案（ntk / rtk）。"""
    if not series or series == "auto":
        return None
    from ..domain.profiles import Profile

    profiles = {p.id: p for p in load_profiles(settings)}
    for candidate in SERIES_PROFILES.get(series, (series,)):
        if candidate in profiles:
            return profiles[candidate]
    return None


def detect_series(c_path: str | Path) -> str:
    """按板级配置文件的特征判断项目系列。

    - 含 ``PORT_<X>_DEFAULT_*`` 端口位表 → NTK
    - 含 ``#define _PIN_<PAD> (_PIN_<PAD>_<FUNC>)`` 引脚复用 → RTK
    """
    try:
        head = Path(c_path).read_text(encoding="utf-8", errors="replace")[:400000]
    except Exception:  # noqa: BLE001
        return "ntk"
    if re.search(r"^#define\s+_PIN_[A-Z]+\d+\s+\(\s*_PIN_[A-Z]+\d+_[A-Za-z0-9_]+\s*\)",
                 head, re.M):
        return "rtk"
    if re.search(r"#define\s+PORT_[A-Z]_DEFAULT_", head):
        return "ntk"
    return "ntk"


def build_check_usecase(
    settings: Settings, profile: object | None = None
) -> CheckUseCase:
    from ..infra.cconfig.parser import CConfigParser
    from ..infra.cconfig.rtk_pinshare import RtkPinshareParser
    from ..infra.excel.reader import ExcelParser

    aliases = settings.aliases
    threshold = float(settings.get("check.confidence_threshold", 0.8))
    if profile is not None:
        override = settings.get(f"profiles.{profile.id}.row_filter")
        if override:
            profile.apply_override(override)
    if profile is not None and profile.c_cfg("kind") == "pinshare":
        c_parser = RtkPinshareParser()
    else:
        group_cfg = profile.c_cfg("group") if profile is not None else None
        table_cfg = profile.c_cfg("port_table") if profile is not None else None
        c_parser = CConfigParser(group_cfg=group_cfg, port_table_cfg=table_cfg)
    return CheckUseCase(
        excel_parser=ExcelParser(settings.column_mapping, profile=profile),
        c_parser=c_parser,
        matcher=build_matcher(aliases),
        rules=build_rules(aliases, threshold),
        planner=build_planner(),
        orchestrator=build_orchestrator(settings),
        profile=profile,
        settings=settings,
    )


def build_apply_usecase() -> ApplyUseCase:
    return ApplyUseCase()
