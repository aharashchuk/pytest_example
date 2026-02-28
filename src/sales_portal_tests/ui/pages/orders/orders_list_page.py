"""OrdersListPage — orders table, search, create order button, row actions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from playwright.sync_api import Locator, Page

from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.export_modal import ExportModal, orders_field_names_mapper
from sales_portal_tests.ui.pages.navbar_component import NavBar
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step

if TYPE_CHECKING:
    from sales_portal_tests.ui.pages.orders.create_order_modal import CreateOrderModal

OrdersTableHeader = Literal["_id", "email", "price", "delivery", "status", "assignedManager", "createdOn"]
OrderAction = Literal["details", "reopen"]

_HEADER_TEXT: dict[OrdersTableHeader, str] = {
    "_id": "Order Number",
    "email": "Email",
    "price": "Price",
    "delivery": "Delivery",
    "status": "Status",
    "assignedManager": "Assigned Manager",
    "createdOn": "Created On",
}


class OrdersListPage(SalesPortalPage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Avoid circular import: CreateOrderModal imports BaseModal which is clean
        from sales_portal_tests.ui.pages.orders.create_order_modal import CreateOrderModal

        self.create_order_modal = CreateOrderModal(self.page)
        self.export_modal: ExportModal = ExportModal(self.page, orders_field_names_mapper)
        self.nav_bar = NavBar(self.page)

    @property
    def unique_element(self) -> Locator:
        return self.create_order_button

    @property
    def title(self) -> Locator:
        return self.page.locator("h2.fw-bold")

    @property
    def create_order_button(self) -> Locator:
        return self.page.locator('[name="add-button"]')

    @property
    def table_row(self) -> Locator:
        return self.page.locator("tbody tr")

    def table_row_by_number(self, order_number: str) -> Locator:
        return self.page.locator(
            "table tbody tr",
            has=self.page.locator("td", has_text=order_number),
        )

    def table_row_by_index(self, index: int) -> Locator:
        return self.page.locator("table tbody tr").nth(index)

    def order_number_cell(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).locator("td").nth(0)

    def email_cell(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).locator("td").nth(1)

    def price_cell(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).locator("td").nth(2)

    def delivery_cell(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).locator("td").nth(3)

    def status_cell(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).locator("td").nth(4)

    def assigned_manager_cell(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).locator("td").nth(5)

    def created_on_cell(self, number_or_index: str | int) -> Locator:
        if isinstance(number_or_index, str):
            return self.table_row_by_number(number_or_index).locator("td").nth(6)
        return self.table_row_by_index(number_or_index).locator("td").nth(6)

    @property
    def table_header(self) -> Locator:
        return self.page.locator('thead th div[onclick*="sortOrdersInTable"]')

    def table_header_named(self, name: OrdersTableHeader) -> Locator:
        return self.table_header.filter(has_text=_HEADER_TEXT[name])

    def table_header_arrow(
        self,
        name: OrdersTableHeader,
        direction: Literal["asc", "desc"],
    ) -> Locator:
        arrow_class = "bi-arrow-down" if direction == "asc" else "bi-arrow-up"
        return self.page.locator(
            "thead th",
            has=self.page.locator("div", has_text=_HEADER_TEXT[name]),
        ).locator(f"i.{arrow_class}")

    def details_button(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).get_by_title("Details", exact=True)

    def reopen_button(self, order_number: str) -> Locator:
        return self.table_row_by_number(order_number).get_by_title("Reopen")

    @property
    def search_input(self) -> Locator:
        return self.page.locator("#search")

    @property
    def search_button(self) -> Locator:
        return self.page.locator("#search-orders")

    @property
    def export_button(self) -> Locator:
        return self.page.locator("#export")

    # ── actions ───────────────────────────────────────────────────────────────

    @step("CLICK CREATE ORDER BUTTON")
    def click_create_order_button(self) -> CreateOrderModal:
        self.create_order_button.click()
        return self.create_order_modal

    @step("GET ORDER'S DATA BY ORDER NUMBER")
    def get_order_data(self, order_number: str) -> dict[str, object]:
        cells = self.table_row_by_number(order_number).locator("td").all_inner_texts()
        order_id, email, price, delivery, status, assigned_manager, created_on = cells
        return {
            "order_id": order_id,
            "email": email,
            "price": float(price.replace("$", "")),
            "delivery": delivery,
            "status": OrderStatus(status),
            "assigned_manager": assigned_manager,
            "created_on": created_on,
        }

    @step("GET ALL ORDERS' DATA IN TABLE")
    def get_table_data(self) -> list[dict[str, object]]:
        data: list[dict[str, object]] = []
        for row in self.table_row.all():
            order_id, email, price, delivery, status, assigned_manager, created_on = row.locator("td").all_inner_texts()
            data.append(
                {
                    "order_id": order_id,
                    "email": email,
                    "price": float(price.replace("$", "")),
                    "delivery": delivery,
                    "status": OrderStatus(status),
                    "assigned_manager": assigned_manager,
                    "created_on": created_on,
                }
            )
        return data

    @step("CLICK ACTION BUTTON ON ORDERS LIST PAGE")
    def click_action(self, order_number: str, button: OrderAction) -> None:
        if button == "details":
            self.details_button(order_number).click()
        elif button == "reopen":
            self.reopen_button(order_number).click()

    @step("CLICK TABLE HEADER ON ORDERS LIST PAGE")
    def click_table_header(self, name: OrdersTableHeader) -> None:
        self.table_header_named(name).click()

    @step("FILL SEARCH INPUT ON ORDERS LIST PAGE")
    def fill_search_input(self, text: str) -> None:
        self.search_input.fill(text)

    @step("CLICK SEARCH BUTTON ON ORDERS LIST PAGE")
    def click_search(self) -> None:
        self.search_button.click()

    @step("OPEN EXPORT MODAL ON ORDERS LIST PAGE")
    def open_export_modal(self) -> None:
        self.export_button.click()
        self.export_modal.check_fields_bulk(
            ["Status", "Total Price", "Delivery", "Customer", "Products", "Assigned Manager", "Created On"]
        )
