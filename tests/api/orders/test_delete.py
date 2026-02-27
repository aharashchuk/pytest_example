"""API tests — DELETE /api/orders/:id (Delete Order)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.orders.create_order_test_data import (
    DELETE_ORDER_CASES,
    CreateOrderCase,
)
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestDeleteOrder:
    """Tests for DELETE /api/orders/:id."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Delete order — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", DELETE_ORDER_CASES)
    def test_delete_order_positive(
        self,
        case: CreateOrderCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order with the specified product count, delete it (204), then verify 404."""
        order = orders_service.create_order_and_entities(admin_token, num_products=case.products_count)
        # Entities are tracked in orders_service.entities_store (set by the cleanup fixture)

        delete_response = orders_api.delete(admin_token, order.id)
        # Remove from cleanup store so teardown doesn't try to delete it again
        cleanup.orders.discard(order.id)

        validate_response(
            delete_response,
            status=case.expected_status,
            error_message=case.expected_error_message,
        )

        # Verify the order no longer exists
        get_response = orders_api.get_by_id(order.id, admin_token)
        validate_response(
            get_response,
            status=StatusCodes.NOT_FOUND,
        )

    # ------------------------------------------------------------------
    # Negative — delete non-existing order
    # ------------------------------------------------------------------

    @allure.title("Delete order — non-existing order ID returns 404")  # type: ignore[misc]
    @pytest.mark.regression
    def test_delete_non_existing_order(
        self,
        orders_api: OrdersApi,
        admin_token: str,
    ) -> None:
        """Attempting to delete a non-existing order should return 404."""
        non_existing_id = "000000000000000000000000"

        response = orders_api.delete(admin_token, non_existing_id)

        validate_response(
            response,
            status=StatusCodes.NOT_FOUND,
            is_success=False,
        )
