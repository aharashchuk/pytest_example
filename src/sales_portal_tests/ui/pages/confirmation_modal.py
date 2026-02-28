"""ConfirmationModal — generic confirmation dialog (title, message, confirm/cancel)."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.ui.pages.base_modal import BaseModal
from sales_portal_tests.utils.report.allure_step import step


class ConfirmationModal(BaseModal):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator('[name="confirmation-modal"]')

    @property
    def title(self) -> Locator:
        return self.unique_element.locator("h5")

    @property
    def confirm_button(self) -> Locator:
        return self.unique_element.locator("button[type='submit']")

    @property
    def cancel_button(self) -> Locator:
        return self.unique_element.locator("button.btn-secondary")

    @property
    def close_button(self) -> Locator:
        return self.unique_element.locator("button.btn-close")

    @property
    def confirmation_message(self) -> Locator:
        return self.unique_element.locator("div.modal-body p")

    @step("CLICK CLOSE BUTTON ON CONFIRMATION MODAL")
    def click_close(self) -> None:
        self.close_button.click()

    @step("CLICK CANCEL BUTTON ON CONFIRMATION MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("CLICK CONFIRM BUTTON ON CONFIRMATION MODAL")
    def click_confirm(self) -> None:
        self.confirm_button.click()
