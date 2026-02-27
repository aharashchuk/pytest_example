"""API tests — PUT /api/orders/:id (Update Order)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.order import OrderUpdateBody
from sales_portal_tests.data.sales_portal.orders.update_order_test_data import (
    UPDATE_ORDER_ERROR_CASES,
    UpdateOrderCase,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestUpdateOrder:
    """Tests for PUT /api/orders/:id."""

    # ------------------------------------------------------------------
    # Positive — update customer and products
    # ------------------------------------------------------------------

    @allure.title("Update order — change customer and products")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_update_order_customer_and_products(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order, then update its customer and products; verify the response."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        new_customer = customers_service.create(admin_token)
        cleanup.customers.add(new_customer.id)
        new_product = products_service.create(admin_token)
        cleanup.products.add(new_product.id)

        payload = OrderUpdateBody(customer=new_customer.id, products=[new_product.id])
        response = orders_api.update(admin_token, order.id, payload)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        updated = body["Order"]
        assert updated["customer"]["_id"] == new_customer.id
        assert any(p["_id"] == new_product.id for p in updated["products"])

    @allure.title("Update order — change products only")  # type: ignore[misc]
    @pytest.mark.regression
    def test_update_order_products_only(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Update only the products list of an existing order."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        new_product = products_service.create(admin_token)
        cleanup.products.add(new_product.id)

        payload = OrderUpdateBody(customer=order.customer.id, products=[new_product.id])
        response = orders_api.update(admin_token, order.id, payload)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        updated = body["Order"]
        assert any(p["_id"] == new_product.id for p in updated["products"])

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT update order — error case: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", UPDATE_ORDER_ERROR_CASES)
    def test_update_order_negative(
        self,
        case: UpdateOrderCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to update with invalid data; expect the specified error response."""
        # Always create a base order to work with (unless testing invalid order-id with no need for a real order)
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        # Determine which token / order_id / customer_id / products to send
        token = "" if case.expected_status == StatusCodes.UNAUTHORIZED else admin_token
        order_id = case.order_id if case.order_id is not None else order.id

        # Build products list
        if case.should_have_products:
            if case.invalid_product_id is not None:
                product_ids: list[str] = [case.invalid_product_id]
            else:
                product = products_service.create(admin_token)
                cleanup.products.add(product.id)
                product_ids = [product.id]
        else:
            product_ids = []

        # Determine customer
        customer_id = case.customer_id if case.customer_id is not None else order.customer.id

        payload = OrderUpdateBody(customer=customer_id, products=product_ids)
        response = orders_api.update(token, order_id, payload)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
