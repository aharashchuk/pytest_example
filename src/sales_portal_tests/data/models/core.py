"""Core shared models used across all domains."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Literal, TypeVar

from sales_portal_tests.data.status_codes import StatusCodes

T = TypeVar("T")


@dataclass
class RequestOptions:
    url: str
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    data: object | None = None
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, str | int | list[str]] | None = None


@dataclass
class ResponseFields:
    is_success: bool
    error_message: str | None


@dataclass
class Response(Generic[T]):
    status: int
    headers: dict[str, str]
    body: T


@dataclass
class CaseApi:
    title: str
    expected_status: StatusCodes
    expected_error_message: str | None
    is_success: bool | None = True
