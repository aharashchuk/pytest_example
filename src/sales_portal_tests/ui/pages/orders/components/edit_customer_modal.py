"""EditOrderCustomerModal — modal to update the customer assigned to an order."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.ui.pages.base_modal import BaseModal
from sales_portal_tests.utils.report.allure_step import step


class EditOrderCustomerModal(BaseModal):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#edit-customer-modal")

    @property
    def select_customers_dropdown(self) -> Locator:
        return self.page.locator("#inputCustomerOrder")

    @property
    def save_button(self) -> Locator:
        return self.page.locator("#update-customer-btn")

    @property
    def cancel_button(self) -> Locator:
        return self.page.locator("#cancel-edit-customer-modal-btn")

    @property
    def close_button(self) -> Locator:
        return self.page.locator("button.btn-close")

    @step("SELECT CUSTOMER IN EDIT ORDER CUSTOMER MODAL")
    def select_customer(self, customer_name: str) -> None:
        self.select_customers_dropdown.select_option(customer_name)

    @step("CLICK CANCEL BUTTON IN EDIT ORDER CUSTOMER MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("CLICK SAVE BUTTON IN EDIT ORDER CUSTOMER MODAL")
    def click_save(self) -> None:
        self.save_button.click()

    @step("CLICK CLOSE BUTTON IN EDIT ORDER CUSTOMER MODAL")
    def click_close(self) -> None:
        self.close_button.click()

    @step("GET CUSTOMERS DROPDOWN VALUES IN EDIT ORDER CUSTOMER MODAL")
    def get_customers_dropdown_texts(self) -> list[str]:
        customers_options = self.select_customers_dropdown.locator("option")
        return list(customers_options.all_text_contents())
