"""NavBar — Home, Products, Customers, Orders navigation buttons."""

from __future__ import annotations

from typing import Literal

from playwright.sync_api import Locator

from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step

NavButtonName = Literal["Home", "Products", "Customers", "Orders"]


class NavBar(SalesPortalPage):
    @property
    def navbar_container(self) -> Locator:
        return self.page.locator(".navbar")

    @property
    def unique_element(self) -> Locator:
        return self.navbar_container

    @property
    def home_button(self) -> Locator:
        return self.navbar_container.locator("[name='home']")

    @property
    def products_button(self) -> Locator:
        return self.navbar_container.locator("[name='products']")

    @property
    def customers_button(self) -> Locator:
        return self.navbar_container.locator("[name='customers']")

    @property
    def orders_button(self) -> Locator:
        return self.navbar_container.locator("[name='orders']")

    @step("NAVBAR: CLICK ON NAVIGATION BUTTON")
    def click_on_nav_button(self, button_name: NavButtonName) -> None:
        buttons: dict[NavButtonName, Locator] = {
            "Home": self.home_button,
            "Products": self.products_button,
            "Customers": self.customers_button,
            "Orders": self.orders_button,
        }
        buttons[button_name].click()
