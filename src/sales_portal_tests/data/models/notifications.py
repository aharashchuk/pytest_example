"""Notifications Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel

from sales_portal_tests.data.sales_portal.notifications import NotificationsTypes


class NotificationId(BaseModel):
    id: str

    model_config = {"populate_by_name": True}


class Notification(BaseModel):
    id: str
    user_id: str
    type: NotificationsTypes
    order_id: str
    message: str
    read: bool
    created_at: str
    expires_at: str
    updated_at: str

    model_config = {"populate_by_name": True}


class NotificationsResponse(BaseModel):
    Notifications: list[Notification]
    IsSuccess: bool
    ErrorMessage: str | None
