"""UI tests — Receive all products on an order in Processing status."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestReceiveProducts:
    """UI tests for receiving all products on an order."""

    @allure.title("Receive all products via Select All checkbox")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_receive_all_via_select_all(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order in Processing with 3 products; select all and save receiving."""
        order = orders_service.create_order_in_process(admin_token, num_products=3)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

        order_details_page.requested_products.select_all()
        order_details_page.requested_products.save_receiving()
        order_details_page.wait_for_spinners()

        order_details_page.header.expect_status(OrderStatus.RECEIVED)

        for product in order.products:
            assert order_details_page.requested_products.is_product_received(product.id, product.name)

        assert not order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Receive all products manually one by one")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_receive_all_manually(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Toggle each product checkbox individually and save; order becomes Received."""
        order = orders_service.create_order_in_process(admin_token, num_products=3)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

        for product in order.products:
            order_details_page.requested_products.toggle_product_by_id(product.id)

        order_details_page.requested_products.save_receiving()
        order_details_page.wait_for_spinners()

        order_details_page.header.expect_status(OrderStatus.RECEIVED)

        for product in order.products:
            assert order_details_page.requested_products.is_product_received(product.id, product.name)

        assert not order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Fully received order hides start-receiving controls")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_received_order_hides_receiving_controls(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a fully received order via API; verify all products marked and no receiving button."""
        order = orders_service.create_received_order(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.header.expect_status(OrderStatus.RECEIVED)

        for product in order.products:
            assert order_details_page.requested_products.is_product_received(product.id, product.name)

        assert not order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Cancel receiving — receiving controls disappear, no status change")  # type: ignore[misc]
    @pytest.mark.regression
    def test_cancel_receiving(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Click start-receiving, then cancel; status remains Processing."""
        order = orders_service.create_order_in_process(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

        order_details_page.requested_products.cancel_receiving()

        order_details_page.header.expect_status(OrderStatus.PROCESSING)
        assert order_details_page.requested_products.is_start_receiving_visible()
