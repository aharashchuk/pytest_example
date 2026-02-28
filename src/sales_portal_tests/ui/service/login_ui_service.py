"""LoginUIService — end-to-end login flow composing LoginPage + HomePage."""

from __future__ import annotations

from playwright.sync_api import Page

import sales_portal_tests.config.env as _env
from sales_portal_tests.data.models.credentials import Credentials
from sales_portal_tests.ui.pages.home_page import HomePage
from sales_portal_tests.ui.pages.login.login_page import LoginPage
from sales_portal_tests.utils.report.allure_step import step

# Re-wrap the env Credentials as the canonical data-model Credentials so that
# the type is consistent everywhere in the service layer.
_ADMIN_CREDENTIALS = Credentials(
    username=_env.CREDENTIALS.username,
    password=_env.CREDENTIALS.password,
)


class LoginUIService:
    """High-level login flows.

    Composes :class:`LoginPage` and :class:`HomePage` to provide
    single-call login helpers suitable for test setup.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_page = LoginPage(page)
        self.home_page = HomePage(page)

    @step("LOGIN AS ADMIN (UI)")
    def login_as_admin(self) -> str:
        """Log in using the configured admin credentials.

        Returns:
            The ``Authorization`` cookie value (token) extracted after login.
        """
        return self.login(_ADMIN_CREDENTIALS)

    @step("LOGIN WITH CREDENTIALS (UI)")
    def login(self, credentials: Credentials) -> str:
        """Open the login page, fill credentials, submit and wait for the home page.

        Args:
            credentials: Username / password pair to use.

        Returns:
            The ``Authorization`` cookie value (token) extracted after login.
        """
        self.login_page.open()
        self.login_page.fill_credentials(credentials)
        self.login_page.click_login()
        self.home_page.wait_for_opened()
        token = next(
            (c["value"] for c in self.page.context.cookies() if c["name"] == "Authorization"),
            "",
        )
        return token
