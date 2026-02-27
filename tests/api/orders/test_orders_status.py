"""API tests — PUT /api/orders/:id/status (Order Status Transitions)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.order import OrderFromResponse
from sales_portal_tests.data.sales_portal.orders.orders_status_ddt import (
    NEGATIVE_ORDER_STATUS_TRANSITIONS,
    POSITIVE_ORDER_STATUS_TRANSITIONS,
    OrderStatusTransitionCase,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.utils.validation.validate_response import validate_response


def _get_order_via_factory(
    orders_service: OrdersApiService,
    factory_name: str,
    products_count: int,
    token: str,
) -> OrderFromResponse:
    """Dispatch to the correct ``OrdersApiService`` factory method by name."""
    factory = getattr(orders_service, factory_name)
    return factory(token, products_count)  # type: ignore[no-any-return]


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestOrderStatusTransitions:
    """Tests for PUT /api/orders/:id/status."""

    # ------------------------------------------------------------------
    # Positive DDT — valid transitions
    # ------------------------------------------------------------------

    @allure.title("Order status transition — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", POSITIVE_ORDER_STATUS_TRANSITIONS)
    def test_order_status_transition_positive(
        self,
        case: OrderStatusTransitionCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order in the required initial state, transition it and validate."""
        order = _get_order_via_factory(orders_service, case.order_factory, case.products_count, admin_token)
        cleanup.orders.add(order.id)

        response = orders_api.update_status(order.id, case.to, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        assert (
            body["Order"]["status"] == case.to.value
        ), f"Expected status {case.to.value!r}, got {body['Order']['status']!r}"

    # ------------------------------------------------------------------
    # Negative DDT — invalid / forbidden transitions
    # ------------------------------------------------------------------

    @allure.title("Order status transition — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", NEGATIVE_ORDER_STATUS_TRANSITIONS)
    def test_order_status_transition_negative(
        self,
        case: OrderStatusTransitionCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt a forbidden status transition; expect the specified error response."""
        order = _get_order_via_factory(orders_service, case.order_factory, case.products_count, admin_token)
        cleanup.orders.add(order.id)

        response = orders_api.update_status(order.id, case.to, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
