"""DDT cases for GET /api/customers/:id."""

from __future__ import annotations

import pytest
from bson import ObjectId

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_not_found_id = str(ObjectId())

GET_BY_ID_CUSTOMER_POSITIVE_CASES = [
    pytest.param(
        CaseApi(
            title="Should get customer by valid id",
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="get-by-valid-id",
    ),
]

GET_BY_ID_CUSTOMER_NEGATIVE_CASES = [
    pytest.param(
        CaseApi(
            title="404 returned for non-existing id of valid format",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.customer_not_found(_not_found_id),
            is_success=False,
        ),
        id="non-existing-valid-id",
    ),
]
