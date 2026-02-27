"""DDT cases for POST /api/orders/:id/receive."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.status_codes import StatusCodes


@dataclass
class ReceiveProductsPositiveCase:
    title: str
    order_products_count: int
    receive_products_count: int
    expected_order_status: OrderStatus


@dataclass
class ReceiveProductsNegativeStatusCase:
    title: str
    order_factory: str
    """Key mapping to an orders-service factory (e.g. 'create_order_with_delivery')."""
    receive_products_count: int
    expected_status: StatusCodes
    expected_error_message: str | None


@dataclass
class ReceiveProductsInvalidPayloadCase:
    title: str
    build_products_description: str
    """Human-readable description of how to build the products list; logic lives in fixture."""
    extra_product_ids: list[str] = field(default_factory=list)
    expected_status: StatusCodes = StatusCodes.BAD_REQUEST
    expected_error_message: str | None = None


RECEIVE_PRODUCTS_POSITIVE_CASES = [
    pytest.param(
        ReceiveProductsPositiveCase(
            title="Processing: receive 1 product (becomes Partially Received)",
            order_products_count=5,
            receive_products_count=1,
            expected_order_status=OrderStatus.PARTIALLY_RECEIVED,
        ),
        id="receive-1-of-5-partially-received",
    ),
    pytest.param(
        ReceiveProductsPositiveCase(
            title="Processing: receive 3 products (becomes Partially Received)",
            order_products_count=5,
            receive_products_count=3,
            expected_order_status=OrderStatus.PARTIALLY_RECEIVED,
        ),
        id="receive-3-of-5-partially-received",
    ),
    pytest.param(
        ReceiveProductsPositiveCase(
            title="Processing: receive 5 products (becomes Received)",
            order_products_count=5,
            receive_products_count=5,
            expected_order_status=OrderStatus.RECEIVED,
        ),
        id="receive-5-of-5-received",
    ),
]

RECEIVE_PRODUCTS_NEGATIVE_STATUS_CASES = [
    pytest.param(
        ReceiveProductsNegativeStatusCase(
            title="Draft status",
            order_factory="create_order_with_delivery",
            receive_products_count=1,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INVALID_ORDER_STATUS,
        ),
        id="draft-status",
    ),
    pytest.param(
        ReceiveProductsNegativeStatusCase(
            title="Received status (already fully received)",
            order_factory="create_received_order",
            receive_products_count=1,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INVALID_ORDER_STATUS,
        ),
        id="already-received",
    ),
]

RECEIVE_PRODUCTS_INVALID_PAYLOAD_CASES = [
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="More than 5 products in request",
            build_products_description="take first 5 product ids and duplicate one",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
        ),
        id="more-than-5-products",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Empty products array",
            build_products_description="empty list",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
        ),
        id="empty-products",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Invalid product id: null string",
            build_products_description="list with null element",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
        ),
        id="null-product-id",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Invalid product id: UUID string",
            build_products_description="list with UUID",
            extra_product_ids=["985a82b8-4a55-439c-b458-57341cedeb94"],
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.product_not_requested("985a82b8-4a55-439c-b458-57341cedeb94"),
        ),
        id="uuid-product-id",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Invalid product id: dummy string",
            build_products_description="list with dummy string id",
            extra_product_ids=["dummy"],
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.product_not_requested("dummy"),
        ),
        id="dummy-product-id",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Invalid product id: negative value string",
            build_products_description="list with negative value as string",
            extra_product_ids=["-1"],
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.product_not_requested("-1"),
        ),
        id="negative-product-id",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Invalid product id: date string",
            build_products_description="list with date as id",
            extra_product_ids=["2025-12-21"],
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.product_not_requested("2025-12-21"),
        ),
        id="date-product-id",
    ),
    pytest.param(
        ReceiveProductsInvalidPayloadCase(
            title="Product id with non-existing id",
            build_products_description="list with non-existing zero-hex id",
            extra_product_ids=["000000000000000000000000"],
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.product_not_requested("000000000000000000000000"),
        ),
        id="non-existing-product-id",
    ),
]
