"""LoginPage — email/password form + submit button."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.data.models.credentials import Credentials
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class LoginPage(SalesPortalPage):
    @property
    def sign_in_page(self) -> Locator:
        return self.page.locator("#signInPage")

    @property
    def email_input(self) -> Locator:
        return self.page.locator("#emailinput")

    @property
    def password_input(self) -> Locator:
        return self.page.locator("#passwordinput")

    @property
    def login_button(self) -> Locator:
        return self.page.locator("button[type='submit']")

    @property
    def unique_element(self) -> Locator:
        return self.sign_in_page

    @step("FILL LOGIN CREDENTIALS")
    def fill_credentials(self, credentials: Credentials) -> None:
        if credentials.username:
            self.email_input.fill(credentials.username)
        if credentials.password:
            self.password_input.fill(credentials.password)

    @step("CLICK LOGIN BUTTON")
    def click_login(self) -> None:
        self.login_button.click()
