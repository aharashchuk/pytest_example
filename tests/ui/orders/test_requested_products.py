"""UI tests — Edit requested products on a Draft order."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.notifications import Notifications
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.utils.validation.validate_response import validate_response

MAXIMUM_REQUESTED_PRODUCTS = 5


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestRequestedProducts:
    """UI tests for editing the requested products on a Draft order."""

    @allure.title("Edit requested products: increase products count to 5")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_increase_products_to_max(
        self,
        orders_service: OrdersApiService,
        products_service: ProductsApiService,
        orders_api: OrdersApi,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create order with 1 product; edit to add 4 more; verify 5 products in BE."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        extra_products = []
        for _ in range(MAXIMUM_REQUESTED_PRODUCTS - 1):
            p = products_service.create(admin_token)
            cleanup.products.add(p.id)
            extra_products.append(p)

        initial_name = order.products[0].name
        desired_names = [initial_name] + [p.name for p in extra_products]

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.requested_products.click_edit()
        order_details_page.edit_products_modal.wait_for_opened()
        expect(order_details_page.edit_products_modal.product_rows).to_have_count(1)

        updated = order_details_page.edit_products_modal.edit_order(desired_names)
        assert len(updated.products) == MAXIMUM_REQUESTED_PRODUCTS

        expect(order_details_page.toast_message).to_contain_text(Notifications.ORDER_UPDATED)
        order_details_page.edit_products_modal.wait_for_closed()

        get_response = orders_api.get_by_id(order.id, admin_token)
        validate_response(get_response, status=StatusCodes.OK, is_success=True, schema=GET_ORDER_SCHEMA)

        assert isinstance(get_response.body, dict)
        updated_order = get_response.body["Order"]
        assert isinstance(updated_order, dict)
        assert len(updated_order["products"]) == MAXIMUM_REQUESTED_PRODUCTS

        actual_names = sorted(p["name"] for p in updated_order["products"])
        expected_names = sorted(desired_names)
        assert actual_names == expected_names

    @allure.title("Edit requested products: decrease products count to 1")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_decrease_products_to_one(
        self,
        orders_service: OrdersApiService,
        orders_api: OrdersApi,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create order with 5 products; edit to keep only 1; verify 1 product in BE."""
        order = orders_service.create_order_and_entities(admin_token, num_products=MAXIMUM_REQUESTED_PRODUCTS)
        cleanup.orders.add(order.id)

        keep_name = order.products[0].name

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.requested_products.click_edit()
        order_details_page.edit_products_modal.wait_for_opened()
        expect(order_details_page.edit_products_modal.product_rows).to_have_count(MAXIMUM_REQUESTED_PRODUCTS)

        order_details_page.edit_products_modal.edit_order([keep_name])
        expect(order_details_page.toast_message).to_contain_text(Notifications.ORDER_UPDATED)
        order_details_page.edit_products_modal.wait_for_closed()

        get_response = orders_api.get_by_id(order.id, admin_token)
        validate_response(get_response, status=StatusCodes.OK, is_success=True, schema=GET_ORDER_SCHEMA)

        assert isinstance(get_response.body, dict)
        updated_order = get_response.body["Order"]
        assert isinstance(updated_order, dict)
        assert len(updated_order["products"]) == 1
        assert updated_order["products"][0]["name"] == keep_name
