"""ProductsApi — endpoint wrappers for /api/products resources."""

from __future__ import annotations

from sales_portal_tests.api.api_clients.types import ApiClient
from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import RequestOptions, Response
from sales_portal_tests.data.models.product import Product
from sales_portal_tests.utils.report.allure_step import step

_JSON_AUTH_HEADERS = {"Content-Type": "application/json"}


def _auth_headers(token: str) -> dict[str, str]:
    return {**_JSON_AUTH_HEADERS, "Authorization": f"Bearer {token}"}


class ProductsApi:
    """Endpoint wrappers for the products resource.

    Args:
        client: Any object satisfying the :class:`~sales_portal_tests.api.api_clients.types.ApiClient` protocol.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    @step("POST /api/products")
    def create(self, product: Product, token: str) -> Response[object | None]:
        """Create a new product.

        Args:
            product: Product payload.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.PRODUCTS,
            method="POST",
            headers=_auth_headers(token),
            data=product.model_dump(),
        )
        return self._client.send(options)

    @step("PUT /api/products/{id}")
    def update(self, product_id: str, product: Product, token: str) -> Response[object | None]:
        """Replace an existing product by *product_id*.

        Args:
            product_id: MongoDB ``_id`` of the product to update.
            product: New product payload.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.product_by_id(product_id),
            method="PUT",
            headers=_auth_headers(token),
            data=product.model_dump(),
        )
        return self._client.send(options)

    @step("GET /api/products/{id}")
    def get_by_id(self, product_id: str, token: str) -> Response[object | None]:
        """Retrieve a single product by *product_id*.

        Args:
            product_id: MongoDB ``_id`` of the product.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.product_by_id(product_id),
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("GET /api/products/all")
    def get_all(self, token: str) -> Response[object | None]:
        """Retrieve all products.

        Args:
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.PRODUCTS_ALL,
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("DELETE /api/products/{id}")
    def delete(self, product_id: str, token: str) -> Response[object | None]:
        """Delete a product by *product_id*.

        Args:
            product_id: MongoDB ``_id`` of the product to delete.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.product_by_id(product_id),
            method="DELETE",
            headers=_auth_headers(token),
        )
        return self._client.send(options)
