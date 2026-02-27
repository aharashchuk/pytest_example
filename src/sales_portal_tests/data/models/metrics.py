"""Metrics Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel


class TopProduct(BaseModel):
    name: str
    sales: int


class OrdersMetrics(BaseModel):
    totalRevenue: float
    totalOrders: int
    averageOrderValue: float
    totalCanceledOrders: int
    recentOrders: list[object] = []
    ordersCountPerDay: list[object] = []


class DateMetrics(BaseModel):
    year: int
    month: int
    day: int


class CustomersGrowthMetrics(BaseModel):
    date: DateMetrics
    count: int


class CustomersMetrics(BaseModel):
    totalNewCustomers: int
    topCustomers: list[object] = []
    customerGrowth: list[CustomersGrowthMetrics] = []


class ProductsMetrics(BaseModel):
    topProducts: list[TopProduct] = []


class MetricsBody(BaseModel):
    orders: OrdersMetrics
    customers: CustomersMetrics
    products: ProductsMetrics


class ResponseMetrics(BaseModel):
    IsSuccess: bool
    Metrics: MetricsBody
    ErrorMessage: str | None = None
