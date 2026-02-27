"""Secret-masking utility — redacts sensitive field values before logging/attaching."""

from __future__ import annotations

import re

# Sensitive field names whose values should be redacted.
_SENSITIVE_FIELDS = r"password|authorization"

# Matches: "fieldName": "value", 'fieldName': 'value', or "fieldName": 123
_PATTERN = re.compile(
    rf'"({_SENSITIVE_FIELDS})":\s*(?:"[^"]*"|\'[^\']*\'|\d+)',
    flags=re.IGNORECASE,
)


def mask_secrets(data: str) -> str:
    """Replace sensitive field values in *data* (typically a JSON string) with ``[REDACTED]``.

    Targeted fields: ``password``, ``authorization`` (case-insensitive).

    Example::

        >>> mask_secrets('{"Authorization": "Bearer abc123", "name": "test"}')
        '{"Authorization": "[REDACTED]", "name": "test"}'
    """
    return _PATTERN.sub(r'"\1": "[REDACTED]"', data)
