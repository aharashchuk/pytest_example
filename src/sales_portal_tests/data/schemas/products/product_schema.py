"""JSON Schema for a single product object."""

from typing import Any

from sales_portal_tests.data.sales_portal.products.manufacturers import Manufacturers

PRODUCT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string"},
        "amount": {"type": "number"},
        "price": {"type": "number"},
        "createdOn": {"type": "string"},
        "notes": {"type": "string"},
        "manufacturer": {
            "type": "string",
            "enum": [m.value for m in Manufacturers],
        },
    },
    "required": ["_id", "name", "amount", "price", "manufacturer", "createdOn"],
    "additionalProperties": False,
}
