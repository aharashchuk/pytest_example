"""DDT cases for PATCH /api/orders/:id/status (order status transitions)."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.status_codes import StatusCodes


@dataclass
class OrderStatusTransitionCase:
    """Case for an order status transition test.

    ``from_state`` describes the initial state in human-readable form.
    ``order_factory`` is a string key that maps to an orders-service factory
    method in the fixture (e.g. ``"create_order_with_delivery"``).
    ``products_count`` is passed to the factory.
    """

    from_state: str
    order_factory: str
    products_count: int
    to: OrderStatus
    expected_status: StatusCodes
    expected_error_message: str | None
    is_success: bool = True


POSITIVE_ORDER_STATUS_TRANSITIONS = [
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Draft with delivery",
            order_factory="create_order_with_delivery",
            products_count=1,
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="draft-with-delivery-to-processing",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Draft with delivery",
            order_factory="create_order_with_delivery",
            products_count=1,
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="draft-with-delivery-to-canceled",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Draft",
            order_factory="create_order_and_entities",
            products_count=1,
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="draft-to-canceled",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Canceled",
            order_factory="create_canceled_order",
            products_count=1,
            to=OrderStatus.DRAFT,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="canceled-to-draft",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="In Process",
            order_factory="create_order_in_process",
            products_count=1,
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="processing-to-canceled",
    ),
]

NEGATIVE_ORDER_STATUS_TRANSITIONS = [
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Draft",
            order_factory="create_order_and_entities",
            products_count=1,
            to=OrderStatus.DRAFT,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Can't reopen not canceled order",
            is_success=False,
        ),
        id="draft-to-draft",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Draft",
            order_factory="create_order_and_entities",
            products_count=1,
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Can't process order. Please, schedule delivery",
            is_success=False,
        ),
        id="draft-to-processing-no-delivery",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="In Process",
            order_factory="create_order_in_process",
            products_count=1,
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="processing-to-processing",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="In Process",
            order_factory="create_order_in_process",
            products_count=1,
            to=OrderStatus.DRAFT,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Can't reopen not canceled order",
            is_success=False,
        ),
        id="processing-to-draft",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Partially Received",
            order_factory="create_partially_received_order",
            products_count=2,
            to=OrderStatus.DRAFT,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Can't reopen not canceled order",
            is_success=False,
        ),
        id="partially-received-to-draft",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Partially Received",
            order_factory="create_partially_received_order",
            products_count=2,
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="partially-received-to-processing",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Partially Received",
            order_factory="create_partially_received_order",
            products_count=2,
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="partially-received-to-canceled",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Received",
            order_factory="create_received_order",
            products_count=1,
            to=OrderStatus.DRAFT,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Can't reopen not canceled order",
            is_success=False,
        ),
        id="received-to-draft",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Received",
            order_factory="create_received_order",
            products_count=1,
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="received-to-processing",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Received",
            order_factory="create_received_order",
            products_count=1,
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="received-to-canceled",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Canceled",
            order_factory="create_canceled_order",
            products_count=1,
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="canceled-to-canceled",
    ),
    pytest.param(
        OrderStatusTransitionCase(
            from_state="Canceled",
            order_factory="create_canceled_order",
            products_count=1,
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Invalid order status",
            is_success=False,
        ),
        id="canceled-to-processing",
    ),
]

INVALID_STATUSES: list[object] = ["testStatus", "", None, 12345, None]
