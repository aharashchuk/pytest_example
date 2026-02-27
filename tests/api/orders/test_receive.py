"""API tests — POST /api/orders/:id/receive (Receive Products)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.orders.receive_ddt import (
    RECEIVE_PRODUCTS_INVALID_PAYLOAD_CASES,
    RECEIVE_PRODUCTS_NEGATIVE_STATUS_CASES,
    RECEIVE_PRODUCTS_POSITIVE_CASES,
    ReceiveProductsInvalidPayloadCase,
    ReceiveProductsNegativeStatusCase,
    ReceiveProductsPositiveCase,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestReceiveProducts:
    """Tests for POST /api/orders/:id/receive."""

    # ------------------------------------------------------------------
    # Positive DDT — valid receive operations
    # ------------------------------------------------------------------

    @allure.title("Receive products — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", RECEIVE_PRODUCTS_POSITIVE_CASES)
    def test_receive_products_positive(
        self,
        case: ReceiveProductsPositiveCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order in process, receive a subset of products, verify resulting status."""
        order = orders_service.create_order_in_process(admin_token, num_products=case.order_products_count)
        cleanup.orders.add(order.id)

        product_ids_to_receive = [p.id for p in order.products[: case.receive_products_count]]

        response = orders_api.receive_products(order.id, product_ids_to_receive, admin_token)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        assert (
            body["Order"]["status"] == case.expected_order_status.value
        ), f"Expected status {case.expected_order_status.value!r}, got {body['Order']['status']!r}"

    # ------------------------------------------------------------------
    # Negative DDT — wrong order status
    # ------------------------------------------------------------------

    @allure.title("Should NOT receive products — wrong order status: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", RECEIVE_PRODUCTS_NEGATIVE_STATUS_CASES)
    def test_receive_products_wrong_status(
        self,
        case: ReceiveProductsNegativeStatusCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to receive products from an order in a non-processing status."""
        order = getattr(orders_service, case.order_factory)(admin_token, case.receive_products_count)
        cleanup.orders.add(order.id)

        product_ids = [p.id for p in order.products[:1]]
        response = orders_api.receive_products(order.id, product_ids, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=False,
            error_message=case.expected_error_message,
        )

    # ------------------------------------------------------------------
    # Negative DDT — invalid product ID payload
    # ------------------------------------------------------------------

    @allure.title("Should NOT receive products — invalid payload: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", RECEIVE_PRODUCTS_INVALID_PAYLOAD_CASES)
    def test_receive_products_invalid_payload(
        self,
        case: ReceiveProductsInvalidPayloadCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to receive products with an invalid payload; expect an error response."""
        order = orders_service.create_order_in_process(admin_token, num_products=5)
        cleanup.orders.add(order.id)

        desc = case.build_products_description

        if desc == "empty list":
            product_ids: list[str] = []
        elif desc == "list with null element":
            product_ids = [None]  # type: ignore[list-item]
        elif desc == "take first 5 product ids and duplicate one":
            product_ids = [p.id for p in order.products[:5]] + [order.products[0].id]
        elif case.extra_product_ids:
            product_ids = case.extra_product_ids
        else:
            product_ids = []

        response = orders_api.receive_products(order.id, product_ids, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=False,
            error_message=case.expected_error_message,
        )
