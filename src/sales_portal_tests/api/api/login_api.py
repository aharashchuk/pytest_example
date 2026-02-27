"""LoginApi — endpoint wrapper for POST /api/login."""

from __future__ import annotations

from sales_portal_tests.api.api_clients.types import ApiClient
from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import RequestOptions, Response
from sales_portal_tests.data.models.credentials import Credentials
from sales_portal_tests.utils.report.allure_step import step


class LoginApi:
    """Endpoint wrapper for the login resource.

    Args:
        client: Any object satisfying the :class:`~sales_portal_tests.api.api_clients.types.ApiClient` protocol.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    @step("POST /api/login")
    def login(self, credentials: Credentials) -> Response[object | None]:
        """Authenticate with *credentials* and return the server response.

        The response headers will contain an ``Authorization`` bearer token on
        a successful login.

        Args:
            credentials: A :class:`~sales_portal_tests.data.models.credentials.Credentials`
                         instance holding ``username`` and ``password``.

        Returns:
            A :class:`~sales_portal_tests.data.models.core.Response` whose body
            contains the login JSON payload.
        """
        options = RequestOptions(
            url=api_config.LOGIN,
            method="POST",
            headers={"Content-Type": "application/json"},
            data={"email": credentials.username, "password": credentials.password},
        )
        return self._client.send(options)
