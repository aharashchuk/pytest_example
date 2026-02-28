"""UI tests — Order confirmation modals (Process / Cancel / Reopen)."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.notifications import (
    CANCEL_ORDER_MODAL,
    PROCESS_ORDER_MODAL,
    REOPEN_ORDER_MODAL,
    Notifications,
)
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestOrderModals:
    """UI tests for the Process / Cancel / Reopen confirmation modals."""

    @allure.title("Process order via Process Confirmation modal")  # type: ignore[misc]
    @pytest.mark.regression
    def test_process_order_via_modal(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open process modal; verify title/body/button; confirm; order becomes In Process."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.click_process()
        order_details_page.process_modal.wait_for_opened()

        # Assert modal copy
        expect(order_details_page.process_modal.title).to_have_text(PROCESS_ORDER_MODAL.title)
        expect(order_details_page.process_modal.confirmation_message).to_have_text(PROCESS_ORDER_MODAL.body)
        expect(order_details_page.process_modal.confirm_button).to_have_text(PROCESS_ORDER_MODAL.action_button)

        order_details_page.process_modal.click_confirm()
        expect(order_details_page.toast_message).to_have_text(Notifications.ORDER_PROCESSED)
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.PROCESSING)

    @allure.title("Cancel order via Cancel Confirmation modal")  # type: ignore[misc]
    @pytest.mark.regression
    def test_cancel_order_via_modal(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open cancel modal; verify copy; confirm; order becomes Canceled."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.click_cancel()
        order_details_page.cancel_modal.wait_for_opened()

        expect(order_details_page.cancel_modal.title).to_have_text(CANCEL_ORDER_MODAL.title)
        expect(order_details_page.cancel_modal.confirmation_message).to_have_text(CANCEL_ORDER_MODAL.body)
        expect(order_details_page.cancel_modal.confirm_button).to_have_text(CANCEL_ORDER_MODAL.action_button)

        order_details_page.cancel_modal.click_confirm()
        expect(order_details_page.toast_message).to_have_text(Notifications.ORDER_CANCELED)
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.CANCELED)

    @allure.title("Reopen order via Reopen Confirmation modal")  # type: ignore[misc]
    @pytest.mark.regression
    def test_reopen_order_via_modal(
        self,
        orders_service: OrdersApiService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open reopen modal; verify copy; confirm; order becomes Draft again."""
        order = orders_service.create_canceled_order(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        order_details_page.open_by_order_id(order.id)
        order_details_page.wait_for_opened()

        order_details_page.click_reopen()
        order_details_page.reopen_modal.wait_for_opened()

        expect(order_details_page.reopen_modal.title).to_have_text(REOPEN_ORDER_MODAL.title)
        expect(order_details_page.reopen_modal.confirmation_message).to_have_text(REOPEN_ORDER_MODAL.body)
        expect(order_details_page.reopen_modal.confirm_button).to_have_text(REOPEN_ORDER_MODAL.action_button)

        order_details_page.reopen_modal.click_confirm()
        expect(order_details_page.toast_message).to_have_text(Notifications.ORDER_REOPENED)
        expect(order_details_page.status_order_label).to_have_text(OrderStatus.DRAFT)
