"""Product data generators."""

from __future__ import annotations

import random

from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.product import OrderProductFromResponse, Product, ProductFromResponse
from sales_portal_tests.data.sales_portal.products.manufacturers import Manufacturers

_faker = Faker()


def generate_product_data(**overrides: object) -> Product:
    """Generate a random Product with optional field overrides."""
    data: dict[str, object] = {
        "name": _faker.word().capitalize() + str(_faker.random_int(min=1, max=100_000)),
        "manufacturer": random.choice(list(Manufacturers)),
        "price": _faker.random_int(min=1, max=99_999),
        "amount": _faker.random_int(min=0, max=999),
        "notes": _faker.pystr(max_chars=250),
    }
    data.update(overrides)
    return Product(**data)


def generate_product_response_data(**overrides: object) -> ProductFromResponse:
    """Generate a ProductFromResponse as it would appear in an API response."""
    base = generate_product_data()
    data: dict[str, object] = {
        "id": str(ObjectId()),
        "name": base.name,
        "manufacturer": base.manufacturer,
        "price": base.price,
        "amount": base.amount,
        "notes": base.notes or "",
        "created_on": _faker.iso8601(),
    }
    data.update(overrides)
    return ProductFromResponse(**data)


def generate_order_product_from_response(**overrides: object) -> OrderProductFromResponse:
    """Generate an OrderProductFromResponse (product inside an order)."""
    base = generate_product_response_data()
    data: dict[str, object] = {
        "id": base.id,
        "name": base.name,
        "manufacturer": base.manufacturer,
        "price": base.price,
        "amount": base.amount,
        "notes": base.notes,
        "received": False,
    }
    data.update(overrides)
    return OrderProductFromResponse(**data)
