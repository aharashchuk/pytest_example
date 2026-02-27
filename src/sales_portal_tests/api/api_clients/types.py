"""ApiClient Protocol — the structural interface all HTTP clients must satisfy."""

from __future__ import annotations

from typing import Protocol

from sales_portal_tests.data.models.core import RequestOptions, Response


class ApiClient(Protocol):
    """Structural protocol for HTTP clients.

    Any object that exposes a ``send`` method with the correct signature is
    considered a valid ``ApiClient`` — no explicit inheritance required.
    """

    def send(self, options: RequestOptions) -> Response[object | None]: ...
