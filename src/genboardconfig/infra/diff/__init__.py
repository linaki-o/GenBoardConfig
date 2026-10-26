"""差异与写回。"""

from .patcher import DiffResult, backup_file, restore_file, unified_diff

__all__ = ["DiffResult", "backup_file", "restore_file", "unified_diff"]
