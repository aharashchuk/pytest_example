"""Product Pydantic models for API request/response bodies."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sales_portal_tests.data.sales_portal.products.manufacturers import Manufacturers


class Product(BaseModel):
    name: str
    manufacturer: Manufacturers
    price: int
    amount: int
    notes: str | None = None


class ProductFromResponse(BaseModel):
    id: str = ""
    name: str = ""
    manufacturer: Manufacturers = Manufacturers.APPLE
    price: int = 0
    amount: int = 0
    notes: str = ""
    created_on: str = ""

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> ProductFromResponse:
        return cls(
            id=str(data.get("_id", "")),
            name=str(data.get("name", "")),
            manufacturer=Manufacturers(data.get("manufacturer", Manufacturers.APPLE)),
            price=int(data.get("price", 0)),
            amount=int(data.get("amount", 0)),
            notes=str(data.get("notes", "")),
            created_on=str(data.get("createdOn", "")),
        )


class ProductResponse(BaseModel):
    Product: ProductFromResponse
    IsSuccess: bool
    ErrorMessage: str | None


class ProductsResponse(BaseModel):
    Products: list[ProductFromResponse]
    IsSuccess: bool
    ErrorMessage: str | None


class OrderProductFromResponse(BaseModel):
    id: str = Field(alias="_id", default="")
    name: str = ""
    manufacturer: Manufacturers = Manufacturers.APPLE
    price: int = 0
    amount: int = 0
    notes: str | None = None
    received: bool = False

    model_config = {"populate_by_name": True}
