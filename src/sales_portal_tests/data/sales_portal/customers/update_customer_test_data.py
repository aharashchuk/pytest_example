"""DDT cases for PUT /api/customers/:id."""

from __future__ import annotations

import pytest
from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.models.customer import Customer
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_data
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class UpdateCustomerCase(CaseApi):
    customer_data: Customer | dict[str, object]
    customer_id: str | None

    def __init__(
        self,
        title: str,
        customer_data: Customer | dict[str, object],
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool = True,
        customer_id: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.customer_data = customer_data
        self.customer_id = customer_id


_non_existing_id = str(ObjectId())

UPDATE_CUSTOMER_POSITIVE_CASES = [
    pytest.param(
        UpdateCustomerCase(
            title="Update customer name to 1 character",
            customer_data={"name": "K"},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="name-1-char",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update customer name to 40 characters",
            customer_data={"name": "Alexandria Catherine Montgomery Smith Jr"},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="name-40-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update customer name with mixed case",
            customer_data={"name": "JoHn DoE"},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="name-mixed-case",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update email to valid format",
            customer_data={"email": _faker.email()},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="email-valid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update phone to valid format",
            customer_data={"phone": "+1" + _faker.numerify("##########")},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="phone-valid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update city to 1 character",
            customer_data={"city": "M"},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="city-1-char",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update city to 20 characters",
            customer_data={"city": "San Francisco City"},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="city-20-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update street to valid format",
            customer_data={"street": "Main Street 123"},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="street-valid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update house number",
            customer_data={"house": 42},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="house-valid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update flat number",
            customer_data={"flat": 101},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="flat-valid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update notes to 250 characters",
            customer_data={"notes": _faker.pystr(min_chars=250, max_chars=250)},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="notes-250-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Clear notes (empty string)",
            customer_data={"notes": ""},
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="notes-cleared",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update full customer data",
            customer_data=generate_customer_data(),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="full-customer-update",
    ),
]

UPDATE_CUSTOMER_INVALID_ID_CASES = [
    pytest.param(
        UpdateCustomerCase(
            title="404 returned for non-existing id of valid format",
            customer_data={"name": "ValidName"},
            customer_id=_non_existing_id,
            expected_status=StatusCodes.NOT_FOUND,
            expected_error_message=ResponseErrors.customer_not_found(_non_existing_id),
            is_success=False,
        ),
        id="non-existing-id",
    ),
]

UPDATE_CUSTOMER_NEGATIVE_CASES = [
    pytest.param(
        UpdateCustomerCase(
            title="Update name with empty string — bad request",
            customer_data={"name": ""},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-empty",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update name with 41 characters — bad request",
            customer_data={"name": _faker.pystr(min_chars=41, max_chars=41)},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-41-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update name with special characters — bad request",
            customer_data={"name": "John@#$%Doe"},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-special-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update with invalid email format — bad request",
            customer_data={"email": "invalid-email"},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="email-invalid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update with empty email — bad request",
            customer_data={"email": ""},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="email-empty",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update phone with invalid format — bad request",
            customer_data={"phone": "1234567"},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-invalid",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update phone without + sign — bad request",
            customer_data={"phone": "1234567890123"},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-no-plus",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update city with 21 characters — bad request",
            customer_data={"city": _faker.pystr(min_chars=21, max_chars=21)},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="city-21-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update city with empty string — bad request",
            customer_data={"city": ""},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="city-empty",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update street with 41 characters — bad request",
            customer_data={"street": _faker.pystr(min_chars=41, max_chars=41)},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-41-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update street with empty string — bad request",
            customer_data={"street": ""},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-empty",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update house with negative number — bad request",
            customer_data={"house": -1},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-negative",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update house with 1000 — bad request",
            customer_data={"house": 1000},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-too-large",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update flat with negative number — bad request",
            customer_data={"flat": -5},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-negative",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update flat with 10000 — bad request",
            customer_data={"flat": 10000},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-too-large",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update notes with 251 characters — bad request",
            customer_data={"notes": _faker.pystr(min_chars=251, max_chars=251)},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="notes-251-chars",
    ),
    pytest.param(
        UpdateCustomerCase(
            title="Update notes with < or > symbols — bad request",
            customer_data={"notes": "Invalid notes with <symbol>"},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="notes-angle-brackets",
    ),
]
