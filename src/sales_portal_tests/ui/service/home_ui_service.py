"""HomeUIService — navigation from the home page to each module."""

from __future__ import annotations

from playwright.sync_api import Page

from sales_portal_tests.ui.pages.customers.customers_list_page import CustomersListPage
from sales_portal_tests.ui.pages.home_page import HomeModuleButton, HomePage
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage
from sales_portal_tests.utils.report.allure_step import step


class HomeUIService:
    """High-level flows for the home page and module navigation.

    Composes :class:`HomePage` with the three list-page objects so that
    ``navigate_to()`` can assert the target page opened successfully.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.home_page = HomePage(page)
        self.products_list_page = ProductsListPage(page)
        self.customers_list_page = CustomersListPage(page)
        self.orders_list_page = OrdersListPage(page)

    @step("OPEN HOME PAGE")
    def open(self) -> None:
        """Navigate directly to the home page hash route."""
        self.home_page.open("#/home")
        self.home_page.wait_for_opened()

    @step("NAVIGATE TO MODULE FROM HOME PAGE")
    def navigate_to(self, module: HomeModuleButton) -> None:
        """Click the *module* button on the home page and wait for the target page.

        Args:
            module: One of ``"Products"``, ``"Customers"``, or ``"Orders"``.
        """
        self.home_page.click_on_view_module(module)

        if module == "Products":
            self.products_list_page.wait_for_opened()
        elif module == "Customers":
            self.customers_list_page.wait_for_opened()
        elif module == "Orders":
            self.orders_list_page.wait_for_opened()

    @step("VERIFY HOME PAGE METRICS ARE VISIBLE")
    def verify_metrics(self) -> None:
        """Assert all five metric cards are visible."""
        from playwright.sync_api import expect

        expect(self.home_page.orders_this_year_value).to_be_visible()
        expect(self.home_page.total_revenue_value).to_be_visible()
        expect(self.home_page.new_customers_value).to_be_visible()
        expect(self.home_page.avg_order_value).to_be_visible()
        expect(self.home_page.canceled_orders_value).to_be_visible()
