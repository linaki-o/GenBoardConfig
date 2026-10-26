"""核对报告输出：HTML / CSV。"""

from __future__ import annotations

import csv
import html
import io
from datetime import datetime

from ...domain.models import STATUS_LABELS, CheckResult, CheckStatus

STATUS_COLORS = {
    CheckStatus.MATCH.value: ("#16a34a", "#dcfce7"),
    CheckStatus.MISMATCH.value: ("#dc2626", "#fee2e2"),
    CheckStatus.MISSING.value: ("#ea580c", "#ffedd5"),
    CheckStatus.AMBIGUOUS.value: ("#ca8a04", "#fef9c3"),
    CheckStatus.NOT_APPLICABLE.value: ("#64748b", "#f1f5f9"),
    CheckStatus.UNRESOLVED.value: ("#7c3aed", "#ede9fe"),
}

CSS = """
:root{--bd:#e2e8f0;--muted:#64748b;--bg:#f8fafc}
*{box-sizing:border-box}
body{font-family:"Microsoft YaHei","Segoe UI",sans-serif;margin:0;padding:24px;background:var(--bg);color:#0f172a}
h1{font-size:20px;margin:0 0 4px}
.meta{color:var(--muted);font-size:12px;margin-bottom:16px}
.cards{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px}
.card{background:#fff;border:1px solid var(--bd);border-radius:10px;padding:10px 16px;min-width:110px}
.card .n{font-size:22px;font-weight:700}
.card .t{font-size:12px;color:var(--muted)}
table{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--bd);border-radius:10px;overflow:hidden}
th,td{padding:7px 10px;border-bottom:1px solid var(--bd);font-size:12px;text-align:left;vertical-align:top}
th{background:#f1f5f9;font-weight:600;position:sticky;top:0}
tr:hover td{background:#f8fafc}
.badge{display:inline-block;padding:1px 8px;border-radius:999px;font-size:11px;white-space:nowrap}
code{font-family:Consolas,monospace;background:#f1f5f9;padding:1px 4px;border-radius:4px;font-size:11px}
.snippet{font-family:Consolas,monospace;font-size:11px;color:#334155;white-space:pre-wrap}
"""

CARD_ORDER = [
    (CheckStatus.MATCH.value, "一致"),
    (CheckStatus.MISMATCH.value, "不一致"),
    (CheckStatus.MISSING.value, "缺失"),
    (CheckStatus.AMBIGUOUS.value, "歧义"),
    (CheckStatus.NOT_APPLICABLE.value, "不适用"),
    (CheckStatus.UNRESOLVED.value, "未解析"),
]


def _badge(status: str) -> str:
    fg, bg = STATUS_COLORS.get(status, ("#0f172a", "#e2e8f0"))
    label = STATUS_LABELS.get(status, status)
    return f'<span class="badge" style="color:{fg};background:{bg}">{html.escape(label)}</span>'


def render_html(result: CheckResult, diff: str = "") -> str:
    reqs = {r.id: r for r in result.requirements}
    profile_mode = bool(result.requirements and result.requirements[0].attributes)
    rows = []
    for res in result.results:
        req = reqs.get(res.requirement_id)
        if profile_mode:
            rows.append(_profile_row(res, req))
        else:
            rows.append(_generic_row(res, req))

    cards = []
    for key, title in CARD_ORDER:
        n = result.summary.counts.get(key, 0)
        fg, bg = STATUS_COLORS.get(key, ("#0f172a", "#e2e8f0"))
        cards.append(
            f'<div class="card"><div class="n" style="color:{fg}">{n}</div>'
            f'<div class="t">{title}</div></div>'
        )
    cards.append(
        f'<div class="card"><div class="n">{result.summary.total}</div><div class="t">总条目</div></div>'
    )
    cards.append(
        f'<div class="card"><div class="n">{result.summary.c_entries}</div><div class="t">C 解析条目</div></div>'
    )

    diff_block = ""
    if diff:
        diff_block = (
            "<h2 style='font-size:16px;margin-top:22px'>修改 Diff</h2>"
            f"<pre class='snippet' style='background:#fff;border:1px solid var(--bd);"
            f"border-radius:10px;padding:12px;overflow:auto'>{html.escape(diff)}</pre>"
        )

    warn_block = ""
    if result.warnings:
        items = "".join(f"<li>{html.escape(w)}</li>" for w in result.warnings)
        warn_block = f"<h2 style='font-size:16px'>警告</h2><ul>{items}</ul>"

    if profile_mode:
        header = (
            "<tr><th>网络名</th><th>引脚</th><th>宏组</th><th>状态</th>"
            "<th>逐属性核对</th><th>置信度</th><th>说明</th></tr>"
        )
    else:
        header = (
            "<tr><th>Sheet</th><th>行</th><th>状态</th><th>管脚</th><th>GPIO</th><th>功能</th>"
            "<th>配置项</th><th>期望值</th><th>当前值</th><th>置信度</th><th>依据</th><th>说明</th></tr>"
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>GPIO 配置核对报告</title><style>{CSS}</style></head><body>
<h1>GPIO 配置核对报告</h1>
<div class="meta">
 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
 Excel：{html.escape(result.excel_path)}<br>
 C 配置：{html.escape(result.c_path)}<br>
 核对档案：{html.escape(str(result.extra.get('profile', 'generic')))}<br>
 大模型调用：{result.llm_calls} 次 / {result.llm_tokens} tokens
</div>
<div class="cards">{''.join(cards)}</div>
{warn_block}
<table>
<thead>{header}</thead>
<tbody>{''.join(rows)}</tbody></table>
{diff_block}
</body></html>"""


def _generic_row(res, req) -> str:
    evidence = "<br>".join(
        f'<div class="snippet">L{e.line} {html.escape(e.snippet)}</div>'
        for e in res.evidence[:2]
    )
    return (
        "<tr>"
        f"<td>{html.escape(req.sheet if req else '')}</td>"
        f"<td>{html.escape(str(req.row_no) if req else '')}</td>"
        f"<td>{_badge(res.status.value)}</td>"
        f"<td>{html.escape(req.pin_name_raw if req else '')}</td>"
        f"<td>{html.escape(str(req.gpio_num) if req and req.gpio_num is not None else '')}</td>"
        f"<td>{html.escape(req.function_name if req else '')}</td>"
        f"<td><code>{html.escape(req.config_key if req else '')}</code></td>"
        f"<td>{html.escape(res.expected_value)}</td>"
        f"<td>{html.escape(res.current_value)}</td>"
        f"<td>{res.confidence:.2f}</td>"
        f"<td>{evidence}</td>"
        f"<td>{html.escape(res.notes)}</td>"
        "</tr>"
    )


def _profile_row(res, req) -> str:
    cells = []
    for attr in res.attribute_results:
        color = {
            "mismatch": "#dc2626",
            "ambiguous": "#ca8a04",
            "missing": "#ea580c",
            "match": "#16a34a",
            "not_applicable": "#94a3b8",
        }.get(attr.status.value, "#0f172a")
        value = html.escape(attr.expected or "-")
        if attr.actual:
            value += " → " + html.escape(attr.actual)
        cells.append(
            f"<div><span style='color:{color}'>{html.escape(attr.label)}</span>: {value}</div>"
        )
    return (
        "<tr>"
        f"<td>{html.escape(req.net_name if req else '')}</td>"
        f"<td>{html.escape(req.pin_name_raw if req else '')}</td>"
        f"<td><code>{html.escape(res.symbol or '-')}</code></td>"
        f"<td>{_badge(res.status.value)}</td>"
        f"<td>{''.join(cells)}</td>"
        f"<td>{res.confidence:.2f}</td>"
        f"<td>{html.escape(res.notes)}</td>"
        "</tr>"
    )


def render_csv(result: CheckResult) -> str:
    reqs = {r.id: r for r in result.requirements}
    profile_mode = bool(result.requirements and result.requirements[0].attributes)
    buf = io.StringIO()
    writer = csv.writer(buf)
    if profile_mode:
        writer.writerow(
            ["网络名", "引脚", "宏组", "状态", "置信度", "逐属性核对", "说明"]
        )
        for res in result.results:
            req = reqs.get(res.requirement_id)
            attrs = "; ".join(
                f"{a.label}: 期望 {a.expected or '-'} / 实际 {a.actual or '-'} ({a.status.value})"
                for a in res.attribute_results
            )
            writer.writerow(
                [
                    req.net_name if req else "",
                    req.pin_name_raw if req else "",
                    res.symbol,
                    STATUS_LABELS.get(res.status.value, res.status.value),
                    f"{res.confidence:.2f}",
                    attrs,
                    res.notes,
                ]
            )
        return buf.getvalue()

    writer.writerow(
        [
            "Sheet", "行号", "状态", "管脚", "GPIO号", "功能", "配置项",
            "期望值", "当前值", "置信度", "来源", "依据", "说明",
        ]
    )
    for res in result.results:
        req = reqs.get(res.requirement_id)
        evidence = " | ".join(f"L{e.line} {e.snippet}" for e in res.evidence)
        writer.writerow(
            [
                req.sheet if req else "",
                req.row_no if req else "",
                STATUS_LABELS.get(res.status.value, res.status.value),
                req.pin_name_raw if req else "",
                req.gpio_num if req and req.gpio_num is not None else "",
                req.function_name if req else "",
                req.config_key if req else "",
                res.expected_value,
                res.current_value,
                f"{res.confidence:.2f}",
                res.source.value,
                evidence,
                res.notes,
            ]
        )
    return buf.getvalue()
