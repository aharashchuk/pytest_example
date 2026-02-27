"""Typed ``allure.step`` decorator that preserves the wrapped function's full signature.

``allure.step`` ships without a ``py.typed`` marker, so mypy strict mode flags
every decorated method with::

    error: Untyped decorator makes function "<name>" untyped  [misc]

This module provides :func:`step` — a thin, fully-typed wrapper that delegates
to ``allure.step`` at runtime but keeps mypy happy by using ``ParamSpec`` /
``Callable`` to propagate the original signature unchanged.

Usage::

    from sales_portal_tests.utils.report.allure_step import step

    class ProductsApi:
        @step("POST /api/products")
        def create(self, product: Product, token: str) -> Response[object | None]:
            ...
"""

from __future__ import annotations

from collections.abc import Callable
from typing import ParamSpec, TypeVar

import allure

P = ParamSpec("P")
R = TypeVar("R")


def step(title: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Return a typed decorator that wraps *fn* in an Allure step named *title*.

    This is a typed shim around :func:`allure.step` so that ``mypy --strict``
    does not lose the type information of the decorated function.

    Args:
        title: The step title displayed in the Allure report.

    Returns:
        A decorator that, when applied to a callable, wraps it in an Allure
        step while preserving its exact ``ParamSpec``/return-type signature.
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        # allure.step returns the same callable at runtime; the cast is safe.
        decorated: Callable[P, R] = allure.step(title)(fn)
        return decorated

    return decorator
