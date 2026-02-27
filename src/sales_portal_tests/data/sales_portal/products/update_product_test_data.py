"""DDT cases for PUT /api/products/:id."""

from __future__ import annotations

import pytest
from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_data
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class UpdateProductCase(CaseApi):
    product_data: dict[str, object]
    product_id: str | None

    def __init__(
        self,
        title: str,
        product_data: dict[str, object],
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool = True,
        product_id: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.product_data = product_data
        self.product_id = product_id


UPDATE_PRODUCT_POSITIVE_CASES = [
    pytest.param(
        UpdateProductCase(
            title="Update name to 3 characters",
            product_data={"name": _faker.pystr(min_chars=3, max_chars=3)},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="name-3-chars",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update name to 40 characters",
            product_data={"name": _faker.pystr(min_chars=40, max_chars=40)},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="name-40-chars",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update price to minimum (1)",
            product_data={"price": 1},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="price-min",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update price to maximum (99999)",
            product_data={"price": 99999},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="price-max",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update amount to minimum (0)",
            product_data={"amount": 0},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="amount-min",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update amount to maximum (999)",
            product_data={"amount": 999},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="amount-max",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update notes to 250 characters",
            product_data={"notes": _faker.pystr(min_chars=250, max_chars=250)},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="notes-250-chars",
    ),
    pytest.param(
        UpdateProductCase(
            title="Clear notes (empty string)",
            product_data={"notes": ""},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="notes-cleared",
    ),
    pytest.param(
        UpdateProductCase(
            title="Update only manufacturer",
            product_data={"manufacturer": generate_product_data().manufacturer},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="manufacturer-only",
    ),
]

UPDATE_PRODUCT_NEGATIVE_CASES = [
    pytest.param(
        UpdateProductCase(
            title="404 for non-existing valid id",
            product_data={"name": "ValidName123"},
            product_id=str(ObjectId()),
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.product_not_found(str(ObjectId())),
            is_success=False,
        ),
        id="non-existing-id",
    ),
    pytest.param(
        UpdateProductCase(
            title="400 for invalid id format",
            product_data={"name": "ValidName123"},
            product_id=_faker.pystr(min_chars=10, max_chars=10),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="invalid-id-format",
    ),
]
