"""DDT cases for PUT /api/orders/:id/delivery (schedule delivery)."""

from __future__ import annotations

import random

import pytest
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.country import Country
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryAddress, DeliveryCondition, DeliveryInfo
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.orders.generate_delivery_data import generate_delivery
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class CreateDeliveryCase(CaseApi):
    delivery_data: DeliveryInfo | dict[str, object]

    def __init__(
        self,
        title: str,
        delivery_data: DeliveryInfo | dict[str, object],
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
        self.delivery_data = delivery_data


def _address_variation(
    country: Country | None = None,
    city: str = "New York",
    street: str = "5th Avenue",
    house: int = 1,
    flat: int = 101,
) -> DeliveryAddress:
    chosen_country: Country = country if country is not None else Country(random.choice(list(Country)))
    return DeliveryAddress(
        country=chosen_country,
        city=city,
        street=street,
        house=house,
        flat=flat,
    )


def _delivery_without_address_field(field: str) -> dict[str, object]:
    delivery = generate_delivery()
    addr = {
        "country": delivery.address.country,
        "city": delivery.address.city,
        "street": delivery.address.street,
        "house": delivery.address.house,
        "flat": delivery.address.flat,
    }
    addr.pop(field, None)
    return {
        "address": addr,
        "condition": delivery.condition,
        "finalDate": delivery.final_date,
    }


CREATE_DELIVERY_POSITIVE_CASES = [
    pytest.param(
        CreateDeliveryCase(
            title="Successfully set delivery info with all required fields",
            delivery_data=generate_delivery(),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="all-required-fields",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Successfully set pickup condition",
            delivery_data=generate_delivery(condition=DeliveryCondition.PICKUP),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="pickup-condition",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Successfully update with future date",
            delivery_data=generate_delivery(final_date="2025/12/31"),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="future-date",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Single character city name",
            delivery_data=generate_delivery(address=_address_variation(city="A")),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="city-1-char",
    ),
]

# --- negative sub-groups ---

_MISSING_FIELDS_CASES = [
    pytest.param(
        CreateDeliveryCase(
            title="Missing finalDate field",
            delivery_data={
                "address": {
                    "country": random.choice(list(Country)),
                    "city": "New York",
                    "street": "5th Ave",
                    "house": 1,
                    "flat": 101,
                },
                "condition": DeliveryCondition.DELIVERY,
            },
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="missing-final-date",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Missing condition field",
            delivery_data={
                "address": {
                    "country": random.choice(list(Country)),
                    "city": "New York",
                    "street": "5th Ave",
                    "house": 1,
                    "flat": 101,
                },
                "finalDate": "2025/12/31",
            },
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="missing-condition",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Missing address field",
            delivery_data={
                "condition": DeliveryCondition.DELIVERY,
                "finalDate": "2025/12/31",
            },
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="missing-address",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Missing country in address",
            delivery_data=_delivery_without_address_field("country"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="missing-address-country",
    ),
]

_INVALID_VALUES_CASES = [
    pytest.param(
        CreateDeliveryCase(
            title="Invalid condition value",
            delivery_data=generate_delivery(condition="Express"),  # intentional invalid value
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="invalid-condition",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Invalid date format",
            delivery_data=generate_delivery(final_date="15-01-2026"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INVALID_DATE,
            is_success=False,
        ),
        id="invalid-date-format",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Past date",
            delivery_data=generate_delivery(final_date="2024/12/31"),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="past-date",
    ),
]

_ADDRESS_VALIDATION_CASES = [
    pytest.param(
        CreateDeliveryCase(
            title="Negative house number",
            delivery_data=generate_delivery(address=_address_variation(house=-1)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="house-negative",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Zero flat number",
            delivery_data=generate_delivery(address=_address_variation(flat=0)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="flat-zero",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Empty city",
            delivery_data=generate_delivery(address=_address_variation(city="")),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="city-empty",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Empty street",
            delivery_data=generate_delivery(address=_address_variation(street="")),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="street-empty",
    ),
]

_BOUNDARY_CASES = [
    pytest.param(
        CreateDeliveryCase(
            title="Exceeded Max length city name (>20 chars)",
            delivery_data=generate_delivery(address=_address_variation(city=_faker.pystr(min_chars=21, max_chars=21))),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="city-21-chars",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Exceeded Max length street name (>40 chars)",
            delivery_data=generate_delivery(
                address=_address_variation(street=_faker.pystr(min_chars=41, max_chars=41))
            ),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="street-41-chars",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Exceeded Max house number (>999)",
            delivery_data=generate_delivery(address=_address_variation(house=1000)),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="house-1000",
    ),
]

_SPECIAL_CHARACTERS_CASES = [
    pytest.param(
        CreateDeliveryCase(
            title="Special characters in street",
            delivery_data=generate_delivery(address=_address_variation(street="!@#$%^&*Street!@#$%^&*")),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="street-special-chars",
    ),
    pytest.param(
        CreateDeliveryCase(
            title="Unicode characters in city",
            delivery_data=generate_delivery(address=_address_variation(city="北京市")),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.INCORRECT_DELIVERY,
            is_success=False,
        ),
        id="city-unicode",
    ),
]

CREATE_DELIVERY_NEGATIVE_CASES = [
    *_MISSING_FIELDS_CASES,
    *_INVALID_VALUES_CASES,
    *_ADDRESS_VALIDATION_CASES,
    *_BOUNDARY_CASES,
    *_SPECIAL_CHARACTERS_CASES,
]
