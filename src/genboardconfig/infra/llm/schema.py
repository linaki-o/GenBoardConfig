"""LLM 结构化输出契约。"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

StatusLiteral = Literal[
    "match", "mismatch", "missing", "ambiguous", "not_applicable", "unresolved"
]


class LlmEvidence(BaseModel):
    entry_id: str = ""
    line: int = 0
    snippet: str = ""


class LlmProposedChange(BaseModel):
    type: Literal[
        "set_macro", "set_struct_field", "set_array_item", "insert_block", "none"
    ] = "none"
    target: str = ""
    old_value: str = ""
    new_value: str = ""
    reason: str = ""


class LlmCheckItem(BaseModel):
    requirement_id: str
    status: StatusLiteral = "unresolved"
    matched_entry_ids: list[str] = Field(default_factory=list)
    current_value: str = ""
    expected_value: str = ""
    confidence: float = 0.0
    evidence: list[LlmEvidence] = Field(default_factory=list)
    proposed_change: LlmProposedChange = Field(default_factory=LlmProposedChange)
    notes: str = ""


class LlmCheckResponse(BaseModel):
    items: list[LlmCheckItem] = Field(default_factory=list)
    unresolved_reason: str = ""


class LlmColumnItem(BaseModel):
    index: int
    field: str = ""
    confidence: float = 0.0


class LlmColumnResponse(BaseModel):
    columns: list[LlmColumnItem] = Field(default_factory=list)


class LlmSymbolItem(BaseModel):
    net_name: str
    group: str = ""
    confidence: float = 0.0
    reason: str = ""


class LlmSymbolResponse(BaseModel):
    mappings: list[LlmSymbolItem] = Field(default_factory=list)


class LlmFunctionItem(BaseModel):
    requirement_id: str
    equivalent: bool = False
    confidence: float = 0.0
    reason: str = ""


class LlmFunctionResponse(BaseModel):
    results: list[LlmFunctionItem] = Field(default_factory=list)


FUNCTION_JSON_SCHEMA: dict[str, Any] = {
    "name": "function_equivalence",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "results": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "requirement_id": {"type": "string"},
                        "equivalent": {"type": "boolean"},
                        "confidence": {"type": "number"},
                        "reason": {"type": "string"},
                    },
                    "required": ["requirement_id", "equivalent", "confidence", "reason"],
                },
            }
        },
        "required": ["results"],
    },
}


SYMBOL_JSON_SCHEMA: dict[str, Any] = {
    "name": "symbol_mapping",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "mappings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "net_name": {"type": "string"},
                        "group": {"type": "string"},
                        "confidence": {"type": "number"},
                        "reason": {"type": "string"},
                    },
                    "required": ["net_name", "group", "confidence", "reason"],
                },
            }
        },
        "required": ["mappings"],
    },
}


CHECK_JSON_SCHEMA: dict[str, Any] = {
    "name": "gpio_check_result",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "requirement_id": {"type": "string"},
                        "status": {"type": "string", "enum": list(StatusLiteral.__args__)},
                        "matched_entry_ids": {"type": "array", "items": {"type": "string"}},
                        "current_value": {"type": "string"},
                        "expected_value": {"type": "string"},
                        "confidence": {"type": "number"},
                        "evidence": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "properties": {
                                    "entry_id": {"type": "string"},
                                    "line": {"type": "integer"},
                                    "snippet": {"type": "string"},
                                },
                                "required": ["entry_id", "line", "snippet"],
                            },
                        },
                        "proposed_change": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "type": {
                                    "type": "string",
                                    "enum": [
                                        "set_macro",
                                        "set_struct_field",
                                        "set_array_item",
                                        "insert_block",
                                        "none",
                                    ],
                                },
                                "target": {"type": "string"},
                                "old_value": {"type": "string"},
                                "new_value": {"type": "string"},
                                "reason": {"type": "string"},
                            },
                            "required": ["type", "target", "old_value", "new_value", "reason"],
                        },
                        "notes": {"type": "string"},
                    },
                    "required": [
                        "requirement_id",
                        "status",
                        "matched_entry_ids",
                        "current_value",
                        "expected_value",
                        "confidence",
                        "evidence",
                        "proposed_change",
                        "notes",
                    ],
                },
            },
            "unresolved_reason": {"type": "string"},
        },
        "required": ["items", "unresolved_reason"],
    },
}

COLUMN_JSON_SCHEMA: dict[str, Any] = {
    "name": "column_identification",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "columns": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "index": {"type": "integer"},
                        "field": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                    "required": ["index", "field", "confidence"],
                },
            }
        },
        "required": ["columns"],
    },
}
