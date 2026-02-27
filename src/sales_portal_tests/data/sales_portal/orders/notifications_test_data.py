"""DDT cases for order notification tests (status-change triggers notification)."""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.status_codes import StatusCodes


@dataclass
class NotificationOnStatusChangeCase:
    to: OrderStatus
    expected_status: StatusCodes
    expected_error_message: str | None
    is_success: bool = True
    # Substring to look for in the notification message.
    # When None the test falls back to checking case.to.value in the message.
    expected_message_contains: str | None = field(default=None)


NOTIFICATION_ON_STATUS_CHANGE_CASES = [
    pytest.param(
        NotificationOnStatusChangeCase(
            to=OrderStatus.PROCESSING,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="status-to-processing",
    ),
    pytest.param(
        NotificationOnStatusChangeCase(
            to=OrderStatus.CANCELED,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="status-to-canceled",
    ),
    pytest.param(
        NotificationOnStatusChangeCase(
            to=OrderStatus.PARTIALLY_RECEIVED,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
            # The API does not emit "Partially Received" in the notification text;
            # it emits a "Products have been marked as delivered" message instead.
            expected_message_contains="Products have been marked as delivered",
        ),
        id="status-to-partially-received",
    ),
    pytest.param(
        NotificationOnStatusChangeCase(
            to=OrderStatus.RECEIVED,
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="status-to-received",
    ),
]
