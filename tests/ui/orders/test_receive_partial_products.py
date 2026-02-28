"""UI tests — Receive partial products on an order in Processing status."""

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
class TestReceivePartialProducts:
    """UI tests for partially receiving products on a Processing order."""

    @allure.title("Receive one out of multiple products — order becomes Partially Received")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_receive_one_product(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Receive the first product only; order status becomes Partially Received."""
        order = orders_service.create_order_in_process(admin_token, num_products=3)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

        order_details_page.requested_products.toggle_product_by_id(order.products[0].id)
        order_details_page.requested_products.save_receiving()
        order_details_page.wait_for_spinners()

        order_details_page.header.expect_status(OrderStatus.PARTIALLY_RECEIVED)
        assert order_details_page.requested_products.is_product_received(order.products[0].id, order.products[0].name)
        # start receiving should still be visible for remaining products
        assert order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Receive multiple products but not all — stays Partially Received")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_receive_multiple_but_not_all(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Receive first and third products out of 4; status is Partially Received."""
        order = orders_service.create_order_in_process(admin_token, num_products=4)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

        order_details_page.requested_products.toggle_product_by_id(order.products[0].id)
        order_details_page.requested_products.toggle_product_by_id(order.products[2].id)
        order_details_page.requested_products.save_receiving()
        order_details_page.wait_for_spinners()

        order_details_page.header.expect_status(OrderStatus.PARTIALLY_RECEIVED)

        assert order_details_page.requested_products.is_product_received(order.products[0].id, order.products[0].name)
        assert order_details_page.requested_products.is_product_received(order.products[2].id, order.products[2].name)
        assert order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Partially received order allows receiving remaining products")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_partially_received_allows_remaining(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a partially received order; start-receiving still available for remaining items."""
        order = orders_service.create_partially_received_order(admin_token, num_products=3)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.header.expect_status(OrderStatus.PARTIALLY_RECEIVED)
        assert order_details_page.requested_products.is_start_receiving_visible()

    @allure.title("Receive remaining products from Partially Received — order becomes Received")  # type: ignore[misc]
    @pytest.mark.regression
    def test_receive_remaining_from_partial(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """From a partially received order receive the remaining products; status → Received."""
        order = orders_service.create_partially_received_order(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()
        order_details_page.requested_products.expect_loaded()

        order_details_page.header.expect_status(OrderStatus.PARTIALLY_RECEIVED)

        order_details_page.requested_products.start_receiving()
        order_details_page.requested_products.wait_for_receiving_controls()

        # Receive remaining (not-yet-received) products
        for product in order.products:
            if not product.received:
                order_details_page.requested_products.toggle_product_by_id(product.id)

        order_details_page.requested_products.save_receiving()
        order_details_page.wait_for_spinners()

        order_details_page.header.expect_status(OrderStatus.RECEIVED)
