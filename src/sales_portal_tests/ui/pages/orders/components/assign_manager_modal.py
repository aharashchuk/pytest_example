"""AssignManagerModal — modal to assign or change the manager for an order."""

from __future__ import annotations

from playwright.sync_api import Locator, expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S, TIMEOUT_15_S
from sales_portal_tests.ui.pages.base_modal import BaseModal
from sales_portal_tests.utils.report.allure_step import step


class AssignManagerModal(BaseModal):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#assign-manager-modal")

    @property
    def title(self) -> Locator:
        return self.unique_element.locator("h5")

    @property
    def manager_search_input(self) -> Locator:
        return self.unique_element.locator("#manager-search-input")

    @property
    def manager_list(self) -> Locator:
        return self.unique_element.locator("#manager-list")

    @property
    def manager_items(self) -> Locator:
        return self.manager_list.locator("li.list-group-item")

    @property
    def save_button(self) -> Locator:
        return self.unique_element.locator("#update-manager-btn")

    @property
    def close_button(self) -> Locator:
        return self.unique_element.locator("button.btn-close")

    @property
    def cancel_button(self) -> Locator:
        return self.unique_element.locator("#cancel-edit-manager-modal-btn")

    def wait_for_opened(self) -> None:
        expect(self.unique_element).to_be_visible(timeout=TIMEOUT_15_S)
        expect(self.manager_list).to_be_visible(timeout=TIMEOUT_10_S)

    @step("SEARCH MANAGER BY NAME")
    def search_manager(self, manager_name: str) -> None:
        expect(self.manager_search_input).to_be_visible(timeout=TIMEOUT_10_S)
        self.manager_search_input.fill(manager_name)
        self.page.wait_for_timeout(300)

    @step("SELECT MANAGER")
    def select_manager(self, manager_name: str) -> None:
        for item in self.manager_items.all():
            text = item.inner_text()
            if manager_name.lower() in text.lower():
                item.click()
                return

    @step("GET ALL AVAILABLE MANAGERS")
    def get_available_managers(self) -> list[str]:
        self.manager_search_input.clear()
        self.page.wait_for_timeout(300)
        managers: list[str] = []
        for item in self.manager_items.all():
            text = item.inner_text().strip()
            if text:
                managers.append(text)
        return managers

    @step("CLICK SAVE BUTTON ON ASSIGN MANAGER MODAL")
    def click_save(self) -> None:
        self.save_button.click()

    @step("CLICK CANCEL BUTTON ON ASSIGN MANAGER MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("CLICK CLOSE BUTTON ON ASSIGN MANAGER MODAL")
    def click_close(self) -> None:
        self.close_button.click()

    def is_save_enabled(self) -> bool:
        return not self.save_button.is_disabled()
