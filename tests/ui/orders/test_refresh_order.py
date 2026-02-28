"""UI tests — Refresh order status via the Refresh button."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestRefreshOrder:
    """UI tests verifying the Refresh button reflects backend status changes."""

    @allure.title("Draft → Processing after Refresh")  # type: ignore[misc]
    @pytest.mark.regression
    def test_refresh_draft_to_processing(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open draft order, update status to Processing via API, refresh — new status shown."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.status_order_label).to_have_text(OrderStatus.DRAFT)

        orders_service.update_status(admin_token, order.id, OrderStatus.PROCESSING)

        order_details_page.click_refresh_order()
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.PROCESSING)

    @allure.title("Processing → Received after Refresh")  # type: ignore[misc]
    @pytest.mark.regression
    def test_refresh_processing_to_received(
        self,
        orders_service: OrdersApiService,
        orders_api: OrdersApi,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open processing order, receive all products via API, refresh — status is Received."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.status_order_label).to_have_text(OrderStatus.PROCESSING)

        product_ids = [p.id for p in order.products]
        orders_api.receive_products(order.id, product_ids, admin_token)

        order_details_page.click_refresh_order()
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.RECEIVED)

    @allure.title("Processing → Partially Received after Refresh")  # type: ignore[misc]
    @pytest.mark.regression
    def test_refresh_processing_to_partially_received(
        self,
        orders_service: OrdersApiService,
        orders_api: OrdersApi,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open processing order with 2 products; receive one via API; refresh — Partially Received."""
        order = orders_service.create_order_in_process(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.status_order_label).to_have_text(OrderStatus.PROCESSING)

        orders_api.receive_products(order.id, [order.products[0].id], admin_token)

        order_details_page.click_refresh_order()
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.PARTIALLY_RECEIVED)

    @allure.title("Partially Received → Received after Refresh")  # type: ignore[misc]
    @pytest.mark.regression
    def test_refresh_partially_to_received(
        self,
        orders_service: OrdersApiService,
        orders_api: OrdersApi,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open partially received order; receive remaining via API; refresh — Received."""
        order = orders_service.create_partially_received_order(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.status_order_label).to_have_text(OrderStatus.PARTIALLY_RECEIVED)

        remaining_ids = [p.id for p in order.products if not p.received]
        orders_api.receive_products(order.id, remaining_ids, admin_token)

        order_details_page.click_refresh_order()
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.RECEIVED)

    @allure.title("Draft → Canceled after Refresh")  # type: ignore[misc]
    @pytest.mark.regression
    def test_refresh_draft_to_canceled(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open draft order, cancel via API, refresh — status is Canceled."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.status_order_label).to_have_text(OrderStatus.DRAFT)

        orders_service.update_status(admin_token, order.id, OrderStatus.CANCELED)

        order_details_page.click_refresh_order()
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.CANCELED)
