"""AssignManagerUIService — assign, unassign and verify order managers via UI."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.utils.report.allure_step import step


class AssignManagerUIService:
    """High-level flows for manager assignment on the order details page.

    Wraps :class:`OrderDetailsPage`, its
    :attr:`~sales_portal_tests.ui.pages.orders.order_details_page.OrderDetailsPage.header`
    and
    :attr:`~sales_portal_tests.ui.pages.orders.order_details_page.OrderDetailsPage.assign_manager_modal`
    components.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.order_details_page = OrderDetailsPage(page)

    @step("OPEN ORDER FOR MANAGER ASSIGNMENT")
    def open_order_for_manager_assignment(self, order_id: str) -> None:
        """Navigate to the order details page for *order_id*.

        Args:
            order_id: MongoDB ``_id`` of the order.
        """
        self.order_details_page.open_by_order_id(order_id)
        self.order_details_page.wait_for_opened()

    @step("OPEN ASSIGN MANAGER MODAL")
    def open_assign_manager_modal(self) -> None:
        """Click the assign / edit manager trigger and wait for the modal."""
        self.order_details_page.header.assign_or_edit_manager.click()
        self.order_details_page.assign_manager_modal.wait_for_opened()

    @step("ASSIGN MANAGER BY NAME")
    def assign(self, manager_name: str) -> None:
        """Open the assign-manager modal, select *manager_name* and save.

        Args:
            manager_name: Display name (or partial name) of the manager to assign.
        """
        self.open_assign_manager_modal()
        self.order_details_page.assign_manager_modal.select_manager(manager_name)
        expect(self.order_details_page.assign_manager_modal.save_button).to_be_enabled(timeout=TIMEOUT_10_S)
        self.order_details_page.assign_manager_modal.click_save()
        self.order_details_page.assign_manager_modal.wait_for_closed()
        self.order_details_page.wait_for_spinners()

    @step("ASSIGN FIRST AVAILABLE MANAGER")
    def assign_first_available(self) -> str:
        """Assign the first manager from the modal's list and return their name.

        Returns:
            Display name of the manager that was assigned.

        Raises:
            AssertionError: If no managers are available in the modal.
        """
        self.open_assign_manager_modal()
        managers = self.order_details_page.assign_manager_modal.get_available_managers()
        assert managers, "No managers available in the assign-manager modal"
        manager_name = managers[0]
        self.order_details_page.assign_manager_modal.select_manager(manager_name)
        expect(self.order_details_page.assign_manager_modal.save_button).to_be_enabled(timeout=TIMEOUT_10_S)
        self.order_details_page.assign_manager_modal.click_save()
        self.order_details_page.assign_manager_modal.wait_for_closed()
        self.order_details_page.wait_for_spinners()
        return manager_name

    @step("GET AVAILABLE MANAGERS IN MODAL")
    def get_available_managers(self) -> list[str]:
        """Open the modal, collect all manager names, then cancel.

        Returns:
            List of manager display names shown in the modal.
        """
        self.open_assign_manager_modal()
        managers = self.order_details_page.assign_manager_modal.get_available_managers()
        self.order_details_page.assign_manager_modal.click_cancel()
        self.order_details_page.assign_manager_modal.wait_for_closed()
        return managers

    @step("CANCEL MANAGER ASSIGNMENT")
    def cancel_manager_assignment(self) -> None:
        """Open the assign-manager modal and cancel without saving."""
        self.open_assign_manager_modal()
        self.order_details_page.assign_manager_modal.click_cancel()
        self.order_details_page.assign_manager_modal.wait_for_closed()

    @step("UNASSIGN MANAGER")
    def unassign(self) -> None:
        """Click unassign, confirm the modal and wait for the page to settle."""
        self.order_details_page.header.unassign_manager.click()
        confirmation_modal = self.order_details_page.confirmation_modal
        confirmation_modal.wait_for_opened()
        confirmation_modal.click_confirm()
        confirmation_modal.wait_for_closed()
        self.order_details_page.wait_for_spinners()

    @step("VERIFY MANAGER IS ASSIGNED")
    def expect_manager_assigned(self, expected_manager_name: str) -> None:
        """Assert the assigned manager container shows *expected_manager_name*.

        Only the name part before any parenthesised qualifier is matched.

        Args:
            expected_manager_name: Full display name (``"John Doe (admin)"``) or
                bare name (``"John Doe"``).
        """
        display_name = expected_manager_name.split("(")[0].strip()
        expect(self.order_details_page.header.assigned_manager_container).to_contain_text(
            display_name, timeout=TIMEOUT_10_S
        )

    @step("VERIFY NO MANAGER IS ASSIGNED")
    def expect_no_manager_assigned(self) -> None:
        """Assert the assign-manager trigger button is visible (no manager assigned)."""
        expect(self.order_details_page.header.assign_manager_trigger).to_be_visible(timeout=TIMEOUT_10_S)
