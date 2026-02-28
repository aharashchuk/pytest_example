"""OrderDetailsHeader — status bar, action buttons and manager section."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S, TIMEOUT_15_S, TIMEOUT_30_S
from sales_portal_tests.ui.pages.base_page import BasePage
from sales_portal_tests.utils.report.allure_step import step


class OrderDetailsHeader(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#order-info-container")

    @property
    def assigned_manager_container(self) -> Locator:
        return self.page.locator("#assigned-manager-container")

    @property
    def status_bar_container(self) -> Locator:
        return self.page.locator("#order-status-bar-container")

    @property
    def order_number_container(self) -> Locator:
        return self.page.locator("//div[./span[contains(text(), 'Order number')]]")

    @property
    def order_number_text(self) -> Locator:
        return self.order_number_container.locator("//span[@class='fst-italic']")

    @property
    def cancel_button(self) -> Locator:
        return self.page.locator("#cancel-order")

    @property
    def reopen_button(self) -> Locator:
        return self.page.locator("#reopen-order")

    @property
    def process_button(self) -> Locator:
        return self.page.locator("#process-order")

    @property
    def refresh_button(self) -> Locator:
        return self.page.locator("#refresh-order")

    @property
    def assign_or_edit_manager(self) -> Locator:
        return self.assigned_manager_container.locator('[onclick^="renderAssigneManagerModal"]')

    @property
    def unassign_manager(self) -> Locator:
        return self.assigned_manager_container.locator('[onclick^="renderRemoveAssignedManagerModal"]')

    @property
    def assign_manager_trigger(self) -> Locator:
        return self.assigned_manager_container.locator('[onclick^="renderAssigneManagerModal"], a[href], button').first

    @property
    def status_text(self) -> Locator:
        return self.status_bar_container.locator(
            ".status-text, span.text-primary, span.text-danger, span.text-warning, span.text-success"
        )

    @step("HEADER: GET ORDER STATUS TEXT")
    def get_status_text(self) -> str:
        return str(self.status_text.first.inner_text()).strip()

    @step("HEADER: GET ORDER NUMBER TEXT")
    def get_order_number_text(self) -> str:
        return str(self.order_number_text.inner_text()).strip()

    @step("HEADER: EXPECT ORDER STATUS")
    def expect_status(self, status: str) -> None:
        expect(self.status_text.first).to_have_text(status, timeout=TIMEOUT_10_S)

    @step("HEADER: CLICK CANCEL ORDER")
    def cancel_order(self) -> None:
        self.cancel_button.click()

    @step("HEADER: CLICK REFRESH ORDER")
    def refresh(self) -> None:
        self.refresh_button.click()

    @step("HEADER: CLICK PROCESS ORDER")
    def process_order(self) -> None:
        self.process_button.click()
        confirmation_modal = self.page.locator(
            '[name="confirmation-modal"].modal.show, [name="confirmation-modal"].modal.fade.show'
        )
        expect(confirmation_modal.first).to_be_visible(timeout=TIMEOUT_10_S)
        confirm_btn = confirmation_modal.locator(
            ".modal-footer button.btn-primary, .modal-footer button.btn-danger, .modal-footer button.btn-success"
        ).first
        confirm_btn.click()
        expect(self.page.locator(".spinner-border")).to_have_count(0, timeout=TIMEOUT_30_S)
        expect(self.process_button).to_be_hidden(timeout=TIMEOUT_30_S)
        expect(self.unique_element).to_be_visible(timeout=TIMEOUT_15_S)

    @step("HEADER: OPEN ASSIGN MANAGER MODAL")
    def open_assign_manager_modal(self) -> None:
        expect(self.assigned_manager_container).to_be_visible(timeout=TIMEOUT_10_S)
        self.assign_manager_trigger.click()

    @step("HEADER: OPEN UNASSIGN MANAGER MODAL")
    def open_unassign_manager_modal(self) -> None:
        self.unassign_manager.first.click()

    @step("HEADER: EXPECT STATUS TO BE VISIBLE")
    def expect_status_visible(self) -> None:
        expect(self.status_bar_container).to_be_visible()

    def is_cancel_visible(self) -> bool:
        return bool(self.cancel_button.is_visible())

    def is_reopen_visible(self) -> bool:
        return bool(self.reopen_button.is_visible())

    def is_process_visible(self) -> bool:
        return bool(self.process_button.is_visible())

    def is_refresh_visible(self) -> bool:
        return bool(self.refresh_button.is_visible())
