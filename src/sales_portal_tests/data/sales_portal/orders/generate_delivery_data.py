"""Delivery data generator."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

from faker import Faker

from sales_portal_tests.data.sales_portal.country import Country
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryAddress, DeliveryCondition, DeliveryInfo

_faker = Faker()


def generate_delivery(**overrides: object) -> DeliveryInfo:
    """Generate a random DeliveryInfo with optional field overrides.

    The ``finalDate`` is set 7 days from now in ``YYYY/MM/DD`` format to match
    the API's expected date format.
    """
    final_date = (datetime.now() + timedelta(days=7)).strftime("%Y/%m/%d")

    address = DeliveryAddress(
        country=Country(random.choice(list(Country))),
        city=_faker.city().replace("'", "").replace("-", ""),
        street=_faker.street_name().replace("'", "").replace("-", ""),
        house=_faker.random_int(min=1, max=999),
        flat=_faker.random_int(min=1, max=9_999),
    )

    result = DeliveryInfo(
        address=address,
        condition=DeliveryCondition.DELIVERY,
        final_date=final_date,
    )

    for key, value in overrides.items():
        object.__setattr__(result, key, value)

    return result
