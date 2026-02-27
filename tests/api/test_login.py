"""Smoke test for the login API."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.service.login_service import LoginService


@allure.suite("API")
@allure.sub_suite("Login")
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.auth
class TestLogin:
    """Smoke tests for LoginService."""

    def test_login_as_admin_returns_token(self, login_service: LoginService) -> None:
        """login_as_admin() should return a non-empty bearer token."""
        token = login_service.login_as_admin()
        assert token, "Expected a non-empty token from login_as_admin()"
