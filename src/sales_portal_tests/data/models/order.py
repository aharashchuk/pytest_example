"""Order Pydantic models for API request/response bodies."""

from __future__ import annotations

from pydantic import BaseModel

from sales_portal_tests.data.models.customer import CustomerFromResponse
from sales_portal_tests.data.models.delivery import DeliveryInfoModel
from sales_portal_tests.data.models.product import OrderProductFromResponse
from sales_portal_tests.data.models.user import User
from sales_portal_tests.data.sales_portal.order_status import OrderStatus


class Comment(BaseModel):
    id: str
    text: str
    created_on: str

    model_config = {"populate_by_name": True}


class OrderCreateBody(BaseModel):
    customer: str
    products: list[str]


class OrderUpdateBody(BaseModel):
    customer: str | None = None
    products: list[str] | None = None


class OrderFromResponse(BaseModel):
    id: str
    status: OrderStatus
    customer: CustomerFromResponse
    products: list[OrderProductFromResponse]
    total_price: float
    delivery: DeliveryInfoModel | None
    comments: list[Comment]
    history: list[dict[str, object]]
    assigned_manager: User | None
    created_on: str

    model_config = {"populate_by_name": True}


class OrderResponse(BaseModel):
    Order: OrderFromResponse
    IsSuccess: bool
    ErrorMessage: str | None


class OrdersResponse(BaseModel):
    Orders: list[OrderFromResponse]
    total: int
    page: int
    limit: int
    search: str
    IsSuccess: bool
    ErrorMessage: str | None
