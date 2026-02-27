"""DDT cases for GET /api/products/:id."""

from __future__ import annotations

import pytest
from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()

_not_found_id = str(ObjectId())
_invalid_id = _faker.pystr(min_chars=10, max_chars=10)

GET_PRODUCT_BY_ID_POSITIVE_CASES = [
    pytest.param(
        CaseApi(
            title="Should get product by valid id",
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="get-by-valid-id",
    ),
]

GET_PRODUCT_BY_ID_NEGATIVE_CASES = [
    pytest.param(
        CaseApi(
            title="404 returned for empty id",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=None,
            is_success=False,
        ),
        id="empty-id",
    ),
    pytest.param(
        CaseApi(
            title="404 returned for non-existing id of valid format",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.product_not_found(_not_found_id),
            is_success=False,
        ),
        id="non-existing-valid-id",
    ),
    pytest.param(
        CaseApi(
            title="500 returned for id of invalid format",
            expected_status=StatusCodes.SERVER_ERROR,
            expected_error_message=None,
            is_success=False,
        ),
        id="invalid-id-format",
    ),
]
