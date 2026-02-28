"""Network interception helpers for integration tests.

Uses Playwright's ``page.route()`` to intercept outgoing requests and return
pre-programmed responses — no real network call is made.

Usage::

    from sales_portal_tests.mock.mock import Mock

    def test_example(page, mock):
        mock.get_customers_all({"Customers": [], "IsSuccess": True, "ErrorMessage": None})
        ...
"""

from __future__ import annotations

import json
import re
from typing import Any

from playwright.sync_api import Page

from sales_portal_tests.config import api_config
from sales_portal_tests.data.status_codes import StatusCodes


class Mock:
    """Thin wrapper around ``page.route()`` for common Sales-Portal intercepts."""

    def __init__(self, page: Page) -> None:
        self._page = page

    # ------------------------------------------------------------------
    # Generic router
    # ------------------------------------------------------------------

    def route_request(
        self,
        url: str | re.Pattern[str],
        body: dict[str, Any],
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Intercept *all* requests matching *url* and respond with *body*."""

        def _handler(route: Any) -> None:  # RouteHandler
            route.fulfill(
                status=status_code,
                content_type="application/json",
                body=json.dumps(body),
            )

        self._page.route(url, _handler)

    # ------------------------------------------------------------------
    # Domain-specific convenience helpers
    # ------------------------------------------------------------------

    def products_page(
        self,
        body: dict[str, Any],
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/products?…`` (sorted/filtered list, may have query params)."""
        self.route_request(re.compile(r"/api/products(\?.*)?$"), body, status_code)

    def product_details_modal(
        self,
        body: dict[str, Any],
        product_id: str,
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/products/:id`` (single-product detail)."""
        self.route_request(api_config.product_by_id(product_id), body, status_code)

    def metrics_home_page(
        self,
        body: dict[str, Any],
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/metrics``."""
        self.route_request(api_config.METRICS, body, status_code)

    def orders_page(
        self,
        body: dict[str, Any],
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/orders?…`` (sorted/filtered list, may have query params)."""
        self.route_request(re.compile(r"/api/orders\?.*$"), body, status_code)

    def order_details_modal(
        self,
        body: dict[str, Any],
        order_id: str,
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/orders/:id`` (single order detail)."""
        self.route_request(api_config.order_by_id(order_id), body, status_code)

    def create_order_modal(
        self,
        body: dict[str, Any],
        status_code: int = StatusCodes.CREATED,
    ) -> None:
        """Mock ``POST /api/orders`` (create order endpoint)."""
        self.route_request(api_config.ORDERS, body, status_code)

    def get_customers_all(
        self,
        body: dict[str, Any],
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/customers/all``."""
        self.route_request(api_config.CUSTOMERS_ALL, body, status_code)

    def get_products_all(
        self,
        body: dict[str, Any],
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/products/all``."""
        self.route_request(api_config.PRODUCTS_ALL, body, status_code)

    def order_by_id(
        self,
        body: dict[str, Any],
        order_id: str,
        status_code: int = StatusCodes.OK,
    ) -> None:
        """Mock ``GET /api/orders/:id``."""
        self.route_request(api_config.order_by_id(order_id), body, status_code)
