"""User Pydantic models."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Roles(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"


class User(BaseModel):
    id: str = Field(alias="_id", default="")
    username: str = ""
    first_name: str = Field(alias="firstName", default="")
    last_name: str = Field(alias="lastName", default="")
    roles: list[Roles] = Field(default_factory=list)
    created_on: str = Field(alias="createdOn", default="")
    is_success: bool = True
    error_message: str | None = None

    model_config = {"populate_by_name": True}

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> User:
        return cls(
            id=str(data.get("_id", "")),
            username=str(data.get("username", "")),
            first_name=str(data.get("firstName", "")),
            last_name=str(data.get("lastName", "")),
            roles=[Roles(r) for r in data.get("roles", [])],
            created_on=str(data.get("createdOn", "")),
            is_success=bool(data.get("IsSuccess", True)),
            error_message=data.get("ErrorMessage"),
        )
