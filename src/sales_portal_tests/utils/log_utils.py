"""Conditional logging utility — prints only when ``TEST_ENV`` is set."""

from __future__ import annotations

import os


def log(message: str) -> None:
    """Print *message* to stdout only when the ``TEST_ENV`` environment variable is set.

    This mirrors the TypeScript ``log()`` helper and keeps test output clean in CI
    while enabling verbose output locally (``TEST_ENV=dev pytest ...``).
    """
    if os.getenv("TEST_ENV"):
        print(message)
