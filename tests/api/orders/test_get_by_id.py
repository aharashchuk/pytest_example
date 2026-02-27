"""API tests — GET /api/orders/:id (Get Order By ID)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.orders.get_order_by_id_test_data import (
    GET_ORDER_BY_ID_NEGATIVE_CASES,
    GET_ORDER_BY_ID_POSITIVE_CASES,
    _invalid_id,
    _not_found_id,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestGetOrderById:
    """Tests for GET /api/orders/:id."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Get order by valid ID — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_ORDER_BY_ID_POSITIVE_CASES)
    def test_get_order_by_id_positive(
        self,
        case: CaseApi,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order then fetch it by ID; response shape and fields must be valid."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        response = orders_api.get_by_id(order.id, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=True,
            error_message=case.expected_error_message,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        fetched = body["Order"]

        assert fetched["_id"] == order.id, f"Expected order id {order.id!r}, got {fetched['_id']!r}"
        assert fetched["customer"]["_id"] == order.customer.id

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT get order by invalid ID — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_ORDER_BY_ID_NEGATIVE_CASES)
    def test_get_order_by_id_negative(
        self,
        case: CaseApi,
        orders_api: OrdersApi,
        admin_token: str,
    ) -> None:
        """Fetching with a non-existing or invalid ID should return the expected error."""
        order_id = _invalid_id if case.expected_status == StatusCodes.SERVER_ERROR else _not_found_id

        response = orders_api.get_by_id(order_id, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
