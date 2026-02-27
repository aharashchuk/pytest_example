"""Customer Pydantic models for API request/response bodies."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from sales_portal_tests.data.sales_portal.country import Country


class Customer(BaseModel):
    email: str
    name: str
    country: Country
    city: str
    street: str
    house: int
    flat: int
    phone: str
    notes: str | None = None


class CustomerFromResponse(BaseModel):
    id: str = ""
    email: str = ""
    name: str = ""
    country: Country = Country.USA
    city: str = ""
    street: str = ""
    house: int = 0
    flat: int = 0
    phone: str = ""
    notes: str = ""
    created_on: str = ""

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> CustomerFromResponse:
        return cls(
            id=str(data.get("_id", "")),
            email=str(data.get("email", "")),
            name=str(data.get("name", "")),
            country=Country(data.get("country", Country.USA)),
            city=str(data.get("city", "")),
            street=str(data.get("street", "")),
            house=int(data.get("house", 0)),
            flat=int(data.get("flat", 0)),
            phone=str(data.get("phone", "")),
            notes=str(data.get("notes", "")),
            created_on=str(data.get("createdOn", "")),
        )


class CustomerResponse(BaseModel):
    Customer: CustomerFromResponse
    IsSuccess: bool
    ErrorMessage: str | None


class CustomersResponse(BaseModel):
    Customers: list[CustomerFromResponse]
    IsSuccess: bool
    ErrorMessage: str | None


class CustomerListResponse(BaseModel):
    Customers: list[CustomerFromResponse]
    total: int
    page: int
    limit: int
    search: str
    IsSuccess: bool
    ErrorMessage: str | None
