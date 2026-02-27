"""DDT cases for DELETE /api/products/:id."""

from __future__ import annotations

import pytest
from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


DELETE_PRODUCT_POSITIVE_CASES = [
    pytest.param(
        CaseApi(
            title="Delete product",
            expected_status=StatusCodes.DELETED,
            expected_error_message=None,
        ),
        id="delete-product",
    ),
]

_non_existing_id = str(ObjectId())
_invalid_id = _faker.pystr(min_chars=10, max_chars=10)

DELETE_PRODUCT_NEGATIVE_CASES = [
    pytest.param(
        CaseApi(
            title="404 returned for empty id",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.product_not_found(""),
            is_success=False,
        ),
        id="empty-id",
    ),
    pytest.param(
        CaseApi(
            title="404 returned for non-existing id of valid format",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.product_not_found(_non_existing_id),
            is_success=False,
        ),
        id="non-existing-valid-id",
    ),
    pytest.param(
        CaseApi(
            title="400 returned for id of invalid format",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="invalid-id-format",
    ),
]
