"""Customer data generators."""

from __future__ import annotations

import random
import re

from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.customer import Customer, CustomerFromResponse
from sales_portal_tests.data.sales_portal.country import Country

_faker = Faker()


def _only_letters(text: str, max_len: int) -> str:
    cleaned = str(re.sub(r"[^A-Za-z ]+", " ", text))
    cleaned = str(re.sub(r"\s{2,}", " ", cleaned)).strip()
    return (cleaned or "John")[:max_len]


def _alpha_num_space(text: str, max_len: int) -> str:
    cleaned = str(re.sub(r"[^A-Za-z0-9 ]+", " ", text))
    cleaned = str(re.sub(r"\s{2,}", " ", cleaned)).strip()
    return (cleaned or "Main")[:max_len]


def _valid_email() -> str:
    return _faker.email().replace(" ", "")


def _valid_phone() -> str:
    digits = _faker.numerify("###############")
    return "+" + digits


def generate_customer_data(**overrides: object) -> Customer:
    """Generate a random Customer with optional field overrides."""
    name_raw = f"{_faker.first_name()} {_faker.last_name()}"
    city_raw = _faker.city()
    street_raw = f"{_faker.street_name()} {_faker.random_int(min=1, max=99)}"

    data: dict[str, object] = {
        "email": _valid_email(),
        "name": _only_letters(name_raw, 40),
        "country": random.choice(list(Country)),
        "city": _only_letters(city_raw, 20),
        "street": _alpha_num_space(street_raw, 40),
        "house": _faker.random_int(min=1, max=999),
        "flat": _faker.random_int(min=1, max=9_999),
        "phone": _valid_phone(),
        "notes": _faker.pystr(max_chars=30),
    }
    data.update(overrides)
    return Customer(**data)


def generate_customer_response_data(**overrides: object) -> CustomerFromResponse:
    """Generate a CustomerFromResponse as it would appear in an API response."""
    base = generate_customer_data()
    data: dict[str, object] = {
        "id": str(ObjectId()),
        "email": base.email,
        "name": base.name,
        "country": base.country,
        "city": base.city,
        "street": base.street,
        "house": base.house,
        "flat": base.flat,
        "phone": base.phone,
        "notes": base.notes or "",
        "created_on": _faker.iso8601(),
    }
    data.update(overrides)
    return CustomerFromResponse(**data)
