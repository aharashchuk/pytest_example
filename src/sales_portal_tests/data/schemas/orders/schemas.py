"""JSON Schemas for order API endpoints."""

from typing import Any

from sales_portal_tests.data.sales_portal.order_status import OrderHistoryActions, OrderStatus
from sales_portal_tests.data.schemas.core_schema import OBLIGATORY_FIELDS_SCHEMA, OBLIGATORY_REQUIRED_FIELDS
from sales_portal_tests.data.schemas.customers.customer_schema import CUSTOMER_SCHEMA
from sales_portal_tests.data.schemas.delivery.schemas import DELIVERY_INFO_SCHEMA
from sales_portal_tests.data.schemas.users.schemas import USER_SCHEMA

ORDER_PRODUCT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string"},
        "amount": {"type": "number"},
        "price": {"type": "number"},
        "manufacturer": {"type": "string"},
        "notes": {"type": "string"},
        "received": {"type": "boolean"},
    },
    "required": ["_id", "name", "amount", "price", "manufacturer", "notes", "received"],
    "additionalProperties": False,
}

COMMENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "text": {"type": "string"},
        "createdOn": {"type": "string"},
    },
    "required": ["_id", "text", "createdOn"],
    "additionalProperties": False,
}

PERFORMER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "username": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "roles": {"type": "array", "items": {"type": "string"}},
        "createdOn": {"type": "string"},
    },
    "required": ["_id", "username", "firstName", "lastName", "roles", "createdOn"],
    "additionalProperties": False,
}

ORDER_HISTORY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": [s.value for s in OrderStatus]},
        "customer": {"type": "string"},
        "products": {"type": "array", "items": ORDER_PRODUCT_SCHEMA},
        "total_price": {"type": "number"},
        "delivery": {"anyOf": [DELIVERY_INFO_SCHEMA, {"type": "null"}]},
        "assignedManager": {"anyOf": [USER_SCHEMA, {"type": "null"}]},
        "changedOn": {"type": "string"},
        "action": {"type": "string", "enum": [a.value for a in OrderHistoryActions]},
        "performer": PERFORMER_SCHEMA,
    },
    "required": [
        "status",
        "customer",
        "products",
        "total_price",
        "delivery",
        "assignedManager",
        "changedOn",
        "action",
        "performer",
    ],
    "additionalProperties": False,
}

ORDER_FROM_RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "status": {"type": "string", "enum": [s.value for s in OrderStatus]},
        "customer": CUSTOMER_SCHEMA,
        "products": {"type": "array", "items": ORDER_PRODUCT_SCHEMA},
        "delivery": {"anyOf": [DELIVERY_INFO_SCHEMA, {"type": "null"}]},
        "total_price": {"type": "number"},
        "createdOn": {"type": "string"},
        "comments": {"type": "array", "items": COMMENT_SCHEMA},
        "history": {"type": "array", "items": ORDER_HISTORY_SCHEMA},
        "assignedManager": {"anyOf": [USER_SCHEMA, {"type": "null"}]},
    },
    "required": [
        "_id",
        "status",
        "customer",
        "products",
        "total_price",
        "createdOn",
        "comments",
        "history",
        "assignedManager",
        "delivery",
    ],
    "additionalProperties": False,
}

CREATE_ORDER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "Order": ORDER_FROM_RESPONSE_SCHEMA,
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": ["Order", *OBLIGATORY_REQUIRED_FIELDS],
    "additionalProperties": False,
}

GET_ORDER_SCHEMA: dict[str, Any] = CREATE_ORDER_SCHEMA

GET_ALL_ORDERS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "orders": {
            "type": "array",
            "items": ORDER_FROM_RESPONSE_SCHEMA,
        },
        "total": {"type": "number"},
        "page": {"type": "number"},
        "limit": {"type": "number"},
        "search": {"type": "string"},
        "status": {
            "type": "array",
            "items": {"type": "string", "enum": [s.value for s in OrderStatus]},
        },
        "sorting": {
            "type": "object",
            "properties": {
                "sortField": {
                    "type": "string",
                    "enum": [
                        "orderNumber",
                        "email",
                        "price",
                        "delivery",
                        "status",
                        "assignedManager",
                        "createdOn",
                    ],
                },
                "sortOrder": {"type": "string", "enum": ["asc", "desc"]},
            },
            "required": ["sortField", "sortOrder"],
            "additionalProperties": False,
        },
        **OBLIGATORY_FIELDS_SCHEMA,
    },
    "required": [
        "orders",
        "total",
        "page",
        "limit",
        "search",
        "status",
        "sorting",
        *OBLIGATORY_REQUIRED_FIELDS,
    ],
    "additionalProperties": False,
}
