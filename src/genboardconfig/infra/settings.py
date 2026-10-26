"""配置加载：settings.yaml + settings.local.yaml + 别名/列映射。"""

from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


def _find_config_dir() -> Path:
    env = os.environ.get("GENBOARDCONFIG_CONFIG")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "config" / "settings.yaml"
        if candidate.exists():
            return candidate.parent
    return Path.cwd() / "config"


@dataclass
class Settings:
    data: dict[str, Any] = field(default_factory=dict)
    config_dir: Path = field(default_factory=_find_config_dir)

    def get(self, path: str, default: Any = None) -> Any:
        node: Any = self.data
        for part in path.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def set(self, path: str, value: Any) -> None:
        parts = path.split(".")
        node = self.data
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value

    def save_local(self) -> Path:
        local = self.config_dir / "settings.local.yaml"
        with local.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(self.data, fh, allow_unicode=True, sort_keys=False)
        return local

    def load_yaml(self, filename: str) -> dict[str, Any]:
        path = self.config_dir / filename
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}

    @property
    def column_mapping(self) -> dict[str, Any]:
        return self.load_yaml("column_mapping.yaml")

    @property
    def aliases(self) -> dict[str, Any]:
        return self.load_yaml("aliases.yaml")

    def prompt_text(self, name: str) -> str:
        path = self.config_dir / "prompts" / name
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")


def load_settings() -> Settings:
    config_dir = _find_config_dir()
    data: dict[str, Any] = {}
    base = config_dir / "settings.yaml"
    if base.exists():
        data = yaml.safe_load(base.read_text(encoding="utf-8")) or {}
    local = config_dir / "settings.local.yaml"
    if local.exists():
        data = _deep_merge(data, yaml.safe_load(local.read_text(encoding="utf-8")) or {})
    return Settings(data=data, config_dir=config_dir)


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)
