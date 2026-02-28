"""DDT cases for create-order integration tests (mock-based).

These cases exercise the UI behaviour when the backend responses are
intercepted and replaced by controlled mocks — no real HTTP calls are made.

Translated from the TypeScript ``createOrderMockDDT.ts``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_response_data
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.notifications import Notifications
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_response_data
from sales_portal_tests.data.status_codes import StatusCodes

if TYPE_CHECKING:
    from sales_portal_tests.mock.mock import Mock


# ---------------------------------------------------------------------------
# Case dataclasses
# ---------------------------------------------------------------------------


@dataclass
class OpenCreateOrderModalCase:
    """Negative / unauthorized case for opening the create-order modal."""

    title: str
    customers_mock: Callable[[Mock], None]
    products_mock: Callable[[Mock], None]
    notification: str | None = None  # expected toast text (None for auth cases)


@dataclass
class CreateOrderResponseErrorCase:
    """Case for error responses when submitting the create-order form."""

    title: str
    response_mock: Callable[[Mock], None]
    notification: str  # expected toast text


# ---------------------------------------------------------------------------
# open_create_order_modal_negative_cases
# Cases where the modal should NOT open because required data is missing / error
# ---------------------------------------------------------------------------

OPEN_CREATE_ORDER_MODAL_NEGATIVE_CASES = [
    pytest.param(
        OpenCreateOrderModalCase(
            title="Should NOT open create order modal with no customers",
            customers_mock=lambda mock: mock.get_customers_all(
                {"Customers": [], "IsSuccess": True, "ErrorMessage": None}
            ),
            products_mock=lambda mock: mock.get_products_all(
                {
                    "Products": [generate_product_response_data().model_dump(by_alias=False)],
                    "IsSuccess": True,
                    "ErrorMessage": None,
                }
            ),
            notification=Notifications.NO_CUSTOMERS_FOUND,
        ),
        id="no-customers",
    ),
    pytest.param(
        OpenCreateOrderModalCase(
            title="Should NOT open create order modal with customers/all 500 error",
            customers_mock=lambda mock: mock.get_customers_all(
                {"IsSuccess": False, "ErrorMessage": None},
                StatusCodes.SERVER_ERROR,
            ),
            products_mock=lambda mock: mock.get_products_all(
                {
                    "Products": [generate_product_response_data().model_dump(by_alias=False)],
                    "IsSuccess": True,
                    "ErrorMessage": None,
                }
            ),
            notification=Notifications.ORDER_UNABLE_TO_CREATE,
        ),
        id="customers-500",
    ),
    pytest.param(
        OpenCreateOrderModalCase(
            title="Should NOT open create order modal with no products",
            customers_mock=lambda mock: mock.get_customers_all(
                {
                    "Customers": [generate_customer_response_data().model_dump(by_alias=False)],
                    "IsSuccess": True,
                    "ErrorMessage": None,
                }
            ),
            products_mock=lambda mock: mock.get_products_all({"Products": [], "IsSuccess": True, "ErrorMessage": None}),
            notification=Notifications.NO_PRODUCTS_FOUND,
        ),
        id="no-products",
    ),
    pytest.param(
        OpenCreateOrderModalCase(
            title="Should NOT open create order modal with products/all 500 error",
            customers_mock=lambda mock: mock.get_customers_all(
                {
                    "Customers": [generate_customer_response_data().model_dump(by_alias=False)],
                    "IsSuccess": True,
                    "ErrorMessage": None,
                }
            ),
            products_mock=lambda mock: mock.get_products_all(
                {"IsSuccess": False, "ErrorMessage": None},
                StatusCodes.SERVER_ERROR,
            ),
            notification=Notifications.ORDER_UNABLE_TO_CREATE,
        ),
        id="products-500",
    ),
]

# ---------------------------------------------------------------------------
# open_create_order_modal_unauthorized_cases
# Cases where the modal should NOT open and the user should be redirected to login
# ---------------------------------------------------------------------------

OPEN_CREATE_ORDER_MODAL_UNAUTHORIZED_CASES = [
    pytest.param(
        OpenCreateOrderModalCase(
            title="Should NOT open create order modal with customers/all 401 error",
            customers_mock=lambda mock: mock.get_customers_all(
                {"IsSuccess": False, "ErrorMessage": ResponseErrors.UNAUTHORIZED},
                StatusCodes.UNAUTHORIZED,
            ),
            products_mock=lambda mock: mock.get_products_all(
                {
                    "Products": [generate_product_response_data().model_dump(by_alias=False)],
                    "IsSuccess": True,
                    "ErrorMessage": None,
                }
            ),
        ),
        id="customers-401",
    ),
    pytest.param(
        OpenCreateOrderModalCase(
            title="Should NOT open create order modal with products/all 401 error",
            customers_mock=lambda mock: mock.get_customers_all(
                {
                    "Customers": [generate_customer_response_data().model_dump(by_alias=False)],
                    "IsSuccess": True,
                    "ErrorMessage": None,
                }
            ),
            products_mock=lambda mock: mock.get_products_all(
                {"IsSuccess": False, "ErrorMessage": ResponseErrors.UNAUTHORIZED},
                StatusCodes.UNAUTHORIZED,
            ),
        ),
        id="products-401",
    ),
]

# ---------------------------------------------------------------------------
# create_order_response_error_cases
# Cases where the modal IS open, the form is submitted, but the server returns an error
# ---------------------------------------------------------------------------

CREATE_ORDER_RESPONSE_ERROR_CASES = [
    pytest.param(
        CreateOrderResponseErrorCase(
            title="Should display message when response status 400",
            response_mock=lambda mock: mock.create_order_modal(
                {"IsSuccess": False, "ErrorMessage": ResponseErrors.BAD_REQUEST},
                StatusCodes.BAD_REQUEST,
            ),
            notification=ResponseErrors.BAD_REQUEST,
        ),
        id="create-order-400",
    ),
    pytest.param(
        CreateOrderResponseErrorCase(
            title="Should display message when response status 404",
            response_mock=lambda mock: mock.create_order_modal(
                {
                    "IsSuccess": False,
                    "ErrorMessage": ResponseErrors.customer_not_found("test3891318231"),
                },
                StatusCodes.NOT_FOUND,
            ),
            notification=Notifications.ORDER_NOT_CREATED,
        ),
        id="create-order-404",
    ),
    pytest.param(
        CreateOrderResponseErrorCase(
            title="Should display message when response status 500",
            response_mock=lambda mock: mock.create_order_modal(
                {"IsSuccess": False, "ErrorMessage": None},
                StatusCodes.SERVER_ERROR,
            ),
            notification=Notifications.ORDER_NOT_CREATED,
        ),
        id="create-order-500",
    ),
]
