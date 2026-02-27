"""JSON Schema validation utility."""

from __future__ import annotations

import jsonschema
import pytest_check as check

from sales_portal_tests.utils.log_utils import log


def validate_json_schema(body: dict[str, object], schema: dict[str, object]) -> None:
    """Validate *body* against *schema* using jsonschema.

    Uses a soft assertion (pytest-check) so the test continues collecting
    failures instead of stopping at the first schema mismatch.
    """
    try:
        jsonschema.validate(instance=body, schema=schema)
        is_valid = True
        errors: list[str] = []
    except jsonschema.ValidationError as exc:
        is_valid = False
        errors = [str(exc.message)]
    except jsonschema.SchemaError as exc:
        is_valid = False
        errors = [f"Invalid schema definition: {exc.message}"]

    check.is_true(is_valid, f"Response body should match JSON schema. Errors: {errors}")

    if is_valid:
        log("Data is valid according to the schema.")
    else:
        log(f"Data is NOT valid according to the schema. Errors: {errors}")
