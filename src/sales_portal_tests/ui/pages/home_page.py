"""HomePage — welcome text, module navigation buttons, metrics locators."""

from __future__ import annotations

from typing import Literal

from playwright.sync_api import Locator

from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step

HomeModuleButton = Literal["Products", "Customers", "Orders"]


class HomePage(SalesPortalPage):
    @property
    def welcome_text(self) -> Locator:
        return self.page.locator(".welcome-text")

    @property
    def products_button(self) -> Locator:
        return self.page.locator("#products-from-home")

    @property
    def orders_button(self) -> Locator:
        return self.page.locator("#orders-from-home")

    @property
    def customers_button(self) -> Locator:
        return self.page.locator("#customers-from-home")

    @property
    def metrics_container(self) -> Locator:
        return self.page.locator(".row.text-center.mb-5.d-flex.justify-content-between")

    @property
    def orders_this_year_value(self) -> Locator:
        return self.metrics_container.locator("#total-orders-container p.card-text")

    @property
    def total_revenue_value(self) -> Locator:
        return self.metrics_container.locator("#total-revenue-container p.card-text")

    @property
    def new_customers_value(self) -> Locator:
        return self.metrics_container.locator("#total-customers-container p.card-text")

    @property
    def avg_order_value(self) -> Locator:
        return self.metrics_container.locator("#avg-orders-value-container p.card-text")

    @property
    def canceled_orders_value(self) -> Locator:
        return self.metrics_container.locator("#canceled-orders-container p.card-text")

    @property
    def unique_element(self) -> Locator:
        return self.welcome_text

    @step("CLICK ON VIEW MODULE BUTTON ON HOME PAGE")
    def click_on_view_module(self, module: HomeModuleButton) -> None:
        module_buttons: dict[HomeModuleButton, Locator] = {
            "Products": self.products_button,
            "Customers": self.customers_button,
            "Orders": self.orders_button,
        }
        module_buttons[module].click()
