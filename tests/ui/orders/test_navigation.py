"""UI tests — Navigation between pages via navbar and home page."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage
from sales_portal_tests.ui.service.home_ui_service import HomeUIService


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestNavigation:
    """Tests for navigation to/from the orders pages."""

    @allure.title("Open Orders List from Home Page")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_open_orders_list_from_home(
        self,
        home_ui_service: HomeUIService,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Click Orders on home page; orders list opens and navbar Orders tab is active."""
        home_ui_service.open()
        home_ui_service.home_page.wait_for_opened()
        home_ui_service.navigate_to("Orders")
        home_ui_service.orders_list_page.wait_for_opened()
        expect(orders_list_page.nav_bar.orders_button).to_contain_class("active")

    @allure.title("Open Orders List on direct URL")  # type: ignore[misc]
    @pytest.mark.regression
    def test_open_orders_list_direct_url(
        self,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Navigate directly to #/orders; orders list opens and navbar active."""
        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()
        expect(orders_list_page.nav_bar.orders_button).to_contain_class("active")

    @allure.title("Open Order Details from Orders List by clicking Details button")  # type: ignore[misc]
    @pytest.mark.regression
    def test_open_order_details_from_list(
        self,
        orders_service: OrdersApiService,
        orders_list_page: OrdersListPage,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create order; open details via the Details button from the orders list."""
        order = orders_service.create_order_in_status(admin_token, 1, OrderStatus.PROCESSING)
        cleanup.orders.add(order.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()
        orders_list_page.click_action(order.id, "details")
        order_details_page.wait_for_opened()

        opened_id = order_details_page.header.get_order_number_text()
        assert opened_id == order.id
        expect(order_details_page.nav_bar.orders_button).to_contain_class("active")

    @allure.title("Open Order Details on direct URL")  # type: ignore[misc]
    @pytest.mark.regression
    def test_open_order_details_direct_url(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Navigate directly to order details URL; correct order ID displayed."""
        order = orders_service.create_order_in_status(admin_token, 1, OrderStatus.PROCESSING)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        opened_id = order_details_page.header.get_order_number_text()
        assert opened_id == order.id
        expect(order_details_page.nav_bar.orders_button).to_contain_class("active")

    @allure.title("Open Orders List from NavBar")  # type: ignore[misc]
    @pytest.mark.regression
    def test_open_orders_list_from_navbar(
        self,
        home_ui_service: HomeUIService,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Start on home page; click Orders in navbar; orders list opens."""
        home_ui_service.open()
        home_ui_service.home_page.wait_for_opened()
        orders_list_page.nav_bar.click_on_nav_button("Orders")
        orders_list_page.wait_for_opened()
        expect(orders_list_page.nav_bar.orders_button).to_contain_class("active")
