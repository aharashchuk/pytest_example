"""ProductsListPage — products table, search, add button, row action buttons."""

from __future__ import annotations

from typing import Literal

from playwright.sync_api import Locator, Page

from sales_portal_tests.data.sales_portal.products.manufacturers import Manufacturers
from sales_portal_tests.ui.pages.confirmation_modal import ConfirmationModal
from sales_portal_tests.ui.pages.export_modal import ExportModal, products_field_names_mapper
from sales_portal_tests.ui.pages.navbar_component import NavBar
from sales_portal_tests.ui.pages.products.details_modal import ProductDetailsModal
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step

ProductsTableHeader = Literal["Name", "Price", "Manufacturer", "Created On"]
ProductAction = Literal["edit", "delete", "details"]


class ProductsListPage(SalesPortalPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.details_modal = ProductDetailsModal(self.page)
        self.delete_modal = ConfirmationModal(self.page)
        self.export_modal: ExportModal = ExportModal(self.page, products_field_names_mapper)
        self.nav_bar = NavBar(self.page)

    @property
    def unique_element(self) -> Locator:
        return self.add_new_product_button

    @property
    def products_page_title(self) -> Locator:
        return self.page.locator("h2.fw-bold")

    @property
    def add_new_product_button(self) -> Locator:
        return self.page.locator('[name="add-button"]')

    @property
    def table_row(self) -> Locator:
        return self.page.locator("tbody tr")

    def table_row_by_name(self, product_name: str) -> Locator:
        return self.page.locator(
            "table tbody tr",
            has=self.page.locator("td", has_text=product_name),
        )

    def table_row_by_index(self, index: int) -> Locator:
        return self.page.locator("table tbody tr").nth(index)

    def name_cell(self, product_name: str) -> Locator:
        return self.table_row_by_name(product_name).locator("td").nth(0)

    def price_cell(self, product_name: str) -> Locator:
        return self.table_row_by_name(product_name).locator("td").nth(1)

    def manufacturer_cell(self, product_name: str) -> Locator:
        return self.table_row_by_name(product_name).locator("td").nth(2)

    def created_on_cell(self, name_or_index: str | int) -> Locator:
        if isinstance(name_or_index, str):
            return self.table_row_by_name(name_or_index).locator("td").nth(3)
        return self.table_row_by_index(name_or_index).locator("td").nth(3)

    @property
    def table_header(self) -> Locator:
        return self.page.locator("thead th div[current]")

    def table_header_named(self, name: ProductsTableHeader) -> Locator:
        return self.table_header.filter(has_text=name)

    def table_header_arrow(
        self,
        name: ProductsTableHeader,
        direction: Literal["asc", "desc"],
    ) -> Locator:
        arrow_class = "bi-arrow-down" if direction == "asc" else "bi-arrow-up"
        return self.page.locator(
            "thead th",
            has=self.page.locator("div[current]", has_text=name),
        ).locator(f"i.{arrow_class}")

    def edit_button(self, product_name: str) -> Locator:
        return self.table_row_by_name(product_name).get_by_title("Edit")

    def details_button(self, product_name: str) -> Locator:
        return self.table_row_by_name(product_name).get_by_title("Details")

    def delete_button(self, product_name: str) -> Locator:
        return self.table_row_by_name(product_name).get_by_title("Delete")

    @property
    def search_input(self) -> Locator:
        return self.page.locator("#search")

    @property
    def search_button(self) -> Locator:
        return self.page.locator("#search-products")

    # ── actions ───────────────────────────────────────────────────────────────

    @step("CLICK ADD NEW PRODUCT")
    def click_add_new_product(self) -> None:
        self.add_new_product_button.click()

    @step("GET PRODUCT DATA FROM TABLE")
    def get_product_data(self, product_name: str) -> dict[str, object]:
        cells = self.table_row_by_name(product_name).locator("td").all_inner_texts()
        name, price, manufacturer, created_on = cells
        return {
            "name": name,
            "price": float(price.replace("$", "")),
            "manufacturer": Manufacturers(manufacturer),
            "created_on": created_on,
        }

    @step("GET ALL PRODUCTS DATA IN TABLE")
    def get_table_data(self) -> list[dict[str, object]]:
        data: list[dict[str, object]] = []
        for row in self.table_row.all():
            name, price, manufacturer, created_on = row.locator("td").all_inner_texts()
            data.append(
                {
                    "name": name,
                    "price": float(price.replace("$", "")),
                    "manufacturer": Manufacturers(manufacturer),
                    "created_on": created_on,
                }
            )
        return data

    @step("CLICK ACTION BUTTON ON PRODUCTS LIST PAGE")
    def click_action(self, product_name: str, button: ProductAction) -> None:
        if button == "edit":
            self.edit_button(product_name).click()
        elif button == "delete":
            self.delete_button(product_name).click()
        elif button == "details":
            self.details_button(product_name).click()

    @step("CLICK TABLE HEADER ON PRODUCTS LIST PAGE")
    def click_table_header(self, name: ProductsTableHeader) -> None:
        self.table_header_named(name).click()

    @step("FILL SEARCH INPUT ON PRODUCTS LIST PAGE")
    def fill_search_input(self, text: str) -> None:
        self.search_input.fill(text)

    @step("CLICK SEARCH BUTTON ON PRODUCTS LIST PAGE")
    def click_search(self) -> None:
        self.search_button.click()

    @step("OPEN EXPORT MODAL ON PRODUCTS LIST PAGE")
    def open_export_modal(self) -> None:
        export_button = self.page.locator('button[name="export-button"]')
        export_button.click()
        self.export_modal.check_fields_bulk(["Name", "Price", "Manufacturer", "Amount", "Created On", "Notes"])
