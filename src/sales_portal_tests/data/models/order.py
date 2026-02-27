"""Order Pydantic models for API request/response bodies."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sales_portal_tests.data.models.customer import CustomerFromResponse
from sales_portal_tests.data.models.delivery import DeliveryInfoModel
from sales_portal_tests.data.models.product import OrderProductFromResponse
from sales_portal_tests.data.models.user import User
from sales_portal_tests.data.sales_portal.order_status import OrderStatus


class Comment(BaseModel):
    id: str = Field(alias="_id", default="")
    text: str = ""
    created_on: str = Field(alias="createdOn", default="")

    model_config = {"populate_by_name": True}


class OrderCreateBody(BaseModel):
    customer: str
    products: list[str]


class OrderUpdateBody(BaseModel):
    customer: str | None = None
    products: list[str] | None = None


class OrderFromResponse(BaseModel):
    id: str = Field(alias="_id", default="")
    status: OrderStatus = OrderStatus.DRAFT
    customer: CustomerFromResponse = Field(default_factory=CustomerFromResponse)
    products: list[OrderProductFromResponse] = Field(default_factory=list)
    total_price: float = Field(alias="total_price", default=0.0)
    delivery: DeliveryInfoModel | None = None
    comments: list[Comment] = Field(default_factory=list)
    history: list[dict[str, object]] = Field(default_factory=list)
    assigned_manager: User | None = Field(alias="assignedManager", default=None)
    created_on: str = Field(alias="createdOn", default="")

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
