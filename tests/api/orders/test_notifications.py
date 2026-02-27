"""API tests — GET /api/notifications (Notifications after order events)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.notifications_api import NotificationsApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.orders.notifications_test_data import (
    NOTIFICATION_ON_STATUS_CHANGE_CASES,
    NotificationOnStatusChangeCase,
)
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestOrderNotifications:
    """Tests for notifications triggered by order status changes."""

    @allure.title("Got notification on status change to {case.to}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", NOTIFICATION_ON_STATUS_CHANGE_CASES)
    def test_notification_on_order_status_change(
        self,
        case: NotificationOnStatusChangeCase,
        orders_service: OrdersApiService,
        notifications_api: NotificationsApi,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order in the target status and verify a notification was generated."""
        order = orders_service.create_order_in_status(admin_token, num_products=2, status=case.to)
        cleanup.orders.add(order.id)

        response = notifications_api.get_user_notifications(admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        notifications = body.get("Notifications", [])

        # Find notifications for this order by orderId field
        order_notifications = [n for n in notifications if str(n.get("orderId", "")) == order.id]

        assert len(order_notifications) > 0, (
            f"No notification found for order {order.id!r} after transition to {case.to.value!r}. "
            f"All notifications: {[n.get('message', n) for n in notifications[:5]]}"
        )

        # Determine what substring to look for in the notification messages
        expected_substring = case.expected_message_contains or case.to.value

        # At least one notification for this order must contain the expected substring
        messages = [str(n.get("message", "")) for n in order_notifications]
        assert any(expected_substring in msg for msg in messages), (
            f"Expected at least one notification for order {order.id!r} to contain "
            f"{expected_substring!r}. Messages found: {messages}"
        )
