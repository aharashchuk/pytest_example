"""OrderDetailsPage — orchestrator for the full order details page."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_30_S
from sales_portal_tests.ui.pages.confirmation_modal import ConfirmationModal
from sales_portal_tests.ui.pages.navbar_component import NavBar
from sales_portal_tests.ui.pages.orders.components.assign_manager_modal import AssignManagerModal
from sales_portal_tests.ui.pages.orders.components.customer_details_component import (
    OrderDetailsCustomerDetails,
)
from sales_portal_tests.ui.pages.orders.components.delivery.comments_tab import CommentsTab
from sales_portal_tests.ui.pages.orders.components.delivery.delivery_tab import DeliveryTab
from sales_portal_tests.ui.pages.orders.components.delivery.order_history_tab import OrderHistoryTab
from sales_portal_tests.ui.pages.orders.components.delivery.schedule_delivery_page import (
    ScheduleDeliveryPage,
)
from sales_portal_tests.ui.pages.orders.components.header_component import OrderDetailsHeader
from sales_portal_tests.ui.pages.orders.components.requested_products_component import (
    OrderDetailsRequestedProducts,
)
from sales_portal_tests.ui.pages.orders.edit_products_modal import EditProductsModal
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class OrderDetailsPage(SalesPortalPage):
    """Order details page orchestrator.

    Splits the page into reusable components: header, customer details,
    requested products, tabs (delivery / history / comments) and modals.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nav_bar = NavBar(page)
        self.header = OrderDetailsHeader(page)
        self.customer_details = OrderDetailsCustomerDetails(page)
        self.requested_products = OrderDetailsRequestedProducts(page)
        self.comments_tab = CommentsTab(page)
        self.delivery_tab = DeliveryTab(page)
        self.order_history_tab = OrderHistoryTab(page)
        self.schedule_delivery_page = ScheduleDeliveryPage(page)
        self.assign_manager_modal = AssignManagerModal(page)
        self.confirmation_modal = ConfirmationModal(page)
        self.process_modal = self.confirmation_modal
        self.cancel_modal = self.confirmation_modal
        self.reopen_modal = self.confirmation_modal
        self.edit_products_modal = EditProductsModal(page)

    # ── stable anchor: any one of several possible FE containers ─────────────

    @property
    def unique_element(self) -> Locator:
        selectors = ", ".join(
            [
                "#order-info-container",
                "#order-details-tabs",
                "#order-details-tabs-section",
                "#order-status-bar-container",
                "#assigned-manager-container",
                "#customer-section",
                "#products-section",
            ]
        )
        return self.page.locator(selectors)

    @property
    def order_info_container(self) -> Locator:
        return self.page.locator("#order-info-container")

    @property
    def tabs_container(self) -> Locator:
        return self.page.locator("#order-details-tabs-section")

    @property
    def process_order_button(self) -> Locator:
        return self.page.locator("#process-order")

    @property
    def cancel_order_button(self) -> Locator:
        return self.page.locator("#cancel-order")

    @property
    def reopen_order_button(self) -> Locator:
        return self.page.locator("#reopen-order")

    @property
    def refresh_order_button(self) -> Locator:
        return self.page.locator("#refresh-order")

    @property
    def status_order_label(self) -> Locator:
        return self.page.locator("div:nth-child(1) > span.text-primary, div:nth-child(1) > span.text-danger")

    @property
    def notification_toast(self) -> Locator:
        return self.page.locator(".toast-body")

    # ── tabs ──────────────────────────────────────────────────────────────────

    @property
    def delivery_tab_button(self) -> Locator:
        return self.page.locator("#delivery-tab")

    @property
    def history_tab_button(self) -> Locator:
        return self.page.locator("#history-tab")

    @property
    def comments_tab_button(self) -> Locator:
        return self.page.locator("#comments-tab")

    # ── navigation ────────────────────────────────────────────────────────────

    @step("OPEN ORDER DETAILS BY ROUTE")
    def open_by_route(self, route: str) -> None:
        self.open(route)

    @step("OPEN ORDER DETAILS BY ID")
    def open_by_order_id(self, order_id: str) -> None:
        self.open(f"#/orders/{order_id}")
        self.wait_for_spinners()

    @step("WAIT FOR ORDER DETAILS PAGE TO OPEN")
    def wait_for_opened(self) -> None:
        expect(self.unique_element.first).to_be_visible(timeout=TIMEOUT_30_S)
        self.wait_for_spinners()

    # ── tabs switching ────────────────────────────────────────────────────────

    @step("SWITCH TO DELIVERY TAB")
    def open_delivery_tab(self) -> None:
        self.delivery_tab_button.click()

    @step("SWITCH TO HISTORY TAB")
    def open_history_tab(self) -> None:
        self.history_tab_button.click()

    @step("SWITCH TO COMMENTS TAB")
    def open_comments_tab(self) -> None:
        self.comments_tab_button.click()

    # ── order actions ─────────────────────────────────────────────────────────

    @step("CLICK PROCESS ORDER BUTTON")
    def click_process(self) -> None:
        self.process_order_button.click()
        self.process_modal.wait_for_opened()

    @step("CLICK CANCEL ORDER BUTTON")
    def click_cancel(self) -> None:
        self.cancel_order_button.click()
        self.cancel_modal.wait_for_opened()

    @step("CLICK REOPEN ORDER BUTTON")
    def click_reopen(self) -> None:
        self.reopen_order_button.click()
        self.reopen_modal.wait_for_opened()

    @step("CLICK REFRESH ORDER BUTTON")
    def click_refresh_order(self) -> None:
        self.refresh_order_button.click()
        self.wait_for_spinners()
