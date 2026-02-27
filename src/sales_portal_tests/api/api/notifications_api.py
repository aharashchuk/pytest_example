"""NotificationsApi — endpoint wrappers for /api/notifications resources."""

from __future__ import annotations

from sales_portal_tests.api.api_clients.types import ApiClient
from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import RequestOptions, Response
from sales_portal_tests.utils.report.allure_step import step

_JSON_AUTH_HEADERS = {"Content-Type": "application/json"}


def _auth_headers(token: str) -> dict[str, str]:
    return {**_JSON_AUTH_HEADERS, "Authorization": f"Bearer {token}"}


class NotificationsApi:
    """Endpoint wrappers for the notifications resource.

    Args:
        client: Any object satisfying the :class:`~sales_portal_tests.api.api_clients.types.ApiClient` protocol.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    @step("GET /api/notifications")
    def get_user_notifications(self, token: str) -> Response[object | None]:
        """Retrieve all notifications for the authenticated user.

        Args:
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.NOTIFICATIONS,
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("PATCH /api/notifications/{id}/read")
    def mark_as_read(self, notification_id: str, token: str) -> Response[object | None]:
        """Mark a single notification as read.

        Args:
            notification_id: MongoDB ``_id`` of the notification.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.notification_as_read(notification_id),
            method="PATCH",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("PATCH /api/notifications/mark-all-read")
    def mark_all_as_read(self, token: str) -> Response[object | None]:
        """Mark all notifications as read for the authenticated user.

        Args:
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.NOTIFICATIONS_MARK_ALL_READ,
            method="PATCH",
            headers=_auth_headers(token),
        )
        return self._client.send(options)
