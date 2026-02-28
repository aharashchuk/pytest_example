"""Integration tests — Create Order modal with mocked API responses.

Uses Playwright network interception (via :class:`~sales_portal_tests.mock.mock.Mock`)
to mock ``GET /api/customers/all``, ``GET /api/products/all``, and
``POST /api/orders`` — no real backend calls are made.

Covers:
- Modal does NOT open when required data is missing or errors occur.
- App redirects to login when a 401 is returned (auth guard).
- Error toasts are shown when the POST fails.
- Modal dropdowns display the mocked customers / products.
"""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_response_data
from sales_portal_tests.data.sales_portal.orders.create_order_mock_ddt import (
    CREATE_ORDER_RESPONSE_ERROR_CASES,
    OPEN_CREATE_ORDER_MODAL_NEGATIVE_CASES,
    OPEN_CREATE_ORDER_MODAL_UNAUTHORIZED_CASES,
    CreateOrderResponseErrorCase,
    OpenCreateOrderModalCase,
)
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_response_data
from sales_portal_tests.mock.mock import Mock
from sales_portal_tests.ui.pages.login.login_page import LoginPage
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage


@allure.suite("Integration")
@allure.sub_suite("Orders")
@pytest.mark.integration
@pytest.mark.ui
@pytest.mark.orders
@pytest.mark.regression
class TestCreateOrderIntegration:
    """Integration tests — Create Order modal with mocked backend responses."""

    # ── Pre-condition: navigate to orders list before each test ───────────────

    @pytest.fixture(autouse=True)
    def open_orders_list(self, orders_list_page: OrdersListPage) -> None:
        """Open the orders list page before each test in this class."""
        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

    # ── Cannot open modal: missing / error data ───────────────────────────────

    @allure.title("Modal does not open when preconditions fail: {case.title}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", OPEN_CREATE_ORDER_MODAL_NEGATIVE_CASES)
    def test_create_order_modal_does_not_open(
        self,
        case: OpenCreateOrderModalCase,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Assert the modal stays hidden and an error toast is shown.

        Cases cover: no customers, no products, 500 errors on both endpoints.
        """
        case.customers_mock(mock)
        case.products_mock(mock)

        create_modal = orders_list_page.click_create_order_button()

        expect(create_modal.unique_element).not_to_be_visible()
        assert case.notification is not None
        expect(orders_list_page.toast_message).to_be_visible()
        expect(orders_list_page.toast_message).to_have_text(case.notification)

    # ── Auth redirect: 401 responses ──────────────────────────────────────────

    @allure.title("App redirects to login on 401: {case.title}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", OPEN_CREATE_ORDER_MODAL_UNAUTHORIZED_CASES)
    def test_create_order_modal_redirects_to_login_on_401(
        self,
        case: OpenCreateOrderModalCase,
        mock: Mock,
        orders_list_page: OrdersListPage,
        login_page: LoginPage,
    ) -> None:
        """Assert the modal does not open and the app redirects to login on 401.

        After redirect the *Authorization* cookie should be absent (logged out).
        """
        case.customers_mock(mock)
        case.products_mock(mock)

        create_modal = orders_list_page.click_create_order_button()

        expect(create_modal.unique_element).not_to_be_visible()
        expect(login_page.unique_element).to_be_visible()
        auth_cookie = login_page.get_cookie_by_name("Authorization")
        assert auth_cookie is None, "Expected Authorization cookie to be absent after logout"

    # ── Error responses when submitting the form ──────────────────────────────

    @allure.title("Error toast on failed order creation: {case.title}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", CREATE_ORDER_RESPONSE_ERROR_CASES)
    def test_create_order_shows_error_toast_on_failure(
        self,
        case: CreateOrderResponseErrorCase,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Submit the create-order form with a mocked error response and assert toast.

        Flow:
        1. Mock customers/all and products/all with valid single entries.
        2. Mock the POST /api/orders endpoint to return the error.
        3. Open the modal, select customer + product, click Create.
        4. Assert the modal closes and the expected toast message is shown.
        """
        customer = generate_customer_response_data()
        product = generate_product_response_data()

        mock.get_customers_all(
            {
                "Customers": [customer.model_dump(by_alias=False)],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )
        mock.get_products_all(
            {
                "Products": [product.model_dump(by_alias=False)],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )
        case.response_mock(mock)

        create_modal = orders_list_page.click_create_order_button()
        create_modal.wait_for_opened()
        create_modal.select_customer(customer.name)
        create_modal.select_product(0, product.name)
        create_modal.click_create()

        expect(create_modal.unique_element).not_to_be_visible()
        expect(orders_list_page.toast_message).to_be_visible()
        expect(orders_list_page.toast_message).to_have_text(case.notification)

    # ── Dropdown population ───────────────────────────────────────────────────

    @allure.title("Create order modal displays mocked customers in dropdown")  # type: ignore[misc]
    def test_customers_dropdown_shows_mocked_data(
        self,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Assert the customers dropdown contains exactly the two mocked customers."""
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
        mock.get_products_all(
            {
                "Products": [generate_product_response_data().model_dump(by_alias=False)],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )

        create_modal = orders_list_page.click_create_order_button()
        create_modal.wait_for_opened()

        dropdown_texts = create_modal.get_customers_dropdown_texts()
        assert customer1.name in dropdown_texts, f"Expected '{customer1.name}' in {dropdown_texts}"
        assert customer2.name in dropdown_texts, f"Expected '{customer2.name}' in {dropdown_texts}"

    @allure.title("Create order modal displays mocked products in dropdown")  # type: ignore[misc]
    def test_products_dropdown_shows_mocked_data(
        self,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Assert the products dropdown contains exactly the two mocked products."""
        product1 = generate_product_response_data()
        product2 = generate_product_response_data()

        mock.get_customers_all(
            {
                "Customers": [generate_customer_response_data().model_dump(by_alias=False)],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )
        mock.get_products_all(
            {
                "Products": [
                    product1.model_dump(by_alias=False),
                    product2.model_dump(by_alias=False),
                ],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )

        create_modal = orders_list_page.click_create_order_button()
        create_modal.wait_for_opened()

        dropdown_texts = create_modal.get_products_dropdown_texts()
        assert product1.name in dropdown_texts, f"Expected '{product1.name}' in {dropdown_texts}"
        assert product2.name in dropdown_texts, f"Expected '{product2.name}' in {dropdown_texts}"

    @allure.title("Create order modal: total price updates when a product is removed")  # type: ignore[misc]
    def test_total_price_updates_on_product_removal(
        self,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Add 2 products to the modal, remove one, assert total price equals remaining product."""
        product1 = generate_product_response_data()
        product2 = generate_product_response_data()
        customer = generate_customer_response_data()

        mock.get_customers_all(
            {
                "Customers": [customer.model_dump(by_alias=False)],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )
        mock.get_products_all(
            {
                "Products": [
                    product1.model_dump(by_alias=False),
                    product2.model_dump(by_alias=False),
                ],
                "IsSuccess": True,
                "ErrorMessage": None,
            }
        )

        create_modal = orders_list_page.click_create_order_button()
        create_modal.wait_for_opened()

        create_modal.select_customer(customer.name)
        create_modal.select_product(0, product1.name)
        create_modal.click_add_product_button()
        create_modal.select_product(1, product2.name)

        create_modal.delete_product(0)

        total_text = create_modal.get_total_price()
        assert str(product2.price) == total_text, f"Expected total price {product2.price}, got {total_text}"
