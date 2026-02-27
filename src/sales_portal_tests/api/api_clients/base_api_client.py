"""Abstract base class for all HTTP API clients."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sales_portal_tests.data.models.core import RequestOptions, Response


class BaseApiClient(ABC):
    """Abstract base for concrete API client implementations.

    Subclasses must implement:
    - :meth:`send` — execute an HTTP request described by *options*.
    - :meth:`_transform_response` — convert the raw library response into a
      typed :class:`~sales_portal_tests.data.models.core.Response` object.
    """

    @abstractmethod
    def send(self, options: RequestOptions) -> Response[object | None]:
        """Send an HTTP request and return a typed response.

        Args:
            options: A :class:`~sales_portal_tests.data.models.core.RequestOptions`
                     instance describing the request (URL, method, headers, body, params).

        Returns:
            A :class:`~sales_portal_tests.data.models.core.Response` with parsed
            ``status``, ``headers`` and ``body``.
        """

    @abstractmethod
    def _transform_response(self, raw_response: Any) -> Response[object | None]:
        """Transform the raw library-level response object into a typed ``Response``.

        Args:
            raw_response: The response object returned by the underlying HTTP library
                          (e.g., ``playwright.sync_api.APIResponse``).

        Returns:
            A :class:`~sales_portal_tests.data.models.core.Response` instance.
        """
