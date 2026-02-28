"""OrderDetailsCustomerDetails — customer details section of the order details page."""

from __future__ import annotations

from playwright.sync_api import Locator, Page

from sales_portal_tests.data.sales_portal.country import Country
from sales_portal_tests.ui.pages.base_page import BasePage
from sales_portal_tests.ui.pages.orders.components.edit_customer_modal import EditOrderCustomerModal
from sales_portal_tests.utils.report.allure_step import step


class OrderDetailsCustomerDetails(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.edit_order_customer_modal = EditOrderCustomerModal(page)

    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#customer-section")

    @property
    def edit_button(self) -> Locator:
        return self.page.locator("#edit-customer-pencil")

    @property
    def details(self) -> Locator:
        return self.unique_element.locator("div.c-details > span:nth-child(2)")

    @step("CUSTOMER: CLICK EDIT")
    def click_edit(self) -> EditOrderCustomerModal:
        self.edit_button.click()
        return self.edit_order_customer_modal

    @step("CUSTOMER: GET DATA")
    def get_customer_data(self) -> dict[str, object]:
        email, name, country, city, street, house, flat, phone, created_on, notes = self.details.all_inner_texts()
        return {
            "email": email,
            "name": name,
            "country": Country(country),
            "city": city,
            "street": street,
            "house": int(house),
            "flat": int(flat),
            "phone": phone,
            "created_on": created_on,
            "notes": notes,
        }

    def is_visible(self) -> bool:
        return bool(self.unique_element.is_visible())

    def is_edit_visible(self) -> bool:
        return bool(self.edit_button.is_visible())
