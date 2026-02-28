"""BaseModal — ABC for all modal dialogs; adds *wait_for_closed* helper."""

from __future__ import annotations

from playwright.sync_api import expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage


class BaseModal(SalesPortalPage):
    def wait_for_closed(self) -> None:
        """Assert that the modal's *unique_element* is no longer visible."""
        expect(self.unique_element).not_to_be_visible(timeout=TIMEOUT_10_S)
