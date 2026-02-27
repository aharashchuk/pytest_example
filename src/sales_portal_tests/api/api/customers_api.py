"""CustomersApi — endpoint wrappers for /api/customers resources."""

from __future__ import annotations

from sales_portal_tests.api.api_clients.types import ApiClient
from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import RequestOptions, Response
from sales_portal_tests.data.models.customer import Customer
from sales_portal_tests.utils.report.allure_step import step

_JSON_AUTH_HEADERS = {"Content-Type": "application/json"}


def _auth_headers(token: str) -> dict[str, str]:
    return {**_JSON_AUTH_HEADERS, "Authorization": f"Bearer {token}"}


class CustomersApi:
    """Endpoint wrappers for the customers resource.

    Args:
        client: Any object satisfying the :class:`~sales_portal_tests.api.api_clients.types.ApiClient` protocol.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    @step("POST /api/customers")
    def create(self, token: str, customer: Customer | dict[str, object]) -> Response[object | None]:
        """Create a new customer.

        Args:
            token: Bearer auth token.
            customer: Customer payload — either a :class:`Customer` model instance
                or a plain :class:`dict` (used for negative tests with missing/invalid fields).
        """
        data = customer.model_dump() if isinstance(customer, Customer) else customer
        options = RequestOptions(
            url=api_config.CUSTOMERS,
            method="POST",
            headers=_auth_headers(token),
            data=data,
        )
        return self._client.send(options)

    @step("DELETE /api/customers/{customer_id}")
    def delete(self, token: str, customer_id: str) -> Response[object | None]:
        """Delete a customer by *customer_id*.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer to delete.
        """
        options = RequestOptions(
            url=api_config.customer_by_id(customer_id),
            method="DELETE",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("GET /api/customers")
    def get_list(
        self,
        token: str,
        params: dict[str, str | int | list[str]] | None = None,
    ) -> Response[object | None]:
        """Retrieve a paginated / filtered list of customers.

        Args:
            token: Bearer auth token.
            params: Optional query parameters (``page``, ``limit``, ``search``, etc.).
        """
        options = RequestOptions(
            url=api_config.CUSTOMERS,
            method="GET",
            headers=_auth_headers(token),
            params=params,
        )
        return self._client.send(options)

    @step("GET /api/customers/all")
    def get_all(self, token: str) -> Response[object | None]:
        """Retrieve all customers without pagination.

        Args:
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.CUSTOMERS_ALL,
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("GET /api/customers/{customer_id}")
    def get_by_id(self, token: str, customer_id: str) -> Response[object | None]:
        """Retrieve a single customer by *customer_id*.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer.
        """
        options = RequestOptions(
            url=api_config.customer_by_id(customer_id),
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("PUT /api/customers/{customer_id}")
    def update(
        self,
        token: str,
        customer_id: str,
        customer: Customer,
    ) -> Response[object | None]:
        """Replace an existing customer by *customer_id*.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer to update.
            customer: New customer payload.
        """
        options = RequestOptions(
            url=api_config.customer_by_id(customer_id),
            method="PUT",
            headers={**_auth_headers(token), "Accept": "application/json"},
            data=customer.model_dump(),
        )
        return self._client.send(options)
