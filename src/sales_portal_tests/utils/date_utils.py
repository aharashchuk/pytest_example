"""Date formatting utilities — stdlib only, no third-party dependencies."""

from __future__ import annotations

from datetime import datetime

_DATE_FORMAT = "%Y/%m/%d"
_DATE_AND_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"


def _parse(value: str | datetime) -> datetime:
    """Parse *value* to a ``datetime`` object.

    Accepts:
    - A ``datetime`` instance (returned as-is).
    - An ISO-8601 string (e.g. ``"2025-12-31T14:30:00"`` or ``"2025-12-31"``).
    """
    if isinstance(value, datetime):
        return value
    # Try full ISO datetime first, then date-only
    for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date/time value: {value!r}")


def convert_to_date(value: str | datetime) -> str:
    """Return *value* formatted as ``YYYY/MM/DD``."""
    return _parse(value).strftime(_DATE_FORMAT)


def convert_to_date_and_time(value: str | datetime) -> str:
    """Return *value* formatted as ``YYYY/MM/DD HH:MM:SS``."""
    return _parse(value).strftime(_DATE_AND_TIME_FORMAT)


def convert_to_full_date_and_time(value: str | datetime) -> str:
    """Return *value* formatted as a human-readable string, e.g. ``October 24, 2024 3:34 PM``."""
    return _parse(value).strftime("%B %-d, %Y %-I:%M %p")
