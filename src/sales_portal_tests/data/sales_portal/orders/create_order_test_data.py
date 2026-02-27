"""DDT cases for POST /api/orders and DELETE /api/orders/:id."""

from __future__ import annotations

import pytest

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes


class CreateOrderCase(CaseApi):
    products_count: int
    order_data: dict[str, object] | None

    def __init__(
        self,
        title: str,
        products_count: int,
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool = True,
        order_data: dict[str, object] | None = None,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.products_count = products_count
        self.order_data = order_data


CREATE_ORDER_POSITIVE_CASES = [
    pytest.param(
        CreateOrderCase(
            title="Create order with product quantity = 1 (min)",
            products_count=1,
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="products-1-min",
    ),
    pytest.param(
        CreateOrderCase(
            title="Create order with product quantity = 5 (max)",
            products_count=5,
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="products-5-max",
    ),
]

CREATE_ORDER_NEGATIVE_CASES = [
    pytest.param(
        CreateOrderCase(
            title="Should NOT create order with empty products",
            products_count=1,
            order_data={"products": []},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="empty-products",
    ),
    pytest.param(
        CreateOrderCase(
            title="Should NOT create order without customer",
            products_count=1,
            order_data={"customer": ""},
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.CUSTOMER_MISSING,
            is_success=False,
        ),
        id="no-customer",
    ),
    pytest.param(
        CreateOrderCase(
            title="Should NOT create order with more than 5 products",
            products_count=6,
            order_data={},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="products-6-above-max",
    ),
]

DELETE_ORDER_CASES = [
    pytest.param(
        CreateOrderCase(
            title="Delete order with product quantity = 1 (min)",
            products_count=1,
            expected_status=StatusCodes.DELETED,
            expected_error_message=None,
        ),
        id="delete-products-1",
    ),
    pytest.param(
        CreateOrderCase(
            title="Delete order with product quantity = 5 (max)",
            products_count=5,
            expected_status=StatusCodes.DELETED,
            expected_error_message=None,
        ),
        id="delete-products-5",
    ),
]
