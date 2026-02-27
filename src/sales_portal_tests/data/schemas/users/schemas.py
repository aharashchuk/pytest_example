"""JSON Schemas for user API endpoints."""

from typing import Any

from sales_portal_tests.data.models.user import Roles
from sales_portal_tests.data.schemas.core_schema import OBLIGATORY_FIELDS_SCHEMA, OBLIGATORY_REQUIRED_FIELDS

USER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "roles": {
            "type": "array",
            "items": {"type": "string", "enum": [r.value for r in Roles]},
        },
        "createdOn": {"type": "string"},
    },
    "required": ["_id", "username", "firstName", "lastName", "roles", "createdOn"],
    "additionalProperties": False,
}

GET_USER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "User": USER_SCHEMA,
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["User", *OBLIGATORY_REQUIRED_FIELDS],
    "additionalProperties": False,
}

GET_ALL_USERS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Users": {
            "type": "array",
            "items": USER_SCHEMA,
        },
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Users", *OBLIGATORY_REQUIRED_FIELDS],
    "additionalProperties": False,
}
