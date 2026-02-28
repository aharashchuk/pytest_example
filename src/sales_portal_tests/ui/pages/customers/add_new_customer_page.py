"""AddNewCustomerPage — form to create a new customer."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.data.models.customer import Customer
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class AddNewCustomerPage(SalesPortalPage):
    @property
    def title(self) -> Locator:
        return self.page.locator("h2.page-title-text")

    @property
    def email(self) -> Locator:
        return self.page.locator("#inputEmail")

    @property
    def name_input(self) -> Locator:
        return self.page.locator("#inputName")

    @property
    def country_select(self) -> Locator:
        return self.page.locator("#inputCountry")

    @property
    def city_input(self) -> Locator:
        return self.page.locator("#inputCity")

    @property
    def street_input(self) -> Locator:
        return self.page.locator("#inputStreet")

    @property
    def house_input(self) -> Locator:
        return self.page.locator("#inputHouse")

    @property
    def flat_input(self) -> Locator:
        return self.page.locator("#inputFlat")

    @property
    def phone_input(self) -> Locator:
        return self.page.locator("#inputPhone")

    @property
    def notes_input(self) -> Locator:
        return self.page.locator("#textareaNotes")

    @property
    def save_button(self) -> Locator:
        return self.page.locator("#save-new-customer")

    @property
    def unique_element(self) -> Locator:
        return self.title

    @step("FILL NEW CUSTOMER FORM")
    def fill_form(self, customer_data: Customer) -> None:
        if customer_data.name:
            self.name_input.fill(customer_data.name)
        if customer_data.email:
            self.email.fill(customer_data.email)
        if customer_data.country:
            self.country_select.select_option(customer_data.country)
        if customer_data.city:
            self.city_input.fill(customer_data.city)
        if customer_data.street:
            self.street_input.fill(customer_data.street)
        if customer_data.house:
            self.house_input.fill(str(customer_data.house))
        if customer_data.flat:
            self.flat_input.fill(str(customer_data.flat))
        if customer_data.phone:
            self.phone_input.fill(str(customer_data.phone))
        if customer_data.notes:
            self.notes_input.fill(customer_data.notes)

    @step("SAVE NEW CUSTOMER")
    def click_save(self) -> None:
        self.save_button.click()
