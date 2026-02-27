"""Delivery condition, location enums and address/info dataclasses."""

from dataclasses import dataclass
from enum import StrEnum

from sales_portal_tests.data.sales_portal.country import Country


class DeliveryCondition(StrEnum):
    DELIVERY = "Delivery"
    PICKUP = "Pickup"


class DeliveryLocation(StrEnum):
    HOME = "Home"
    OTHER = "Other"


@dataclass
class DeliveryAddress:
    country: Country
    city: str
    street: str
    house: int
    flat: int


@dataclass
class DeliveryInfo:
    address: DeliveryAddress
    condition: DeliveryCondition
    final_date: str
