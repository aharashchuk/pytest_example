"""Order data generator (mock/response shapes for UI tests)."""

from __future__ import annotations

import random
from datetime import datetime

from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.order import Comment, OrderFromResponse
from sales_portal_tests.data.models.product import OrderProductFromResponse
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_response_data
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryCondition, DeliveryInfo
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.sales_portal.orders.generate_delivery_data import generate_delivery
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_order_product_from_response

_faker = Faker()


def generate_order_data(**overrides: object) -> OrderFromResponse:
    """Generate a random OrderFromResponse suitable for mock/response-builder usage."""
    products: list[OrderProductFromResponse] = [generate_order_product_from_response()]
    delivery: DeliveryInfo = generate_delivery()

    # Convert DeliveryInfo dataclass to the Pydantic DeliveryInfoModel expected by OrderFromResponse
    from sales_portal_tests.data.models.delivery import DeliveryAddressModel, DeliveryInfoModel

    delivery_model = DeliveryInfoModel(
        address=DeliveryAddressModel(
            country=delivery.address.country,
            city=delivery.address.city,
            street=delivery.address.street,
            house=delivery.address.house,
            flat=delivery.address.flat,
        ),
        condition=DeliveryCondition(delivery.condition),
        finalDate=delivery.final_date,
    )

    data: dict[str, object] = {
        "id": str(ObjectId()),
        "status": random.choice(list(OrderStatus)),
        "customer": generate_customer_response_data(),
        "products": products,
        "total_price": _faker.random_int(min=1, max=99_999),
        "delivery": delivery_model,
        "comments": [],
        "history": [],
        "assigned_manager": None,
        "created_on": datetime.now().isoformat(),
    }
    data.update(overrides)
    return OrderFromResponse(**data)


def generate_order_create_body(customer_id: str, product_ids: list[str]) -> dict[str, object]:
    """Build the minimal payload for POST /api/orders."""
    return {
        "customer": customer_id,
        "products": product_ids,
    }


def _make_comment() -> Comment:
    return Comment(
        id=str(ObjectId()),
        text=_faker.sentence(),
        created_on=datetime.now().isoformat(),
    )
