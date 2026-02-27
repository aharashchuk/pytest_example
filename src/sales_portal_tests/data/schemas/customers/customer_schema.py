"""JSON Schema for a single customer object."""

from typing import Any

from sales_portal_tests.data.sales_portal.country import Country

CUSTOMER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "email": {"type": "string"},
        "name": {"type": "string"},
        "country": {"type": "string", "enum": [c.value for c in Country]},
        "city": {"type": "string"},
        "street": {"type": "string"},
        "house": {"type": "number"},
        "flat": {"type": "number"},
        "phone": {"type": "string"},
        "notes": {"type": "string"},
        "createdOn": {"type": "string"},
    },
    "required": [
        "_id",
        "email",
        "name",
        "country",
        "city",
        "street",
        "house",
        "flat",
        "phone",
        "createdOn",
    ],
}
