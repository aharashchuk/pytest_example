"""AddNewProductPage — form to create a new product."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.data.models.product import Product
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class AddNewProductPage(SalesPortalPage):
    @property
    def title(self) -> Locator:
        return self.page.locator("h2.page-title-text")

    @property
    def name_input(self) -> Locator:
        return self.page.locator("#inputName")

    @property
    def manufacturer_select(self) -> Locator:
        return self.page.locator("#inputManufacturer")

    @property
    def price_input(self) -> Locator:
        return self.page.locator("#inputPrice")

    @property
    def amount_input(self) -> Locator:
        return self.page.locator("#inputAmount")

    @property
    def notes_input(self) -> Locator:
        return self.page.locator("#textareaNotes")

    @property
    def save_button(self) -> Locator:
        return self.page.locator("#save-new-product")

    @property
    def unique_element(self) -> Locator:
        return self.title

    @step("FILL NEW PRODUCT FORM")
    def fill_form(self, product_data: Product) -> None:
        if product_data.name:
            self.name_input.fill(product_data.name)
        if product_data.manufacturer:
            self.manufacturer_select.select_option(product_data.manufacturer)
        if product_data.price:
            self.price_input.fill(str(product_data.price))
        if product_data.amount:
            self.amount_input.fill(str(product_data.amount))
        if product_data.notes:
            self.notes_input.fill(product_data.notes)

    @step("SAVE NEW PRODUCT")
    def click_save(self) -> None:
        self.save_button.click()
