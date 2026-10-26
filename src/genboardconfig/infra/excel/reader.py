"""Excel 解析：定位表头、映射列语义、输出归一化后的需求项。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

from ...domain.models import ExpectedAttribute, GPIORequirement
from ...domain.normalize import (
    clean_text,
    norm_gpio_num,
    norm_key,
    norm_pin,
    norm_value,
)


@dataclass
class SheetInfo:
    name: str
    header_row: int
    columns: dict[int, str] = field(default_factory=dict)   # 列索引 → 字段名
    row_count: int = 0


@dataclass
class ExcelParseResult:
    requirements: list[GPIORequirement] = field(default_factory=list)
    sheets: list[SheetInfo] = field(default_factory=list)
    column_mapping: dict[str, str] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    unmapped_columns: list[str] = field(default_factory=list)
    filter_stats: dict[str, Any] = field(default_factory=dict)


class ColumnMapper:
    """表头文本 → 领域字段。"""

    def __init__(self, mapping_cfg: dict[str, Any]):
        self.rules: dict[str, list[str]] = {}
        for field_name, aliases in (mapping_cfg.get("fields") or {}).items():
            self.rules[field_name] = [norm_key(a) for a in aliases]
        self.hint_keywords = [
            norm_key(k) for k in (mapping_cfg.get("header_hint_keywords") or [])
        ]

    def field_for_header(self, header: str) -> str:
        return self.match_header(header)[0]

    def match_header(self, header: str) -> tuple[str, float]:
        """返回 (字段名, 匹配度)。"""
        key = norm_key(header)
        if not key:
            return "", 0.0
        best, best_score = "", 0.0
        for field_name, aliases in self.rules.items():
            for alias in aliases:
                if not alias:
                    continue
                if key == alias:
                    score = 1.0
                elif alias in key or key in alias:
                    score = 0.75
                else:
                    score = 0.0
                if score > best_score:
                    best, best_score = field_name, score
        return (best, best_score) if best_score >= 0.7 else ("", 0.0)

    def score_header_row(self, values: list[Any]) -> float:
        hits = 0
        for value in values:
            key = norm_key(clean_text(value))
            if not key:
                continue
            if self.field_for_header(clean_text(value)):
                hits += 1
            elif any(k in key for k in self.hint_keywords):
                hits += 1
        return hits


class ExcelParser:
    def __init__(
        self,
        mapping_cfg: dict[str, Any] | None = None,
        profile: "Profile | None" = None,
    ):
        self.profile = profile
        self._field_override: dict[str, str] = {}
        if profile is not None:
            self.mapper = ColumnMapper({"fields": profile.columns})
        else:
            self.mapper = ColumnMapper(mapping_cfg or {})

    def parse(self, path: str | Path, sheet: str | None = None) -> ExcelParseResult:
        path = Path(path)
        result = ExcelParseResult()
        wb = load_workbook(path, data_only=True, read_only=False)
        try:
            for ws in wb.worksheets:
                if sheet and ws.title != sheet:
                    continue
                if not sheet and self.profile is not None:
                    if not self.profile.match_sheet(ws.title):
                        continue
                info = self._parse_sheet(ws, result)
                result.sheets.append(info)
        finally:
            wb.close()
        result.column_mapping = {
            str(i): f for s in result.sheets for i, f in s.columns.items()
        }
        return result

    def _parse_sheet(self, ws, result: ExcelParseResult) -> SheetInfo:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return SheetInfo(name=ws.title, header_row=0)

        header_row_idx, header_values = self._locate_header(rows)
        info = SheetInfo(name=ws.title, header_row=header_row_idx + 1)
        if header_row_idx < 0:
            result.warnings.append(f"[{ws.title}] 未识别到表头，已跳过该 Sheet")
            return info

        # —— 列 → 字段 映射（同一字段被多列命中时，取数据最完整的一列）——
        candidates: dict[str, list[tuple[int, float]]] = {}
        unmapped: dict[int, str] = {}
        for col_idx, value in enumerate(header_values):
            field_name, score = self.mapper.match_header(clean_text(value))
            header_text = clean_text(value)
            if not field_name:
                if header_text:
                    unmapped[col_idx] = header_text
                    result.unmapped_columns.append(
                        f"{ws.title}!{get_column_letter(col_idx + 1)} «{header_text}»"
                    )
                continue
            candidates.setdefault(field_name, []).append((col_idx, score))

        data_rows = [
            (idx, row)
            for idx, row in enumerate(rows[header_row_idx + 1 :], start=header_row_idx + 2)
            if row is not None and any(clean_text(v) for v in row)
        ]
        filled = self._column_fill_counts(data_rows)

        for field_name, items in candidates.items():
            items.sort(key=lambda it: (-filled.get(it[0], 0), -it[1], it[0]))
            keep_col, keep_score = items[0]
            info.columns[keep_col] = field_name
            for col_idx, _score in items[1:]:
                info.columns[col_idx] = ""
                result.unmapped_columns.append(
                    f"{ws.title}!{get_column_letter(col_idx + 1)} "
                    f"«{clean_text(header_values[col_idx])}»"
                    f"（与 {field_name} 重复，已按数据完整度取舍）"
                )
            if len(items) > 1:
                result.warnings.append(
                    f"[{ws.title}] 字段 {field_name} 命中 {len(items)} 列，"
                    f"已选择 «{clean_text(header_values[keep_col])}»"
                )

        req_no = 0
        kept: list[tuple[int, dict[str, str]]] = []
        skipped: dict[str, int] = {}
        filter_info: dict[str, Any] = {}
        for row_idx, row in data_rows:
            record = self._row_to_record(row, info.columns)
            if not any(record.values()):
                continue
            if self._is_footnote(record):
                continue
            kept.append((row_idx, record))

        if self.profile is not None and self.profile.filter_field:
            kept, filter_info = self._apply_row_filter(kept, info, result, skipped)
            # 过滤列回退时，属性取数列同步切换（如方向列 GPIO TYPE → Chip Section）
            used = filter_info.get("used_field")
            if used and used != self.profile.filter_field:
                self._field_override[self.profile.filter_field] = used

        for row_idx, record in kept:
            req_no += 1
            result.requirements.append(
                self._build_requirement(record, ws.title, row_idx, req_no)
            )
        info.row_count = req_no
        return info

    def _apply_row_filter(
        self,
        kept: list[tuple[int, dict[str, str]]],
        info: SheetInfo,
        result: ExcelParseResult,
        skipped: dict[str, int],
    ) -> tuple[list[tuple[int, dict[str, str]]], dict[str, Any]]:
        """按档案的行过滤规则筛选；主列无匹配时自动回退到备用列。

        返回 (参与核对的行, 过滤统计)。
        """
        profile = self.profile
        assert profile is not None
        field = profile.filter_field
        values = profile.filter_values
        mapped = field in info.columns.values()

        selected: list[tuple[int, dict[str, str]]] = []
        for row_idx, record in kept:
            value = (record.get(field, "") or "").strip().upper()
            if value in values:
                selected.append((row_idx, record))
            else:
                key = value or "(空)"
                skipped[key] = skipped.get(key, 0) + 1

        used_field, used_values = field, values
        fallback = False
        if not selected and profile.fallback_field:
            fb_field = profile.fallback_field
            fb_values = profile.fallback_values
            fb_selected = []
            fb_skipped: dict[str, int] = {}
            for row_idx, record in kept:
                value = (record.get(fb_field, "") or "").strip().upper()
                if value in fb_values:
                    fb_selected.append((row_idx, record))
                else:
                    key = value or "(空)"
                    fb_skipped[key] = fb_skipped.get(key, 0) + 1
            if fb_selected:
                selected = fb_selected
                skipped = fb_skipped
                used_field, used_values = fb_field, fb_values
                fallback = True

        info_stats = {
            "field": field,
            "values": values,
            "mapped": mapped,
            "kept": len(selected),
            "skipped": sum(skipped.values()),
            "skipped_values": skipped,
            "used_field": used_field,
            "used_values": used_values,
            "fallback": fallback,
        }
        result.filter_stats = info_stats

        if not selected:
            detail = "、".join(f"{k}×{v}" for k, v in skipped.items()) or "无数据行"
            if not mapped:
                result.warnings.append(
                    f"[{info.name}] 过滤列「{field}」未能在表头中找到（列映射失败），"
                    f"{sum(skipped.values())} 行全部被跳过。"
                    f"未映射的表头：{'、'.join(result.unmapped_columns) or '（无）'}"
                )
            else:
                result.warnings.append(
                    f"[{info.name}] 按「{field}」过滤后无行参与核对"
                    f"（跳过 {sum(skipped.values())} 行，取值分布：{detail}）。"
                    f"{profile.row_filter.get('empty_hint', '')}"
                )
        elif fallback:
            detail = "、".join(f"{k}×{v}" for k, v in skipped.items()) or "无"
            result.warnings.append(
                f"[{info.name}] 「{field}」列无匹配行（该列取值：{detail}），"
                f"已自动改用备用列「{used_field}」（取值 {used_values}）参与核对，"
                f"共 {len(selected)} 行。"
            )
        return selected, info_stats

    @staticmethod
    def _column_fill_counts(data_rows: list[tuple[int, tuple]]) -> dict[int, int]:
        """统计每一列的非空单元格数量，用于同字段多列时的取舍。"""
        counts: dict[int, int] = {}
        for _idx, row in data_rows:
            for col_idx, value in enumerate(row):
                if clean_text(value):
                    counts[col_idx] = counts.get(col_idx, 0) + 1
        return counts

    def _locate_header(self, rows: list[tuple]) -> tuple[int, list[Any]]:
        best_idx, best_score = -1, 0.0
        for idx, row in enumerate(rows[:15]):
            score = self.mapper.score_header_row(list(row))
            if score > best_score:
                best_idx, best_score = idx, score
        if best_idx < 0 or best_score < 2:
            return -1, []
        return best_idx, list(rows[best_idx])

    def _row_to_record(
        self, row: tuple, columns: dict[int, str]
    ) -> dict[str, str]:
        record: dict[str, str] = {}
        for col_idx, value in enumerate(row):
            field_name = columns.get(col_idx, "")
            if not field_name:
                continue
            record[field_name] = clean_text(value)
        return record

    @staticmethod
    def _is_footnote(record: dict[str, str]) -> bool:
        keys = [k for k in record if k]
        if not keys:
            return True
        filled = [v for v in record.values() if v]
        if len(filled) <= 1 and keys and all(
            k not in {"pin_name", "gpio_num", "function", "config_key", "expected_value"}
            for k in keys
        ):
            return True
        first = next(iter(record.values()), "")
        if first.strip() in {"合计", "总计", "备注", "说明", "以上", "注：", "注:"}:
            return True
        return False

    def _build_requirement(
        self, record: dict[str, str], sheet: str, row_no: int, seq: int
    ) -> GPIORequirement:
        pin_raw = record.get("pin_name", "")
        pin_key, _ = norm_pin(pin_raw)
        gpio_num = norm_gpio_num(record.get("gpio_num", ""))
        if gpio_num is None:
            gpio_num = norm_gpio_num(record.get("expected_value", ""))
        config_key = record.get("config_key", "")
        expected = record.get("expected_value", "")
        requirement = GPIORequirement(
            id=f"R{seq:04d}",
            sheet=sheet,
            row_no=row_no,
            pin_name_raw=pin_raw,
            pin_key=pin_key,
            gpio_num=gpio_num,
            function_name=record.get("function", ""),
            config_key=config_key,
            config_key_norm=norm_key(config_key),
            expected_value=expected,
            expected_normalized=norm_value(expected),
            chip_instance=record.get("chip_instance", ""),
            polarity=record.get("polarity", ""),
            pull=record.get("pull", ""),
            mux=record.get("mux", ""),
            bom_ref=record.get("bom_ref", ""),
            remark=record.get("remark", ""),
            raw=record,
        )
        if self.profile is not None:
            self._apply_profile(requirement, record)
        return requirement

    def _apply_profile(
        self, requirement: GPIORequirement, record: dict[str, str]
    ) -> None:
        """按档案把一行拆成多个待核对属性。"""
        profile = self.profile
        assert profile is not None
        net = record.get("net_name", "") or record.get("config_key", "")
        requirement.net_name = net
        requirement.config_key = net
        requirement.config_key_norm = norm_key(net)
        for spec in profile.attributes:
            source_field = self._field_override.get(spec.from_field, spec.from_field)
            raw = record.get(source_field, "") if source_field else ""
            is_na = profile.is_na(raw) if raw else False
            requirement.attributes.append(
                ExpectedAttribute(
                    name=spec.name,
                    label=spec.label,
                    source_field=source_field,
                    value=raw,
                    normalized="" if is_na else profile.map_value(spec.name, raw),
                    checkable=spec.checkable and bool(raw) and not is_na,
                    check=spec.check,
                    note="Excel 标注为 NA，不参与判定" if is_na else "",
                )
            )
        primary = next(
            (a for a in requirement.attributes if a.check == "port_bit"),
            None,
        )
        if primary is not None:
            requirement.expected_value = primary.value
            requirement.expected_normalized = primary.normalized
