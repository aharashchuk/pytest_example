"""SalesPortalPage — intermediate ABC adding spinner/toast helpers and navigation."""

from __future__ import annotations

from abc import abstractmethod

from playwright.sync_api import Locator, expect

from sales_portal_tests.config.env import SALES_PORTAL_URL
from sales_portal_tests.data.sales_portal.constants import TIMEOUT_30_S
from sales_portal_tests.ui.pages.base_page import BasePage
from sales_portal_tests.utils.report.allure_step import step


class SalesPortalPage(BasePage):
    # ------------------------------------------------------------------
    # Shared locators
    # ------------------------------------------------------------------

    @property
    def spinner(self) -> Locator:
        return self.page.locator(".spinner-border")

    @property
    def toast_message(self) -> Locator:
        return self.page.locator(".toast-body")

    @property
    @abstractmethod
    def unique_element(self) -> Locator:
        """Each concrete page must expose an element that uniquely identifies it."""

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------

    @step("WAIT FOR SALES PORTAL PAGE TO OPEN")
    def wait_for_opened(self) -> None:
        """Assert *unique_element* is visible and all spinners are gone."""
        expect(self.unique_element).to_be_visible(timeout=TIMEOUT_30_S)
        self.wait_for_spinners()

    @step("WAIT FOR SPINNERS TO DISAPPEAR")
    def wait_for_spinners(self) -> None:
        """Wait until there are no active spinners on the page."""
        expect(self.spinner).to_have_count(0, timeout=TIMEOUT_30_S)

    @step("OPEN SALES PORTAL PAGE WITH ROUTE")
    def open(self, route: str = "") -> None:
        """Navigate to the sales portal, optionally appending *route*.

        Accepts any of these formats: ``'/#/orders/123'``, ``'#/orders/123'``,
        ``'/orders/123'`` — the leading ``/`` is stripped before concatenation.
        """
        normalized = route.strip().lstrip("/") if route else ""
        url = f"{SALES_PORTAL_URL}{normalized}" if normalized else SALES_PORTAL_URL
        self.page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT_30_S)
