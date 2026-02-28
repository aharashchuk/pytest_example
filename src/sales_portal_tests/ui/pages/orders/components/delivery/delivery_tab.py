"""DeliveryTab — order details delivery information tabpanel."""

from __future__ import annotations

from playwright.sync_api import Locator

from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class DeliveryTab(SalesPortalPage):
    @property
    def tab(self) -> Locator:
        return self.page.locator('#delivery.tab-pane.active.show[role="tabpanel"]')

    @property
    def title(self) -> Locator:
        return self.tab.locator("h4", has_text="Delivery Information")

    @property
    def schedule_delivery_button(self) -> Locator:
        return self.tab.locator("#delivery-btn")

    @property
    def unique_element(self) -> Locator:
        return self.tab

    @property
    def order_info_table(self) -> Locator:
        return self.tab.locator("div.mb-4.p-3")

    @property
    def rows(self) -> Locator:
        return self.order_info_table.locator("div.c-details")

    @property
    def label_cells(self) -> Locator:
        return self.rows.locator("span:first-child")

    @property
    def value_cells(self) -> Locator:
        return self.rows.locator("span:last-child")

    @step("GET ALL DATA FROM DELIVERY INFO")
    def get_data(self) -> dict[str, object]:
        field_labels = self.label_cells.all_inner_texts()
        field_values = self.value_cells.all_inner_texts()

        label_to_value: dict[str, str] = {}
        for i, raw_label in enumerate(field_labels):
            label = raw_label.strip() if raw_label else ""
            if not label:
                continue
            label_to_value[label] = (field_values[i] if i < len(field_values) else "").strip()

        def text(label: str) -> str:
            return label_to_value.get(label, "").strip()

        def num(label: str) -> int:
            return int(text(label)) if text(label) else 0

        return {
            "delivery_type": text("Delivery Type"),
            "delivery_date": text("Delivery Date"),
            "country": text("Country"),
            "city": text("City"),
            "street": text("Street"),
            "house": num("House"),
            "flat": num("Flat"),
        }

    @step("OPEN DELIVERY FORM")
    def click_delivery_form(self) -> None:
        self.schedule_delivery_button.click()
