"""UI tests — Order status transitions via UI (Process / Cancel / Reopen)."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestProcessing:
    """UI tests for order status transitions via the order details page."""

    @allure.title("Processing order shows receiving controls")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_processing_order_shows_receiving_controls(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order in Processing via API; verify receiving controls visible on UI."""
        order = orders_service.create_order_in_process(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.requested_products.expect_loaded()
        order_details_page.header.expect_status(OrderStatus.PROCESSING)
        assert order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Draft order shows edit controls only")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_draft_order_shows_edit_controls(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a Draft order; verify Cancel visible, Process hidden, no receiving controls."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.requested_products.expect_loaded()
        order_details_page.header.expect_status(OrderStatus.DRAFT)

        expect(order_details_page.cancel_order_button).to_be_visible()
        expect(order_details_page.process_order_button).not_to_be_visible()
        assert not order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("In Process order hides process button, shows receiving")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_in_process_hides_process_button(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Order in Processing: Process button hidden, Cancel and receiving visible."""
        order = orders_service.create_order_in_process(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.header.expect_status(OrderStatus.PROCESSING)

        expect(order_details_page.process_order_button).not_to_be_visible()
        expect(order_details_page.cancel_order_button).to_be_visible()

        order_details_page.requested_products.expect_loaded()
        assert order_details_page.requested_products.is_start_receiving_visible()
