"""CustomerDetailsModal — read-only customer details dialog."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.data.sales_portal.country import Country
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class CustomerDetailsModal(SalesPortalPage):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#CustomerDetailsModal")

    @property
    def title(self) -> Locator:
        return self.unique_element.locator("h5")

    @property
    def close_button(self) -> Locator:
        return self.unique_element.locator("button.btn-close")

    @property
    def edit_button(self) -> Locator:
        return self.unique_element.locator("button.btn-primary")

    @property
    def cancel_button(self) -> Locator:
        return self.unique_element.locator("button.btn-secondary")

    @property
    def product_value(self) -> Locator:
        return self.unique_element.locator("p")

    @step("CLOSE CUSTOMER DETAILS MODAL")
    def click_close(self) -> None:
        self.close_button.click()

    @step("CANCEL CUSTOMER DETAILS MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("EDIT CUSTOMER DETAILS MODAL")
    def click_edit(self) -> None:
        self.edit_button.click()

    @step("GET CUSTOMER DETAILS")
    def get_data(self) -> dict[str, object]:
        email, name, country, city, street, house, flat, phone, created_on, notes = self.product_value.all_inner_texts()
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
            "notes": "" if notes == "-" else notes,
        }
