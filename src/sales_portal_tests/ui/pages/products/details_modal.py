"""ProductDetailsModal — read-only product details dialog."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.data.sales_portal.products.manufacturers import Manufacturers
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class ProductDetailsModal(SalesPortalPage):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#ProductDetailsModal")

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

    @step("CLICK CLOSE BUTTON ON PRODUCT DETAILS MODAL")
    def click_close(self) -> None:
        self.close_button.click()

    @step("CLICK CANCEL BUTTON ON PRODUCT DETAILS MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("CLICK EDIT BUTTON ON PRODUCT DETAILS MODAL")
    def click_edit(self) -> None:
        self.edit_button.click()

    @step("GET PRODUCT DETAILS ON PRODUCT DETAILS MODAL")
    def get_data(self) -> dict[str, object]:
        name, amount, price, manufacturer, created_on, notes = self.product_value.all_inner_texts()
        return {
            "name": name,
            "amount": int(amount),
            "price": int(price),
            "manufacturer": Manufacturers(manufacturer),
            "created_on": created_on,
            "notes": "" if notes == "-" else notes,
        }
