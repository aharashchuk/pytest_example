"""UI tests — Order Details page (header controls, status-based visibility)."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestOrderDetails:
    """Tests for order details page — header buttons and product controls by status."""

    @allure.title("Draft order without delivery: correct header buttons and pencils visible")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_draft_order_no_delivery_buttons(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Draft order (no delivery): Cancel visible; Process and Reopen hidden; edit pencils visible."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.cancel_order_button).to_be_visible()
        expect(order_details_page.process_order_button).not_to_be_visible()
        expect(order_details_page.reopen_order_button).not_to_be_visible()

        expect(order_details_page.customer_details.unique_element).to_be_visible()
        expect(order_details_page.customer_details.edit_button).to_be_visible()

        order_details_page.requested_products.expect_loaded()
        assert order_details_page.requested_products.is_edit_visible()
        assert not order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Draft order with delivery: Process button visible")  # type: ignore[misc]
    @pytest.mark.regression
    def test_draft_order_with_delivery_can_process(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Draft order with delivery: Process button should be available."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.process_order_button).to_be_visible()

    @allure.title("In Process order: receiving controls visible")  # type: ignore[misc]
    @pytest.mark.regression
    def test_in_process_receiving_controls_visible(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """In Process order: start receiving visible; after clicking, receiving controls appear."""
        order = orders_service.create_order_in_process(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.requested_products.expect_loaded()
        assert order_details_page.requested_products.is_start_receiving_visible()

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

    @allure.title("Canceled order: Reopen visible; Cancel and Process hidden")  # type: ignore[misc]
    @pytest.mark.regression
    def test_canceled_order_reopen_visible(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Canceled order: Reopen button visible; Cancel and Process hidden."""
        order = orders_service.create_canceled_order(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.reopen_order_button).to_be_visible()
        expect(order_details_page.cancel_order_button).not_to_be_visible()
        expect(order_details_page.process_order_button).not_to_be_visible()

    @allure.title("Partially Received order: start receiving is available")  # type: ignore[misc]
    @pytest.mark.regression
    def test_partially_received_start_receiving_available(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Partially received order still shows start-receiving button for remaining products."""
        order = orders_service.create_partially_received_order(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.requested_products.expect_loaded()
        assert order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Draft with delivery: Process button triggers receiving flow")  # type: ignore[misc]
    @pytest.mark.regression
    def test_process_via_header_shows_receiving(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """After processing a draft order with delivery, receiving controls become available."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.header.process_order()
        order_details_page.wait_for_spinners()

        order_details_page.requested_products.expect_loaded()
        assert order_details_page.requested_products.is_start_receiving_visible()
