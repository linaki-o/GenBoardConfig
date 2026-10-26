"""提示词仓库：从 config/prompts 加载模板，支持版本与热更新。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROMPT_VERSION = "v1"


@dataclass
class PromptTemplate:
    name: str
    text: str
    path: Path | None = None


class PromptRepo:
    def __init__(self, config_dir: str | Path):
        self.config_dir = Path(config_dir)
        self._cache: dict[str, PromptTemplate] = {}

    def get(self, name: str) -> PromptTemplate:
        if name in self._cache:
            return self._cache[name]
        path = self.config_dir / "prompts" / f"{name}.md"
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        template = PromptTemplate(name=name, text=text, path=path if path.exists() else None)
        self._cache[name] = template
        return template

    def reload(self) -> None:
        self._cache.clear()
