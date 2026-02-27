"""JSON Schema for login endpoint."""

from typing import Any

from sales_portal_tests.data.schemas.core_schema import OBLIGATORY_FIELDS_SCHEMA, OBLIGATORY_REQUIRED_FIELDS

LOGIN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": [*OBLIGATORY_REQUIRED_FIELDS],
}
