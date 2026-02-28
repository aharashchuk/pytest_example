"""ProductDeleteModal — confirmation dialog for deleting a product."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class ProductDeleteModal(SalesPortalPage):
    @property
    def delete_modal_container(self) -> Locator:
        return self.page.locator(".modal-dialog")

    @property
    def title(self) -> Locator:
        return self.delete_modal_container.locator("h5")

    @property
    def close_btn(self) -> Locator:
        return self.delete_modal_container.locator("button.btn-close")

    @property
    def cancel_btn(self) -> Locator:
        return self.delete_modal_container.locator("button.btn.btn-secondary")

    @property
    def delete_btn(self) -> Locator:
        return self.delete_modal_container.locator("button[type='submit']")

    @property
    def unique_element(self) -> Locator:
        return self.delete_btn

    @step("CLICK CLOSE BUTTON ON PRODUCT DELETE MODAL")
    def click_close(self) -> None:
        self.close_btn.click()

    @step("CLICK DELETE BUTTON ON PRODUCT DELETE MODAL")
    def click_delete(self) -> None:
        self.delete_btn.click()

    @step("CLICK CANCEL BUTTON ON PRODUCT DELETE MODAL")
    def click_cancel(self) -> None:
        self.cancel_btn.click()

    @step("WAIT FOR PRODUCT DELETE MODAL TO OPEN")
    def wait_for_opened(self) -> None:
        self.unique_element.wait_for(state="visible", timeout=TIMEOUT_10_S)

    @step("WAIT FOR PRODUCT DELETE MODAL TO CLOSE")
    def wait_for_closed(self) -> None:
        self.unique_element.wait_for(state="hidden", timeout=TIMEOUT_10_S)
