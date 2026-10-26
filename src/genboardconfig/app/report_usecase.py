"""报告用例：导出 HTML / CSV / Diff。"""

from __future__ import annotations

from pathlib import Path

from ..infra.report.html_report import render_csv, render_html
from .context import Session


class ReportUseCase:
    def export_html(
        self, session: Session, diff: str = "", target: str | Path | None = None
    ) -> Path:
        out = Path(target) if target else session.workdir / "report.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_html(session.check_result, diff), encoding="utf-8")
        return out

    def export_csv(
        self, session: Session, target: str | Path | None = None
    ) -> Path:
        out = Path(target) if target else session.workdir / "report.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_csv(session.check_result), encoding="utf-8-sig")
        return out

    def export_patch(
        self, session: Session, diff: str, target: str | Path | None = None
    ) -> Path:
        out = Path(target) if target else session.workdir / "changes.patch"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(diff, encoding="utf-8")
        return out
