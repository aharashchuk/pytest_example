"""AddNewCustomerUIService — open the add-customer form and submit it."""

from __future__ import annotations

from playwright.sync_api import Page

from sales_portal_tests.data.models.customer import Customer
from sales_portal_tests.ui.pages.customers.add_new_customer_page import AddNewCustomerPage
from sales_portal_tests.ui.pages.customers.customers_list_page import CustomersListPage
from sales_portal_tests.utils.report.allure_step import step


class AddNewCustomerUIService:
    """High-level flows for creating a new customer via the UI.

    Composes :class:`AddNewCustomerPage` and :class:`CustomersListPage`.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.add_new_customer_page = AddNewCustomerPage(page)
        self.customers_list_page = CustomersListPage(page)

    @step("OPEN ADD NEW CUSTOMER PAGE")
    def open(self) -> None:
        """Navigate directly to the add-new-customer route."""
        self.add_new_customer_page.open("#/customers/add")
        self.add_new_customer_page.wait_for_opened()

    @step("CREATE NEW CUSTOMER VIA UI")
    def create(self, customer_data: Customer) -> None:
        """Fill the form with *customer_data*, save and wait for the list page.

        Args:
            customer_data: The :class:`~sales_portal_tests.data.models.customer.Customer`
                instance whose fields are used to populate the form.
        """
        self.add_new_customer_page.fill_form(customer_data)
        self.add_new_customer_page.click_save()
        self.customers_list_page.wait_for_opened()
