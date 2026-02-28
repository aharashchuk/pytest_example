"""ExportModal — format selection (CSV/JSON), field checkboxes, download button.

Field-name mappers and factory helpers mirror the TypeScript equivalents so that
tests can use the same Literal types for checkbox names.
"""

from __future__ import annotations

from typing import Literal

from playwright.sync_api import Download, Locator, Page, expect

from sales_portal_tests.ui.pages.base_modal import BaseModal
from sales_portal_tests.utils.report.allure_step import step

ExportFormat = Literal["CSV", "JSON"]

_EXPORT_FORMAT_ID: dict[ExportFormat, str] = {
    "CSV": "exportCsv",
    "JSON": "exportJson",
}

# ── field-name → checkbox value mappers ──────────────────────────────────────

ProductsCheckbox = Literal[
    "Select All",
    "Name",
    "Price",
    "Manufacturer",
    "Amount",
    "Created On",
    "Notes",
]

CustomersCheckbox = Literal[
    "Select All",
    "Email",
    "Name",
    "Country",
    "City",
    "Street",
    "House",
    "Flat",
    "Phone",
    "Created On",
]

OrdersCheckbox = Literal[
    "Select All",
    "Status",
    "Total Price",
    "Delivery",
    "Customer",
    "Products",
    "Assigned Manager",
    "Created On",
]

products_field_names_mapper: dict[str, str] = {
    "Select All": "selectAll",
    "Name": "product_name",
    "Price": "product_price",
    "Manufacturer": "product_manufacturer",
    "Amount": "product_amount",
    "Created On": "product_createdOn",
    "Notes": "product_notes",
}

customers_field_names_mapper: dict[str, str] = {
    "Select All": "selectAll",
    "Email": "customer_email",
    "Name": "customer_name",
    "Country": "customer_country",
    "City": "customer_city",
    "Street": "customer_street",
    "House": "customer_house",
    "Flat": "customer_flat",
    "Phone": "customer_phone",
    "Created On": "customer_createdOn",
}

orders_field_names_mapper: dict[str, str] = {
    "Select All": "selectAll",
    "Status": "status",
    "Total Price": "total_price",
    "Delivery": "delivery",
    "Customer": "customer",
    "Products": "products",
    "Assigned Manager": "assignedManager",
    "Created On": "createdOn",
}


class ExportModal(BaseModal):
    """Export modal — field checkboxes, format selection, download."""

    def __init__(self, page: Page, field_names_mapper: dict[str, str]) -> None:
        super().__init__(page)
        self._field_names_mapper = field_names_mapper

    # ── locators ─────────────────────────────────────────────────────────────

    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#exportModal")

    @property
    def fields_checkboxes_container(self) -> Locator:
        return self.unique_element.locator("#fields-checkboxes")

    @property
    def select_all_checkbox(self) -> Locator:
        return self.unique_element.locator("#select-all-fields")

    @property
    def download_button(self) -> Locator:
        return self.unique_element.locator("#export-button")

    @property
    def cancel_button(self) -> Locator:
        return self.unique_element.locator("button.btn-secondary")

    @property
    def close_button(self) -> Locator:
        return self.unique_element.locator("button.btn-close")

    def format_radio(self, fmt: ExportFormat) -> Locator:
        return self.unique_element.locator(f"#{_EXPORT_FORMAT_ID[fmt]}")

    def format_label(self, fmt: ExportFormat) -> Locator:
        return self.unique_element.locator(f'label[for="{_EXPORT_FORMAT_ID[fmt]}"]')

    def field_checkbox(self, name: str) -> Locator:
        value = self._field_names_mapper[name]
        return self.fields_checkboxes_container.locator(f'input[value="{value}"]')

    # ── actions ───────────────────────────────────────────────────────────────

    @step("CHECK FIELD IN EXPORT MODAL")
    def check_field(self, name: str, *, should_be_checked: bool = True) -> None:
        checkbox = self.field_checkbox(name)
        if should_be_checked:
            checkbox.check()
        else:
            checkbox.uncheck()

    @step("CHECK FIELDS IN BULK IN EXPORT MODAL")
    def check_fields_bulk(self, names: list[str], *, should_be_checked: bool = True) -> None:
        for name in names:
            self.check_field(name, should_be_checked=should_be_checked)

    @step("SELECT EXPORT FORMAT IN EXPORT MODAL")
    def select_format(self, fmt: ExportFormat) -> None:
        radio = self.format_radio(fmt)
        if radio.count() > 0:
            radio.check()
            return
        self.format_label(fmt).click()

    @step("CHECK ALL FIELDS IN EXPORT MODAL")
    def check_all_fields(self) -> None:
        self.select_all_checkbox.check()

    @step("UNCHECK ALL FIELDS IN EXPORT MODAL")
    def uncheck_all_fields(self) -> None:
        if self.select_all_checkbox.count() > 0:
            self.select_all_checkbox.uncheck()
        for name in self._field_names_mapper:
            if name == "Select All":
                continue
            self.check_field(name, should_be_checked=False)

    @step("CLICK CANCEL BUTTON IN EXPORT MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("CLOSE EXPORT MODAL")
    def close(self) -> None:
        self.close_button.click()

    @step("CLICK DOWNLOAD BUTTON IN EXPORT MODAL")
    def click_download(self) -> None:
        expect(self.download_button).to_be_visible()
        self.download_button.click()

    @step("DOWNLOAD FILE IN EXPORT MODAL")
    def download_file(self) -> Download:
        expect(self.download_button).to_be_visible()
        with self.page.expect_download() as download_info:
            self.download_button.click()
        return download_info.value


# ── factory helpers ───────────────────────────────────────────────────────────


def create_orders_export_modal(page: Page) -> ExportModal:
    return ExportModal(page, orders_field_names_mapper)


def create_products_export_modal(page: Page) -> ExportModal:
    return ExportModal(page, products_field_names_mapper)


def create_customers_export_modal(page: Page) -> ExportModal:
    return ExportModal(page, customers_field_names_mapper)
