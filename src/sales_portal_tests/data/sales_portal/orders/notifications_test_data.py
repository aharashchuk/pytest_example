"""DDT cases for order notification tests (status-change triggers notification)."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.status_codes import StatusCodes


@dataclass
class NotificationOnStatusChangeCase:
    to: OrderStatus
    expected_status: StatusCodes
    expected_error_message: str | None
    is_success: bool = True


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
