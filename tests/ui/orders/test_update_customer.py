"""UI tests — Update customer on an order."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.ui.service.order_details_ui_service import OrderDetailsUIService

# ---------------------------------------------------------------------------
# DDT: statuses where the edit-customer button should NOT be visible
# ---------------------------------------------------------------------------
ORDER_IN_STATUS_CASES = [
    pytest.param(("create_order_in_process", 1), id="in-process"),
    pytest.param(("create_partially_received_order", 2), id="partially-received"),
    pytest.param(("create_received_order", 1), id="received"),
    pytest.param(("create_canceled_order", 1), id="canceled"),
]


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestUpdateCustomer:
    """UI tests for updating the customer assigned to an order."""

    @allure.title("Edit customer button is visible in Draft order")  # type: ignore[misc]
    @pytest.mark.regression
    def test_edit_customer_button_visible_in_draft(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        order_details_ui_service: OrderDetailsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Customer section and edit button are visible for a Draft order."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_ui_service.open_order_by_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.customer_details.unique_element).to_be_visible()
        expect(order_details_page.customer_details.edit_button).to_be_visible()

    @allure.title("Update customer in Draft order via Edit Customer modal")  # type: ignore[misc]
    @pytest.mark.regression
    def test_update_customer_in_draft_order(
        self,
        orders_service: OrdersApiService,
        customers_service: CustomersApiService,
        order_details_page: OrderDetailsPage,
        order_details_ui_service: OrderDetailsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Selecting a different customer in the modal updates the customer details section."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        second_customer = customers_service.create(admin_token)
        cleanup.customers.add(second_customer.id)

        order_details_ui_service.open_order_by_id(order.id)
        order_details_page.wait_for_opened()

        edit_modal = order_details_page.customer_details.click_edit()
        edit_modal.wait_for_opened()
        edit_modal.select_customer(second_customer.name)
        edit_modal.click_save()
        order_details_page.wait_for_opened()

        updated_data = order_details_page.customer_details.get_customer_data()

        assert updated_data["email"] == second_customer.email
        assert updated_data["name"] == second_customer.name
        assert updated_data["country"] == second_customer.country
        assert updated_data["city"] == second_customer.city
        assert updated_data["street"] == second_customer.street
        assert updated_data["house"] == second_customer.house
        assert updated_data["flat"] == second_customer.flat
        assert updated_data["phone"] == second_customer.phone

    @allure.title("Edit customer button is NOT visible in non-Draft orders")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", ORDER_IN_STATUS_CASES)
    def test_edit_button_not_visible_by_status(
        self,
        case: tuple[str, int],
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        order_details_ui_service: OrderDetailsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Edit customer button must not be visible for non-Draft order statuses."""
        factory_name, num_products = case
        order = getattr(orders_service, factory_name)(admin_token, num_products=num_products)
        cleanup.orders.add(order.id)

        order_details_ui_service.open_order_by_id(order.id)
        order_details_page.wait_for_opened()

        expect(order_details_page.customer_details.unique_element).to_be_visible()
        expect(order_details_page.customer_details.edit_button).not_to_be_visible()
