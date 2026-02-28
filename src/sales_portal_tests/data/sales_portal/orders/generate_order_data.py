"""Order data generator (mock/response shapes for UI tests)."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.order import Comment, OrderFromResponse
from sales_portal_tests.data.models.product import OrderProductFromResponse
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_response_data
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryCondition, DeliveryInfo
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.sales_portal.orders.generate_delivery_data import generate_delivery
from sales_portal_tests.data.sales_portal.orders.orders_list_integration_data import SortField, SortOrder
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


def generate_order_response_data(**overrides: Any) -> dict[str, Any]:
    """Return an ``IOrderResponse``-shaped dict suitable for mocking ``GET /api/orders/:id``.

    The outer envelope mirrors the backend response::

        {
            "Order": { …order fields… },
            "IsSuccess": True,
            "ErrorMessage": None,
        }
    """
    order = generate_order_data(**overrides)
    return {
        "Order": order.model_dump(by_alias=True),
        "IsSuccess": True,
        "ErrorMessage": None,
    }


def generate_orders_response_data(
    orders_count: int,
    sorting: dict[str, str] | None = None,
    **order_overrides: Any,
) -> dict[str, Any]:
    """Return an ``IOrdersResponse``-shaped dict for mocking ``GET /api/orders?…``.

    Args:
        orders_count: How many order objects to generate.
        sorting: Optional ``{"sortField": ..., "sortOrder": ...}`` dict embedded
            in the response (mirrors the backend envelope).
        **order_overrides: Forwarded to :func:`generate_order_data`.
    """
    orders = [generate_order_data(**order_overrides) for _ in range(orders_count)]
    sort_field: SortField = (sorting or {}).get("sortField", "createdOn")  # type: ignore[assignment]
    sort_order: SortOrder = (sorting or {}).get("sortOrder", "desc")  # type: ignore[assignment]
    return {
        "Orders": [o.model_dump(by_alias=True) for o in orders],
        "search": "",
        "IsSuccess": True,
        "ErrorMessage": None,
        "total": orders_count,
        "page": 1,
        "limit": 10,
        "status": [],
        "sorting": {
            "sortField": sort_field,
            "sortOrder": sort_order,
        },
    }


def _make_comment() -> Comment:
    return Comment(
        id=str(ObjectId()),
        text=_faker.sentence(),
        created_on=datetime.now().isoformat(),
    )
