"""DDT cases for POST /api/customers."""

from __future__ import annotations

import pytest
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.models.customer import Customer
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_data
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class CreateCustomerCase(CaseApi):
    customer_data: Customer | dict[str, object]

    def __init__(
        self,
        title: str,
        customer_data: Customer | dict[str, object],
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
        self.customer_data = customer_data


CREATE_CUSTOMER_POSITIVE_CASES = [
    # name
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 1 character length in name",
            customer_data=generate_customer_data(name="K"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="name-1-char",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 40 characters length in name",
            customer_data=generate_customer_data(name="Alexandria Catherine Montgomery Smith Jr"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="name-40-chars",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with upper-case name",
            customer_data=generate_customer_data(name="STESHA"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="name-uppercase",
    ),
    # email
    pytest.param(
        CreateCustomerCase(
            title="Create customer with upper-case email",
            customer_data=generate_customer_data(email="DONNY.BLACK@tTEST.COM"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="email-uppercase",
    ),
    # city
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 1 character length in city",
            customer_data=generate_customer_data(city="M"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="city-1-char",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 20 characters length in city",
            customer_data=generate_customer_data(city="Nolagthiosd Ghdipiso"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="city-20-chars",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with upper-case city",
            customer_data=generate_customer_data(city="TORONTO"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="city-uppercase",
    ),
    # street
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 1 character length in street",
            customer_data=generate_customer_data(street="J"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="street-1-char",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 40 characters length in street",
            customer_data=generate_customer_data(street="Alexandria Catherine Montgomery Smith Jr"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="street-40-chars",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with upper-case street",
            customer_data=generate_customer_data(street="SAINT JAMES"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="street-uppercase",
    ),
    # house
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 1 character length in house",
            customer_data=generate_customer_data(house=1),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="house-1",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 3 characters length in house",
            customer_data=generate_customer_data(house=999),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="house-999",
    ),
    # flat
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 1 character length in flat",
            customer_data=generate_customer_data(flat=1),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="flat-1",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 4 characters length in flat",
            customer_data=generate_customer_data(flat=9999),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="flat-9999",
    ),
    # phone
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 10 characters length in phone",
            customer_data=generate_customer_data(phone="+1234567890"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="phone-10-chars",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 20 characters length in phone",
            customer_data=generate_customer_data(phone="+12345678901234567890"),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="phone-20-chars",
    ),
    # notes
    pytest.param(
        CreateCustomerCase(
            title="Create customer with empty notes",
            customer_data=generate_customer_data(notes=""),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="notes-empty",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Create customer with 250 characters length in notes",
            customer_data=generate_customer_data(notes=_faker.pystr(min_chars=250, max_chars=250)),
            expected_status=StatusCodes.CREATED,
            expected_error_message=None,
        ),
        id="notes-250-chars",
    ),
]

CREATE_CUSTOMER_NEGATIVE_CASES = [
    # name
    pytest.param(
        CreateCustomerCase(
            title="Customer without name is not created",
            customer_data=generate_customer_data().model_dump(exclude={"name"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Customer with empty name is not created",
            customer_data=generate_customer_data(name=""),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-empty",
    ),
    pytest.param(
        CreateCustomerCase(
            title="41 characters name customer is not created",
            customer_data=generate_customer_data(name=_faker.pystr(min_chars=41, max_chars=41)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-41-chars",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Name with numbers customer is not created",
            customer_data=generate_customer_data(name="Sony87"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-with-numbers",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Name with underscore customer is not created",
            customer_data=generate_customer_data(name="Dan_99"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-with-underscore",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Name with 2 spaces in name customer is not created",
            customer_data=generate_customer_data(name="Test  Customer"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="name-double-space",
    ),
    # email
    pytest.param(
        CreateCustomerCase(
            title="Customer without email is not created",
            customer_data=generate_customer_data().model_dump(exclude={"email"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="email-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Customer with empty email is not created",
            customer_data=generate_customer_data(email=""),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="email-empty",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Email without @ customer is not created",
            customer_data=generate_customer_data(email="tata.com"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="email-no-at",
    ),
    # country
    pytest.param(
        CreateCustomerCase(
            title="Without country customer is not created",
            customer_data=generate_customer_data().model_dump(exclude={"country"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="country-missing",
    ),
    # city
    pytest.param(
        CreateCustomerCase(
            title="Customer without city is not created",
            customer_data=generate_customer_data().model_dump(exclude={"city"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="city-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Customer with empty city is not created",
            customer_data=generate_customer_data(city=""),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="city-empty",
    ),
    pytest.param(
        CreateCustomerCase(
            title="City with dash customer is not created",
            customer_data=generate_customer_data(city="Baden-Baden"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="city-with-dash",
    ),
    pytest.param(
        CreateCustomerCase(
            title="City with apostrophe customer is not created",
            customer_data=generate_customer_data(city="Kapa'a"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="city-with-apostrophe",
    ),
    # street
    pytest.param(
        CreateCustomerCase(
            title="Customer without street is not created",
            customer_data=generate_customer_data().model_dump(exclude={"street"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Customer with empty street is not created",
            customer_data=generate_customer_data(street=""),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-empty",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Street with dash customer is not created",
            customer_data=generate_customer_data(street="Rose-street"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-with-dash",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Street with apostrophe customer is not created",
            customer_data=generate_customer_data(street="Jamie's"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-with-apostrophe",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Street with 2 spaces customer is not created",
            customer_data=generate_customer_data(street="Test  Street"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="street-double-space",
    ),
    # house
    pytest.param(
        CreateCustomerCase(
            title="Customer without house is not created",
            customer_data=generate_customer_data().model_dump(exclude={"house"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="100000 house customer is not created",
            customer_data=generate_customer_data(house=100000),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-too-large",
    ),
    pytest.param(
        CreateCustomerCase(
            title="0 house customer is not created",
            customer_data=generate_customer_data(house=0),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-zero",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Negative house customer is not created",
            customer_data=generate_customer_data(house=-10),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-negative",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Not integer house customer is not created",
            customer_data={**generate_customer_data().model_dump(), "house": _faker.pystr(min_chars=5, max_chars=5)},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="house-not-integer",
    ),
    # flat
    pytest.param(
        CreateCustomerCase(
            title="Customer without flat is not created",
            customer_data=generate_customer_data().model_dump(exclude={"flat"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="100000 flat customer is not created",
            customer_data=generate_customer_data(flat=100000),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-too-large",
    ),
    pytest.param(
        CreateCustomerCase(
            title="0 flat customer is not created",
            customer_data=generate_customer_data(flat=0),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-zero",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Negative flat customer is not created",
            customer_data=generate_customer_data(flat=-10),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-negative",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Not integer flat customer is not created",
            customer_data={**generate_customer_data().model_dump(), "flat": _faker.pystr(min_chars=5, max_chars=5)},
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="flat-not-integer",
    ),
    # phone
    pytest.param(
        CreateCustomerCase(
            title="Customer without phone is not created",
            customer_data=generate_customer_data().model_dump(exclude={"phone"}),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-missing",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Customer with empty phone is not created",
            customer_data=generate_customer_data(phone=""),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-empty",
    ),
    pytest.param(
        CreateCustomerCase(
            title="+12345678 phone customer is not created",
            customer_data=generate_customer_data(phone="+12345678"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-too-short",
    ),
    pytest.param(
        CreateCustomerCase(
            title="+123456789123456789123 phone customer is not created",
            customer_data=generate_customer_data(phone="+123456789123456789123"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-too-long",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Dash in phone customer is not created",
            customer_data=generate_customer_data(phone="-"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-dash",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Customer without + in phone is not created",
            customer_data=generate_customer_data(phone="12345678910"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-no-plus",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Negative phone customer is not created",
            customer_data=generate_customer_data(phone="-1234567890"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="phone-negative",
    ),
    # notes
    pytest.param(
        CreateCustomerCase(
            title="251 notes customer is not created",
            customer_data=generate_customer_data(notes=_faker.pystr(min_chars=251, max_chars=251)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="notes-251-chars",
    ),
    pytest.param(
        CreateCustomerCase(
            title="Notes with < or > symbols customer is not created",
            customer_data=generate_customer_data(notes="Invalid notes with <symbol>"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="notes-with-angle-brackets",
    ),
]
