"""API tests — POST /api/orders (Create Order)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.order import OrderCreateBody
from sales_portal_tests.data.sales_portal.orders.create_order_test_data import (
    CREATE_ORDER_NEGATIVE_CASES,
    CREATE_ORDER_POSITIVE_CASES,
    CreateOrderCase,
)
from sales_portal_tests.data.schemas.orders.schemas import CREATE_ORDER_SCHEMA
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestCreateOrder:
    """Tests for POST /api/orders."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Create order — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_ORDER_POSITIVE_CASES)
    def test_create_order_positive(
        self,
        case: CreateOrderCase,
        orders_api: OrdersApi,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a valid order with the specified number of products and validate the response."""
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        product_ids: list[str] = []
        for _ in range(case.products_count):
            product = products_service.create(admin_token)
            product_ids.append(product.id)
        cleanup.products.update(product_ids)

        payload = OrderCreateBody(customer=customer.id, products=product_ids)
        response = orders_api.create(admin_token, payload)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=CREATE_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        created = body["Order"]
        cleanup.orders.add(created["_id"])

        assert created["customer"]["_id"] == customer.id
        assert len(created["products"]) == case.products_count

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT create order — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_ORDER_NEGATIVE_CASES)
    def test_create_order_negative(
        self,
        case: CreateOrderCase,
        orders_api: OrdersApi,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to create an invalid order; expect an error response."""
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        product_ids: list[str] = []
        for _ in range(case.products_count):
            product = products_service.create(admin_token)
            product_ids.append(product.id)
        cleanup.products.update(product_ids)

        # Use overridden order_data if provided, otherwise build normally
        if case.order_data is not None:
            override = dict(case.order_data)
            # Fill in customer/products from created entities if not explicitly overridden
            payload_customer = str(override.get("customer", customer.id))
            payload_products = override.get("products", product_ids)
            raw_payload = {
                "customer": payload_customer,
                "products": payload_products,
            }
            # Build a custom payload dict — send via the api directly
            from sales_portal_tests.config import api_config
            from sales_portal_tests.data.models.core import RequestOptions

            options = RequestOptions(
                url=api_config.ORDERS,
                method="POST",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {admin_token}",
                },
                data=raw_payload,
            )
            response = orders_api._client.send(options)
        else:
            payload = OrderCreateBody(customer=customer.id, products=product_ids)
            response = orders_api.create(admin_token, payload)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
