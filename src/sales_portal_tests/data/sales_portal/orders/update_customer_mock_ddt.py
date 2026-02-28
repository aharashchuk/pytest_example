"""DDT cases for update-customer integration tests (mock-based).

These cases exercise the UI behaviour when the backend responses are
intercepted and replaced by controlled mocks — no real HTTP calls are made.

Translated from the TypeScript ``updateCustomerDDT.ts``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.notifications import Notifications
from sales_portal_tests.data.status_codes import StatusCodes

if TYPE_CHECKING:
    from sales_portal_tests.mock.mock import Mock


# ---------------------------------------------------------------------------
# Case dataclasses
# ---------------------------------------------------------------------------


@dataclass
class EditCustomerInOrderCase:
    """Negative case for opening the edit-customer modal in an order."""

    title: str
    customers_mock: Callable[[Mock], None]
    notification: str  # expected toast text


@dataclass
class EditOrderCustomerResponseErrorCase:
    """Case for error responses when saving the edit-customer form."""

    title: str
    response_mock: Callable[[Mock, str], None]


# ---------------------------------------------------------------------------
# edit_customer_in_order_negative_cases
# Cases where the modal should NOT open because required data is missing / error
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# edit_customer_in_order_negative_cases
# Cases where the modal should NOT open because customers endpoint errors out
# ---------------------------------------------------------------------------

EDIT_CUSTOMER_IN_ORDER_NEGATIVE_CASES = [
    pytest.param(
        EditCustomerInOrderCase(
            title="Should NOT open edit customer modal with customers/all 500 error",
            customers_mock=lambda mock: mock.get_customers_all(
                {"IsSuccess": False, "ErrorMessage": None},
                StatusCodes.SERVER_ERROR,
            ),
            notification=Notifications.CUSTOMER_UNABLE_TO_UPDATE,
        ),
        id="customers-500",
    ),
]

# ---------------------------------------------------------------------------
# edit_order_customer_response_error_cases
# Cases where the modal IS open and customer is selected but the server
# returns an error when saving
# ---------------------------------------------------------------------------

EDIT_ORDER_CUSTOMER_RESPONSE_ERROR_CASES = [
    pytest.param(
        EditOrderCustomerResponseErrorCase(
            title="Should display message when response status 400",
            response_mock=lambda mock, order_id: mock.order_by_id(
                {"IsSuccess": False, "ErrorMessage": ResponseErrors.BAD_REQUEST},
                order_id,
                StatusCodes.BAD_REQUEST,
            ),
        ),
        id="update-customer-400",
    ),
    pytest.param(
        EditOrderCustomerResponseErrorCase(
            title="Should display message when response status 404",
            response_mock=lambda mock, order_id: mock.order_by_id(
                {
                    "IsSuccess": False,
                    "ErrorMessage": ResponseErrors.customer_not_found("test3891318231"),
                },
                order_id,
                StatusCodes.NOT_FOUND,
            ),
        ),
        id="update-customer-404",
    ),
    pytest.param(
        EditOrderCustomerResponseErrorCase(
            title="Should display message when response status 500",
            response_mock=lambda mock, order_id: mock.order_by_id(
                {"IsSuccess": False, "ErrorMessage": None},
                order_id,
                StatusCodes.SERVER_ERROR,
            ),
        ),
        id="update-customer-500",
    ),
]
