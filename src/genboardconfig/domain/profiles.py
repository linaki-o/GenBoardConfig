"""档案（Profile）：把「表结构 → 比对规则」外置为可配置数据。"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AttributeSpec:
    name: str
    label: str = ""
    from_field: str = ""
    check: str = "none"          # symbol | port_bit | none
    checkable: bool = True

    def __post_init__(self) -> None:
        if not self.label:
            self.label = self.name
        if self.check == "none":
            self.checkable = False


@dataclass
class Profile:
    id: str = "generic"
    name: str = ""
    excel_sheet: str = ""
    header_keywords: list[str] = field(default_factory=list)
    columns: dict[str, list[str]] = field(default_factory=dict)
    attributes: list[AttributeSpec] = field(default_factory=list)
    value_map: dict[str, dict[str, str]] = field(default_factory=dict)
    na_values: list[str] = field(default_factory=list)
    c_config: dict[str, Any] = field(default_factory=dict)
    row_filter: dict[str, Any] = field(default_factory=dict)
    path: Path | None = None

    # ---------- 加载 ----------
    @classmethod
    def load(cls, path: str | Path) -> "Profile":
        path = Path(path)
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        excel = data.get("excel", {}) or {}
        attributes = [
            AttributeSpec(
                name=item.get("name", ""),
                label=item.get("label", ""),
                from_field=item.get("from", ""),
                check=item.get("check", "none"),
            )
            for item in (excel.get("attributes") or [])
        ]
        return cls(
            id=data.get("id", path.stem),
            name=data.get("name", path.stem),
            excel_sheet=excel.get("sheet", ""),
            header_keywords=[str(k).lower() for k in (excel.get("header_keywords") or [])],
            columns={k: [str(a).lower() for a in v] for k, v in (excel.get("columns") or {}).items()},
            attributes=attributes,
            value_map=excel.get("value_map", {}) or {},
            na_values=[str(v).strip().upper() for v in (excel.get("na_values") or [])],
            c_config=data.get("c_config", {}) or {},
            row_filter=excel.get("row_filter", {}) or {},
            path=path,
        )

    def is_na(self, value: str) -> bool:
        """单元格是否为「不适用」占位值（NA / N/A / -）。"""
        text = (value or "").strip().upper()
        if not text:
            return False
        return text in set(self.na_values)

    # ---------- 行过滤 ----------
    @property
    def filter_field(self) -> str:
        return str(self.row_filter.get("field") or "")

    @property
    def filter_values(self) -> list[str]:
        return [str(v).strip().upper() for v in (self.row_filter.get("values") or [])]

    @property
    def fallback_field(self) -> str:
        fallback = self.row_filter.get("fallback") or {}
        return str(fallback.get("field") or "")

    @property
    def fallback_values(self) -> list[str]:
        fallback = self.row_filter.get("fallback") or {}
        return [str(v).strip().upper() for v in (fallback.get("values") or [])]

    def passes_filter(self, record: dict[str, str]) -> bool:
        field = self.filter_field
        if not field or not self.filter_values:
            return True
        value = (record.get(field, "") or "").strip().upper()
        return value in self.filter_values

    def passes_fallback(self, record: dict[str, str]) -> bool:
        field = self.fallback_field
        if not field or not self.fallback_values:
            return True
        value = (record.get(field, "") or "").strip().upper()
        return value in self.fallback_values

    def apply_override(self, override: dict[str, Any] | None) -> None:
        """应用本地覆盖（如在设置页切换行过滤列）。"""
        if not override:
            return
        if "field" in override:
            self.row_filter["field"] = override["field"]
        if "values" in override:
            self.row_filter["values"] = override["values"]
        if "empty_hint" in override:
            self.row_filter["empty_hint"] = override["empty_hint"]

    def override(self) -> dict[str, Any]:
        return {
            "field": self.filter_field,
            "values": self.filter_values,
            "empty_hint": self.row_filter.get("empty_hint", ""),
        }


    @classmethod
    def load_dir(cls, directory: str | Path) -> list["Profile"]:
        directory = Path(directory)
        if not directory.exists():
            return []
        profiles = []
        for path in sorted(directory.glob("*.yaml")):
            try:
                profiles.append(cls.load(path))
            except Exception:  # noqa: BLE001
                continue
        return profiles

    # ---------- 判定 ----------
    def match_sheet(self, sheet_name: str) -> bool:
        return not self.excel_sheet or self.excel_sheet.lower() == sheet_name.lower()

    def score_headers(self, headers: list[str]) -> float:
        if not headers:
            return 0.0
        lowered = [str(h).lower() for h in headers]
        hits = 0
        for keyword in self.header_keywords:
            if any(keyword in h for h in lowered):
                hits += 1
        return hits / max(1, len(self.header_keywords))

    def attribute(self, name: str) -> AttributeSpec | None:
        for spec in self.attributes:
            if spec.name == name:
                return spec
        return None

    def map_value(self, attr_name: str, raw: str) -> str:
        mapping = self.value_map.get(attr_name, {}) or {}
        text = (raw or "").strip()
        if text in mapping:
            return mapping[text]
        for key, value in mapping.items():
            if key.lower() == text.lower():
                return value
        return text.upper()

    def c_cfg(self, *keys: str, default: Any = None) -> Any:
        node: Any = self.c_config
        for key in keys:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node
