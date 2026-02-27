"""Response validation utility — checks status, IsSuccess, ErrorMessage, and optional JSON schema."""

from __future__ import annotations

from typing import Any

import pytest_check as check

from sales_portal_tests.data.models.core import Response
from sales_portal_tests.utils.validation.validate_schema import validate_json_schema


def validate_response(
    response: Response[Any],
    *,
    status: int,
    is_success: bool | None = None,
    error_message: str | None = None,
    schema: dict[str, object] | None = None,
) -> None:
    """Assert status code and optional body fields of an API *response*.

    Args:
        response:       The typed ``Response`` object returned by an API wrapper.
        status:         Expected HTTP status code (hard-checked first).
        is_success:     Expected value of ``body.IsSuccess`` (soft-checked if provided).
        error_message:  Expected value of ``body.ErrorMessage`` (soft-checked if provided).
        schema:         Optional JSON Schema dict — validated via ``validate_json_schema``
                        when provided (soft-checked).

    Notes:
        - ``status`` is always soft-asserted so all failures are collected.
        - ``is_success`` / ``error_message`` are only checked when explicitly passed.
        - Prefer either schema validation *or* Pydantic parsing as the primary shape
          assertion in a single test (see Decision 2 in the implementation plan).
    """
    check.equal(
        response.status,
        status,
        f"Expected HTTP status {status}, got {response.status}",
    )

    if is_success is not None:
        body = response.body
        actual_is_success = body.get("IsSuccess") if isinstance(body, dict) else getattr(body, "IsSuccess", None)
        check.equal(actual_is_success, is_success, f"Expected IsSuccess={is_success}, got {actual_is_success}")

    if error_message is not None:
        body = response.body
        actual_error_message = (
            body.get("ErrorMessage") if isinstance(body, dict) else getattr(body, "ErrorMessage", None)
        )
        check.equal(
            actual_error_message,
            error_message,
            f"Expected ErrorMessage={error_message!r}, got {actual_error_message!r}",
        )

    if schema is not None:
        body = response.body
        body_dict: dict[str, object]
        if isinstance(body, dict):
            body_dict = body
        elif hasattr(body, "model_dump"):
            body_dict = body.model_dump()
        else:
            body_dict = vars(body) if body is not None else {}
        validate_json_schema(body_dict, schema)
