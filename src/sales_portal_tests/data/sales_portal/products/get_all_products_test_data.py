"""DDT cases for GET /api/products (all products)."""

from __future__ import annotations

import pytest

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

GET_ALL_PRODUCTS_POSITIVE_CASES = [
    pytest.param(
        CaseApi(
            title="Should return list of all products",
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="get-all-products",
    ),
]

GET_ALL_PRODUCTS_NEGATIVE_CASES = [
    pytest.param(
        CaseApi(
            title="401 returned for request without token",
            expected_status=StatusCodes.UNAUTHORIZED,
            expected_error_message=ResponseErrors.UNAUTHORIZED,
            is_success=False,
        ),
        id="no-token-unauthorized",
    ),
]
