"""OrderDetailsUIService — high-level order-details flows."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.utils.report.allure_step import step


class OrderDetailsUIService:
    """High-level flows for the order details page.

    Wraps :class:`OrderDetailsPage` to provide single-call helpers that
    combine navigation, tab switching and assertions.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.order_details_page = OrderDetailsPage(page)

    @step("OPEN ORDER DETAILS BY ID")
    def open_order_by_id(self, order_id: str) -> None:
        """Navigate to the order details page for *order_id*.

        Args:
            order_id: MongoDB ``_id`` of the order to open.
        """
        self.order_details_page.open_by_order_id(order_id)
        self.order_details_page.wait_for_opened()

    @step("NAVIGATE TO DELIVERY TAB")
    def open_order_delivery(self, order_id: str) -> None:
        """Open the order details page for *order_id* and switch to the delivery tab.

        Args:
            order_id: MongoDB ``_id`` of the order.
        """
        self.order_details_page.open_by_order_id(order_id)
        self.order_details_page.wait_for_opened()
        self.order_details_page.open_delivery_tab()
        self.order_details_page.delivery_tab.wait_for_opened()
        expect(self.order_details_page.delivery_tab.title).to_have_text("Delivery Information")

    @step("NAVIGATE TO SCHEDULE DELIVERY FORM")
    def open_schedule_delivery_form(self) -> None:
        """Click the schedule-delivery button and wait for the form page.

        Call :meth:`open_order_delivery` first to ensure the delivery tab is open.
        """
        self.order_details_page.delivery_tab.click_delivery_form()
        self.order_details_page.schedule_delivery_page.wait_for_opened()
        self.order_details_page.schedule_delivery_page.wait_for_spinners()

    @step("SAVE DELIVERY AND RETURN TO DELIVERY TAB")
    def save_delivery(self) -> None:
        """Click save on the schedule-delivery form and wait for the delivery tab."""
        self.order_details_page.schedule_delivery_page.click_save()
        self.order_details_page.delivery_tab.wait_for_opened()

    @step("NAVIGATE TO ORDER HISTORY TAB")
    def open_order_history(self, order_id: str) -> None:
        """Open the order details page for *order_id* and switch to the history tab.

        Args:
            order_id: MongoDB ``_id`` of the order.
        """
        self.order_details_page.open_by_order_id(order_id)
        self.order_details_page.wait_for_opened()
        self.order_details_page.open_history_tab()
        self.order_details_page.order_history_tab.wait_for_opened()

    @step("UPDATE ORDER STATUS: PROCESS")
    def process_order(self) -> None:
        """Click the Process button and confirm the modal."""
        self.order_details_page.click_process()
        self.order_details_page.process_modal.click_confirm()
        self.order_details_page.process_modal.wait_for_closed()
        self.order_details_page.wait_for_spinners()

    @step("UPDATE ORDER STATUS: CANCEL")
    def cancel_order(self) -> None:
        """Click the Cancel button and confirm the modal."""
        self.order_details_page.click_cancel()
        self.order_details_page.cancel_modal.click_confirm()
        self.order_details_page.cancel_modal.wait_for_closed()
        self.order_details_page.wait_for_spinners()

    @step("UPDATE ORDER STATUS: REOPEN")
    def reopen_order(self) -> None:
        """Click the Reopen button and confirm the modal."""
        self.order_details_page.click_reopen()
        self.order_details_page.reopen_modal.click_confirm()
        self.order_details_page.reopen_modal.wait_for_closed()
        self.order_details_page.wait_for_spinners()

    @step("VERIFY ORDER STATUS")
    def verify_order_status(self, expected_status: str) -> None:
        """Assert the order status label matches *expected_status*.

        Args:
            expected_status: The status string visible in the header status bar.
        """
        expect(self.order_details_page.header.status_text.first).to_have_text(expected_status, timeout=TIMEOUT_10_S)
