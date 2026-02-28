"""CustomersListPage — customers table, search, add button, row action buttons."""

from __future__ import annotations

from typing import Literal

from playwright.sync_api import Locator, Page

from sales_portal_tests.data.sales_portal.country import Country
from sales_portal_tests.ui.pages.confirmation_modal import ConfirmationModal
from sales_portal_tests.ui.pages.customers.details_modal import CustomerDetailsModal
from sales_portal_tests.ui.pages.export_modal import ExportModal, customers_field_names_mapper
from sales_portal_tests.ui.pages.navbar_component import NavBar
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step

CustomerTableHeader = Literal["Email", "Name", "Country", "Created On"]
CustomerAction = Literal["edit", "delete", "details"]


class CustomersListPage(SalesPortalPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.details_modal = CustomerDetailsModal(self.page)
        self.delete_modal = ConfirmationModal(self.page)
        self.export_modal: ExportModal = ExportModal(self.page, customers_field_names_mapper)
        self.nav_bar = NavBar(self.page)

    @property
    def unique_element(self) -> Locator:
        return self.add_new_customer_button

    @property
    def customers_page_title(self) -> Locator:
        return self.page.locator("h2.fw-bold")

    @property
    def add_new_customer_button(self) -> Locator:
        return self.page.locator('[name="add-button"]')

    @property
    def table_row(self) -> Locator:
        return self.page.locator("tbody tr")

    def table_row_by_email(self, customer_email: str) -> Locator:
        return self.page.locator(
            "table tbody tr",
            has=self.page.locator("td", has_text=customer_email),
        )

    def table_row_by_index(self, index: int) -> Locator:
        return self.page.locator("table tbody tr").nth(index)

    def email_cell(self, customer_email: str) -> Locator:
        return self.table_row_by_email(customer_email).locator("td").nth(0)

    def name_cell(self, customer_email: str) -> Locator:
        return self.table_row_by_email(customer_email).locator("td").nth(1)

    def country_cell(self, customer_email: str) -> Locator:
        return self.table_row_by_email(customer_email).locator("td").nth(2)

    def created_on_cell(self, email_or_index: str | int) -> Locator:
        if isinstance(email_or_index, str):
            return self.table_row_by_email(email_or_index).locator("td").nth(3)
        return self.table_row_by_index(email_or_index).locator("td").nth(3)

    @property
    def table_header(self) -> Locator:
        return self.page.locator("thead th div[current]")

    def table_header_named(self, name: CustomerTableHeader) -> Locator:
        return self.table_header.filter(has_text=name)

    def table_header_arrow(
        self,
        name: CustomerTableHeader,
        direction: Literal["asc", "desc"],
    ) -> Locator:
        arrow_class = "bi-arrow-down" if direction == "asc" else "bi-arrow-up"
        return self.page.locator(
            "thead th",
            has=self.page.locator("div[current]", has_text=name),
        ).locator(f"i.{arrow_class}")

    def edit_button(self, customer_email: str) -> Locator:
        return self.table_row_by_email(customer_email).get_by_title("Edit")

    def details_button(self, customer_email: str) -> Locator:
        return self.table_row_by_email(customer_email).get_by_title("Details")

    def delete_button(self, customer_email: str) -> Locator:
        return self.table_row_by_email(customer_email).get_by_title("Delete")

    @property
    def search_input(self) -> Locator:
        return self.page.locator("#search")

    @property
    def search_button(self) -> Locator:
        return self.page.locator("#search-customers")

    # ── actions ───────────────────────────────────────────────────────────────

    @step("CLICK ADD NEW CUSTOMER")
    def click_add_new_customer(self) -> None:
        self.add_new_customer_button.click()

    @step("GET CUSTOMER DATA FROM TABLE")
    def get_customer_data(self, customer_email: str) -> dict[str, object]:
        email, name, country, created_on = self.table_row_by_email(customer_email).locator("td").all_inner_texts()
        return {
            "email": email,
            "name": name,
            "country": Country(country),
            "created_on": created_on,
        }

    @step("GET ALL CUSTOMERS' DATA IN TABLE")
    def get_table_data(self) -> list[dict[str, object]]:
        data: list[dict[str, object]] = []
        for row in self.table_row.all():
            email, name, country, created_on = row.locator("td").all_inner_texts()
            data.append(
                {
                    "email": email,
                    "name": name,
                    "country": Country(country),
                    "created_on": created_on,
                }
            )
        return data

    @step("CLICK ACTION BUTTON ON CUSTOMER LIST PAGE")
    def click_action(self, customer_email: str, button: CustomerAction) -> None:
        if button == "edit":
            self.edit_button(customer_email).click()
        elif button == "delete":
            self.delete_button(customer_email).click()
        elif button == "details":
            self.details_button(customer_email).click()

    @step("CLICK TABLE HEADER ON CUSTOMERS LIST PAGE")
    def click_table_header(self, name: CustomerTableHeader) -> None:
        self.table_header_named(name).click()

    @step("FILL SEARCH INPUT ON CUSTOMERS LIST PAGE")
    def fill_search_input(self, text: str) -> None:
        self.search_input.fill(text)

    @step("CLICK SEARCH BUTTON ON CUSTOMERS LIST PAGE")
    def click_search(self) -> None:
        self.search_button.click()

    @step("OPEN EXPORT MODAL ON CUSTOMERS LIST PAGE")
    def open_export_modal(self) -> None:
        export_button = self.page.locator('button[name="export-button"]')
        export_button.click()
        self.export_modal.check_fields_bulk(
            ["Email", "Name", "Country", "City", "Street", "House", "Flat", "Phone", "Created On"]
        )
