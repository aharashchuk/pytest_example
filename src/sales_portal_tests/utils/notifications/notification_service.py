"""Notification service Protocol and concrete wrapper."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class NotificationService(Protocol):
    """Protocol for notification back-ends.

    Any class that implements ``post_notification(text)`` satisfies this protocol
    without explicit inheritance — structural sub-typing (duck-typing) applies.
    """

    def post_notification(self, text: str) -> None:
        """Send *text* as a notification.

        Args:
            text: The notification message to send.
        """
        ...
