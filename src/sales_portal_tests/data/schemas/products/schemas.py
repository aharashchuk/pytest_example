"""JSON Schemas for product API endpoints."""

from typing import Any

from sales_portal_tests.data.schemas.core_schema import OBLIGATORY_FIELDS_SCHEMA, OBLIGATORY_REQUIRED_FIELDS
from sales_portal_tests.data.schemas.products.product_schema import PRODUCT_SCHEMA

CREATE_PRODUCT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Product": PRODUCT_SCHEMA,
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Product", *OBLIGATORY_REQUIRED_FIELDS],
}

# GET /products/:id returns the same shape as CREATE
GET_PRODUCT_SCHEMA: dict[str, Any] = CREATE_PRODUCT_SCHEMA

GET_ALL_PRODUCTS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Products": {
            "type": "array",
            "items": PRODUCT_SCHEMA,
        },
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Products", *OBLIGATORY_REQUIRED_FIELDS],
}
