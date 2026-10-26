"""后台任务：核对与应用放到工作线程，避免界面冻结。"""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import QThread, Signal


class Worker(QThread):
    progress = Signal(str, float)
    completed = Signal(object)
    failed = Signal(str)
    log = Signal(str)

    def __init__(self, fn: Callable[[Callable[[str, float], None]], object], parent=None):
        super().__init__(parent)
        self._fn = fn
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    def run(self) -> None:  # noqa: D102
        def progress(message: str, percent: float) -> None:
            if self._cancelled:
                raise InterruptedError("任务已取消")
            self.progress.emit(message, percent)
            self.log.emit(f"[{percent * 100:5.1f}%] {message}")

        try:
            result = self._fn(progress)
        except InterruptedError:
            self.log.emit("任务已取消")
            self.completed.emit(None)
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(f"{type(exc).__name__}: {exc}")
        else:
            self.completed.emit(result)
