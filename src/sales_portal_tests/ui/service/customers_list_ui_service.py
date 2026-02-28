"""CustomersListUIService — search, delete and navigate from the customers list."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from sales_portal_tests.ui.pages.customers.add_new_customer_page import AddNewCustomerPage
from sales_portal_tests.ui.pages.customers.customers_list_page import CustomersListPage
from sales_portal_tests.utils.report.allure_step import step


class CustomersListUIService:
    """High-level flows for the customers list page.

    Composes :class:`CustomersListPage` and :class:`AddNewCustomerPage`.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.customers_list_page = CustomersListPage(page)
        self.add_new_customer_page = AddNewCustomerPage(page)

    @step("OPEN CUSTOMERS LIST PAGE")
    def open(self) -> None:
        """Navigate directly to the customers list route."""
        self.customers_list_page.open("#/customers")
        self.customers_list_page.wait_for_opened()

    @step("OPEN ADD NEW CUSTOMER PAGE FROM LIST")
    def open_add_new_customer_page(self) -> None:
        """Click the Add New Customer button and wait for the form page."""
        self.customers_list_page.click_add_new_customer()
        self.add_new_customer_page.wait_for_opened()

    @step("OPEN CUSTOMER DETAILS MODAL")
    def open_details(self, customer_email: str) -> None:
        """Click the details button for *customer_email* and wait for the modal.

        Args:
            customer_email: Email of the customer whose details modal to open.
        """
        self.customers_list_page.details_button(customer_email).click()
        self.customers_list_page.details_modal.wait_for_opened()

    @step("OPEN DELETE CUSTOMER MODAL")
    def open_delete_modal(self, customer_email: str) -> None:
        """Click the delete button for *customer_email* and wait for the modal.

        Args:
            customer_email: Email of the customer to delete.
        """
        self.customers_list_page.click_action(customer_email, "delete")
        self.customers_list_page.delete_modal.wait_for_opened()

    @step("DELETE CUSTOMER VIA UI")
    def delete(self, customer_email: str) -> None:
        """Delete *customer_email*: click delete → confirm → wait for modal close.

        Args:
            customer_email: Email of the customer to delete.
        """
        self.customers_list_page.click_action(customer_email, "delete")
        self.customers_list_page.delete_modal.wait_for_opened()
        self.customers_list_page.delete_modal.click_confirm()
        self.customers_list_page.delete_modal.wait_for_closed()

    @step("SEARCH CUSTOMER ON CUSTOMERS LIST PAGE")
    def search(self, text: str) -> None:
        """Fill the search box with *text* and submit.

        Args:
            text: The search string to enter.
        """
        self.customers_list_page.fill_search_input(text)
        self.customers_list_page.click_search()
        self.customers_list_page.wait_for_opened()

    @step("ASSERT CUSTOMER IS VISIBLE IN TABLE")
    def assert_customer_visible(self, customer_email: str, *, visible: bool = True) -> None:
        """Assert that *customer_email* is (or is not) visible in the table.

        Args:
            customer_email: Email of the customer row to check.
            visible: ``True`` (default) to assert presence; ``False`` to assert absence.
        """
        expect(self.customers_list_page.table_row_by_email(customer_email)).to_be_visible(visible=visible)
