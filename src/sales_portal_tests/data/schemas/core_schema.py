"""Core JSON Schema fragments shared by all response schemas."""

from typing import Any

OBLIGATORY_FIELDS_SCHEMA: dict[str, Any] = {
    "IsSuccess": {"type": "boolean"},
    "ErrorMessage": {"type": ["string", "null"]},
}

OBLIGATORY_REQUIRED_FIELDS: list[str] = ["IsSuccess", "ErrorMessage"]
