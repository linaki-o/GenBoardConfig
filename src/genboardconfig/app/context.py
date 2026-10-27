"""应用层：用例编排与上下文。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from ..domain.models import CheckResult, ConfigEntry, GPIORequirement
from ..infra.cconfig.parser import CParseResult

ProgressFn = Callable[[str, float], None]


@dataclass
class Session:
    """一次核对会话的全部中间产物。"""

    excel_path: str = ""
    c_path: str = ""
    c_parse: CParseResult | None = None
    check_result: CheckResult = field(default_factory=CheckResult)
    candidates: dict[str, list[Any]] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    log_lines: list[str] = field(default_factory=list)
    profile: Any = None
    parser: Any = None          # 本次核对使用的 C 侧解析器（复检时复用）

    @property
    def workdir(self) -> Path:
        base = Path(self.c_path).parent if self.c_path else Path.cwd()
        return base / ".genboard"

    def entries_by_id(self) -> dict[str, ConfigEntry]:
        return {e.id: e for e in self.check_result.entries}

    def requirements_by_id(self) -> dict[str, GPIORequirement]:
        return {r.id: r for r in self.check_result.requirements}
