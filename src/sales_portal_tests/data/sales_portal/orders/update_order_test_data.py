"""DDT cases for PUT /api/orders/:id (update order)."""

from __future__ import annotations

import pytest

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes


class UpdateOrderCase(CaseApi):
    order_id: str | None
    invalid_product_id: str | None
    customer_id: str | None
    should_have_products: bool

    def __init__(
        self,
        title: str,
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool = True,
        order_id: str | None = None,
        invalid_product_id: str | None = None,
        customer_id: str | None = None,
        should_have_products: bool = True,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.order_id = order_id
        self.invalid_product_id = invalid_product_id
        self.customer_id = customer_id
        self.should_have_products = should_have_products


UPDATE_ORDER_ERROR_CASES = [
    pytest.param(
        UpdateOrderCase(
            title="404 returned for non-existing order",
            order_id="ffffffffffffffffffffffff",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message="Order with id 'ffffffffffffffffffffffff' wasn't found",
            is_success=False,
            should_have_products=True,
        ),
        id="non-existing-order",
    ),
    pytest.param(
        UpdateOrderCase(
            title="404 returned for non-existing product id",
            invalid_product_id="ffffffffffffffffffffffff",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message="Product with id 'ffffffffffffffffffffffff' wasn't found",
            is_success=False,
            should_have_products=True,
        ),
        id="non-existing-product",
    ),
    pytest.param(
        UpdateOrderCase(
            title="400 returned for empty products array",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
            should_have_products=False,
        ),
        id="empty-products",
    ),
    pytest.param(
        UpdateOrderCase(
            title="401 returned without token",
            expected_status=StatusCodes.UNAUTHORIZED,
            expected_error_message=ResponseErrors.UNAUTHORIZED,
            is_success=False,
            should_have_products=True,
        ),
        id="no-token",
    ),
    pytest.param(
        UpdateOrderCase(
            title="404 returned for non-existing customer",
            customer_id="ffffffffffffffffffffffff",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message="Customer with id 'ffffffffffffffffffffffff' wasn't found",
            is_success=False,
            should_have_products=True,
        ),
        id="non-existing-customer",
    ),
    pytest.param(
        UpdateOrderCase(
            title="500 returned on invalid ObjectId format for order",
            order_id="123",
            expected_status=StatusCodes.SERVER_ERROR,
            expected_error_message=(
                "Argument passed in must be a string of 12 bytes or a string of 24 hex characters or an integer"
            ),
            is_success=False,
            should_have_products=True,
        ),
        id="invalid-order-id-format",
    ),
    pytest.param(
        UpdateOrderCase(
            title="500 returned on invalid ObjectId format for customer",
            customer_id="123",
            expected_status=StatusCodes.SERVER_ERROR,
            expected_error_message=(
                'Cast to ObjectId failed for value "123" (type string) at path "_id" for model "Customer"'
            ),
            is_success=False,
            should_have_products=True,
        ),
        id="invalid-customer-id-format",
    ),
]
