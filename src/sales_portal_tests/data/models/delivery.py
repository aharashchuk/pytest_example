"""Delivery Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel

from sales_portal_tests.data.sales_portal.delivery_status import DeliveryCondition


class DeliveryAddressModel(BaseModel):
    country: str
    city: str
    street: str
    house: int
    flat: int


class DeliveryInfoModel(BaseModel):
    address: DeliveryAddressModel
    condition: DeliveryCondition
    finalDate: str
