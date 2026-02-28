"""Integration tests — Update customer on an order with mocked API responses.

Uses Playwright network interception (via :class:`~sales_portal_tests.mock.mock.Mock`)
to mock ``GET /api/customers/all`` and ``GET /api/orders/:id`` — no real backend
calls are made during the save step.

Covers:
- Edit-customer modal does NOT open when customers/all is empty or errors.
- App redirects to login when a 401 is returned.
- Error toasts shown when the PUT /api/orders/:id fails.
- Modal dropdown lists the mocked customers.
"""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_response_data
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.notifications import Notifications
from sales_portal_tests.data.sales_portal.orders.update_customer_mock_ddt import (
    EDIT_CUSTOMER_IN_ORDER_NEGATIVE_CASES,
    EDIT_ORDER_CUSTOMER_RESPONSE_ERROR_CASES,
    EditCustomerInOrderCase,
    EditOrderCustomerResponseErrorCase,
)
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.mock.mock import Mock
from sales_portal_tests.ui.pages.login.login_page import LoginPage
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.ui.service.order_details_ui_service import OrderDetailsUIService


@allure.suite("Integration")
@allure.sub_suite("Orders")
@pytest.mark.integration
@pytest.mark.ui
@pytest.mark.orders
@pytest.mark.regression
class TestUpdateCustomerIntegration:
    """Integration tests — edit customer modal in an order with mocked backend."""

    # ── Shared order setup (function-scoped) ──────────────────────────────────

    @pytest.fixture(autouse=True)
    def setup_order(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        order_details_ui_service: OrderDetailsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a real Draft order via API, open its details page.

        Stores the order id on the instance for use in individual tests.
        """
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)
        self._order_id = order.id
        order_details_ui_service.open_order_by_id(order.id)
        order_details_page.wait_for_opened()

    # ── Modal should NOT open: negative cases ─────────────────────────────────

    @allure.title("Edit customer modal does not open when: {case.title}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", EDIT_CUSTOMER_IN_ORDER_NEGATIVE_CASES)
    def test_edit_customer_modal_does_not_open(
        self,
        case: EditCustomerInOrderCase,
        mock: Mock,
        order_details_page: OrderDetailsPage,
    ) -> None:
        """Assert the edit-customer modal stays hidden and an error toast is shown.

        Cases: empty customers list, 500 error on customers/all.
        """
        case.customers_mock(mock)

        edit_modal = order_details_page.customer_details.click_edit()

        expect(edit_modal.unique_element).not_to_be_visible()
        expect(order_details_page.toast_message).to_be_visible()
        expect(order_details_page.toast_message).to_have_text(case.notification)

    # ── Auth redirect on 401 ──────────────────────────────────────────────────

    @allure.title("App redirects to login when customers/all returns 401")  # type: ignore[misc]
    def test_edit_customer_modal_redirects_to_login_on_401(
        self,
        mock: Mock,
        order_details_page: OrderDetailsPage,
        login_page: LoginPage,
    ) -> None:
        """Assert the modal does not open and the app logs out on a 401 from customers/all."""
        mock.get_customers_all(
            {"IsSuccess": False, "ErrorMessage": ResponseErrors.UNAUTHORIZED},
            StatusCodes.UNAUTHORIZED,
        )

        edit_modal = order_details_page.customer_details.click_edit()

        expect(edit_modal.unique_element).not_to_be_visible()
        expect(login_page.unique_element).to_be_visible()
        auth_cookie = login_page.get_cookie_by_name("Authorization")
        assert auth_cookie is None, "Expected Authorization cookie to be absent after logout"

    # ── Modal dropdown population ─────────────────────────────────────────────

    @allure.title("Edit customer modal dropdown shows mocked customers")  # type: ignore[misc]
    def test_edit_customer_dropdown_shows_mocked_customers(
        self,
        mock: Mock,
        order_details_page: OrderDetailsPage,
    ) -> None:
        """Assert the customers dropdown in the modal contains the two mocked customers."""
        customer1 = generate_customer_response_data()
        customer2 = generate_customer_response_data()

        mock.get_customers_all(
            {
                "Customers": [
                    customer1.model_dump(by_alias=False),
                    customer2.model_dump(by_alias=False),
                ],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )

        edit_modal = order_details_page.customer_details.click_edit()
        edit_modal.wait_for_opened()

        dropdown_texts = edit_modal.get_customers_dropdown_texts()
        assert customer1.name in dropdown_texts, f"Expected '{customer1.name}' in {dropdown_texts}"
        assert customer2.name in dropdown_texts, f"Expected '{customer2.name}' in {dropdown_texts}"

    @allure.title("Edit customer modal opens with empty dropdown when no customers exist")  # type: ignore[misc]
    def test_edit_customer_modal_opens_with_empty_dropdown(
        self,
        mock: Mock,
        order_details_page: OrderDetailsPage,
    ) -> None:
        """Assert the edit-customer modal opens but its dropdown contains no options.

        When ``GET /api/customers/all`` returns an empty list with 200 OK the
        frontend still creates and shows the modal — it just has no customer
        options to select.
        """
        mock.get_customers_all(
            {
                "Customers": [],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )

        edit_modal = order_details_page.customer_details.click_edit()
        edit_modal.wait_for_opened()

        dropdown_texts = edit_modal.get_customers_dropdown_texts()
        assert dropdown_texts == [], f"Expected empty dropdown, got: {dropdown_texts}"

    # ── Error responses when saving ───────────────────────────────────────────

    @allure.title("Error toast on failed customer update: {case.title}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", EDIT_ORDER_CUSTOMER_RESPONSE_ERROR_CASES)
    def test_edit_customer_shows_error_toast_on_failure(
        self,
        case: EditOrderCustomerResponseErrorCase,
        mock: Mock,
        order_details_page: OrderDetailsPage,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open the edit-customer modal with a real second customer, mock the save, assert toast.

        Flow:
        1. Create a second customer via API.
        2. Open the edit modal (customers/all returns real data).
        3. Select the second customer.
        4. Register mock for the PUT/GET /api/orders/:id to return an error.
        5. Click Save → assert the modal closes and the toast shows the expected message.
        """
        second_customer = customers_service.create(admin_token)
        cleanup.customers.add(second_customer.id)

        edit_modal = order_details_page.customer_details.click_edit()
        edit_modal.wait_for_opened()
        edit_modal.select_customer(second_customer.name)

        case.response_mock(mock, self._order_id)

        edit_modal.click_save()

        expect(edit_modal.unique_element).not_to_be_visible()
        expect(order_details_page.toast_message).to_be_visible()
        expect(order_details_page.toast_message).to_have_text(Notifications.CUSTOMER_FAILED_TO_UPDATE)

    # ── Auth redirect on 401 during save ──────────────────────────────────────

    @allure.title("App logs out when order/:id returns 401 during customer save")  # type: ignore[misc]
    def test_edit_customer_save_redirects_to_login_on_401(
        self,
        mock: Mock,
        order_details_page: OrderDetailsPage,
        login_page: LoginPage,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open edit modal, select a customer, mock 401 on save, assert logout redirect."""
        second_customer = customers_service.create(admin_token)
        cleanup.customers.add(second_customer.id)

        edit_modal = order_details_page.customer_details.click_edit()
        edit_modal.wait_for_opened()
        edit_modal.select_customer(second_customer.name)

        mock.order_by_id(
            {"IsSuccess": False, "ErrorMessage": ResponseErrors.UNAUTHORIZED},
            self._order_id,
            StatusCodes.UNAUTHORIZED,
        )

        edit_modal.click_save()

        expect(edit_modal.unique_element).not_to_be_visible()
        expect(login_page.unique_element).to_be_visible()
        auth_cookie = login_page.get_cookie_by_name("Authorization")
        assert auth_cookie is None, "Expected Authorization cookie to be absent after logout"
