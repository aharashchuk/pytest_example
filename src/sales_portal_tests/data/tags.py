"""Pytest marker tag constants."""

from enum import StrEnum


class Tags(StrEnum):
    SMOKE = "smoke"
    REGRESSION = "regression"
    INTEGRATION = "integration"
    API = "api"
    UI = "ui"
    E2E = "e2e"
    AUTH = "auth"
    HOME_PAGE = "home"
    PRODUCTS = "products"
    CUSTOMERS = "customers"
    ORDERS = "orders"
    MANAGERS = "managers"
