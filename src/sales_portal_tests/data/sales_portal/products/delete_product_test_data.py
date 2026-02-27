"""DDT cases for DELETE /api/products/:id."""

from __future__ import annotations

import pytest
from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class DeleteProductCase(CaseApi):
    """DDT case for DELETE /api/products/:id that carries the product ID to delete."""

    product_id: str

    def __init__(
        self,
        title: str,
        product_id: str,
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool | None = True,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.product_id = product_id


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

# Exported for use in tests that need to call the API with these IDs directly
NON_EXISTING_PRODUCT_ID: str = _non_existing_id
INVALID_FORMAT_DELETE_PRODUCT_ID: str = _invalid_id
EMPTY_DELETE_PRODUCT_ID: str = ""

DELETE_PRODUCT_NEGATIVE_CASES = [
    pytest.param(
        DeleteProductCase(
            title="404 returned for empty id",
            product_id="",
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=None,
            is_success=None,
        ),
        id="empty-id",
    ),
    pytest.param(
        DeleteProductCase(
            title="404 returned for non-existing id of valid format",
            product_id=_non_existing_id,
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.product_not_found(_non_existing_id),
            is_success=False,
        ),
        id="non-existing-valid-id",
    ),
    pytest.param(
        DeleteProductCase(
            title="500 returned for id of invalid format",
            product_id=_invalid_id,
            expected_status=StatusCodes.SERVER_ERROR,
            expected_error_message=None,
            is_success=False,
        ),
        id="invalid-id-format",
    ),
]
