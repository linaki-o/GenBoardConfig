"""校验：结构 + 语义复检。"""

from .semantic import SemanticReport, recheck
from .structure import ValidationReport, check_structure

__all__ = ["SemanticReport", "ValidationReport", "check_structure", "recheck"]
