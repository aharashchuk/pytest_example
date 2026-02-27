"""JSON Schemas for customer API endpoints."""

from typing import Any

from sales_portal_tests.data.schemas.core_schema import OBLIGATORY_FIELDS_SCHEMA, OBLIGATORY_REQUIRED_FIELDS
from sales_portal_tests.data.schemas.customers.customer_schema import CUSTOMER_SCHEMA

CREATE_CUSTOMER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Customer": CUSTOMER_SCHEMA,
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Customer", *OBLIGATORY_REQUIRED_FIELDS],
}

GET_BY_ID_CUSTOMER_SCHEMA: dict[str, Any] = CREATE_CUSTOMER_SCHEMA

UPDATE_CUSTOMER_SCHEMA: dict[str, Any] = CREATE_CUSTOMER_SCHEMA

GET_ALL_CUSTOMERS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Customers": {
            "type": "array",
            "items": CUSTOMER_SCHEMA,
        },
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Customers", *OBLIGATORY_REQUIRED_FIELDS],
}

GET_LIST_CUSTOMERS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Customers": {
            "type": "array",
            "items": CUSTOMER_SCHEMA,
        },
        "total": {"type": "number"},
        "page": {"type": "number"},
        "limit": {"type": "number"},
        "search": {"type": "string"},
        "country": {"type": "array"},
        "sorting": {"type": "object"},
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Customers", *OBLIGATORY_REQUIRED_FIELDS],
}
