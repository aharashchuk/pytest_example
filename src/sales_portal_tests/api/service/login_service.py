"""LoginService — business-level login flow with validation."""

from __future__ import annotations

from sales_portal_tests.api.api.login_api import LoginApi
from sales_portal_tests.config import env as _env
from sales_portal_tests.data.models.credentials import Credentials
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.report.allure_step import step
from sales_portal_tests.utils.validation.validate_response import validate_response


class LoginService:
    """High-level login service.

    Args:
        login_api: Low-level :class:`~sales_portal_tests.api.api.login_api.LoginApi` wrapper.
    """

    def __init__(self, login_api: LoginApi) -> None:
        self._login_api = login_api

    @step("LOGIN AS ADMIN - API")
    def login_as_admin(self, credentials: Credentials | None = None) -> str:
        """Authenticate as admin and return the bearer token.

        Args:
            credentials: Custom credentials.  Defaults to the ``CREDENTIALS``
                         constant from :mod:`~sales_portal_tests.config.env`.

        Returns:
            The ``Authorization`` bearer token string from the response headers.
        """
        env_creds = _env.CREDENTIALS
        raw = (
            credentials
            if credentials is not None
            else Credentials(
                username=env_creds.username,
                password=env_creds.password,
            )
        )
        response = self._login_api.login(raw)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
        )
        token = response.headers.get("authorization", "")
        assert token, "Expected a non-empty Authorization token in the login response headers"
        return token
