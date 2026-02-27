"""DDT cases for POST /api/products."""

from __future__ import annotations

import pytest
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.models.product import Product
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_data
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class CreateProductCase(CaseApi):
    product_data: Product | dict[str, object]

    def __init__(
        self,
        title: str,
        product_data: Product | dict[str, object],
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool = True,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.product_data = product_data


CREATE_PRODUCT_POSITIVE_CASES = [
    pytest.param(
        CreateProductCase(
            title="Create product with 3 character length in name",
            product_data=generate_product_data(name=_faker.pystr(min_chars=3, max_chars=3)),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="name-3-chars",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with 40 character length in name",
            product_data=generate_product_data(name=_faker.pystr(min_chars=40, max_chars=40)),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="name-40-chars",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with 1 space in name",
            product_data=generate_product_data(name="Test Product"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="name-with-space",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with min price (1)",
            product_data=generate_product_data(price=1),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="price-min",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with max price (99999)",
            product_data=generate_product_data(price=99999),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="price-max",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with min amount (0)",
            product_data=generate_product_data(amount=0),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="amount-min",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with max amount (999)",
            product_data=generate_product_data(amount=999),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="amount-max",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with 250 character notes",
            product_data=generate_product_data(notes=_faker.pystr(min_chars=250, max_chars=250)),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="notes-250-chars",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product with empty notes",
            product_data=generate_product_data(notes=""),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="notes-empty",
    ),
    pytest.param(
        CreateProductCase(
            title="Create product without notes",
            product_data=generate_product_data(notes=None),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="notes-omitted",
    ),
]

CREATE_PRODUCT_NEGATIVE_CASES = [
    pytest.param(
        CreateProductCase(
            title="Name too short (2 chars)",
            product_data=generate_product_data(name=_faker.pystr(min_chars=2, max_chars=2)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-too-short",
    ),
    pytest.param(
        CreateProductCase(
            title="Name too long (41 chars)",
            product_data=generate_product_data(name=_faker.pystr(min_chars=41, max_chars=41)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-too-long",
    ),
    pytest.param(
        CreateProductCase(
            title="Price zero is rejected",
            product_data=generate_product_data(price=0),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="price-zero",
    ),
    pytest.param(
        CreateProductCase(
            title="Price above max (100000) is rejected",
            product_data=generate_product_data(price=100_000),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="price-above-max",
    ),
    pytest.param(
        CreateProductCase(
            title="Notes too long (251 chars) is rejected",
            product_data=generate_product_data(notes=_faker.pystr(min_chars=251, max_chars=251)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="notes-too-long",
    ),
]
