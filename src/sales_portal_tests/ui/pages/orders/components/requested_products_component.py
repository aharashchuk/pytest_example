"""OrderDetailsRequestedProducts — requested products section + receiving flow."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect

from sales_portal_tests.data.sales_portal.constants import TIMEOUT_10_S, TIMEOUT_15_S
from sales_portal_tests.ui.pages.base_page import BasePage
from sales_portal_tests.utils.report.allure_step import step


class OrderDetailsRequestedProducts(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#products-section").first

    @property
    def accordion_root(self) -> Locator:
        return self.page.locator("#products-accordion-section")

    @property
    def edit_button(self) -> Locator:
        return self.page.locator("#edit-products-pencil")

    @property
    def start_receiving_button(self) -> Locator:
        return self.unique_element.locator("#start-receiving-products, #start-receiving").first

    @property
    def save_receiving_button(self) -> Locator:
        return self.unique_element.locator(
            "#save-received-products, #save-receiving, button#save-received-products"
        ).first

    @property
    def cancel_receiving_button(self) -> Locator:
        return self.unique_element.locator("#cancel-receiving").first

    @property
    def select_all_checkbox(self) -> Locator:
        return self.unique_element.locator("#selectAll")

    @property
    def product_checkboxes(self) -> Locator:
        return self.page.locator('input[name="product"]')

    def product_item_by_index(self, index: int) -> Locator:
        return self.accordion_root.locator(f"#heading{index}").first

    def product_checkbox_by_index(self, index: int) -> Locator:
        return self.page.locator(f"#check{index}")

    def product_checkbox_by_id(self, product_id: str) -> Locator:
        return self.page.locator(f'input[name="product"][value="{product_id}"]').first

    def product_item_by_name(self, name: str) -> Locator:
        return self.unique_element.locator("button", has_text=name).first

    @step("PRODUCTS: CLICK EDIT")
    def click_edit(self) -> None:
        self.edit_button.click()

    @step("PRODUCTS: START RECEIVING")
    def start_receiving(self) -> None:
        self.start_receiving_button.click()

    @step("PRODUCTS: SAVE RECEIVING")
    def save_receiving(self) -> None:
        expect(self.save_receiving_button).to_be_enabled(timeout=TIMEOUT_10_S)
        self.save_receiving_button.click()

    @step("PRODUCTS: CANCEL RECEIVING")
    def cancel_receiving(self) -> None:
        self.cancel_receiving_button.click()

    @step("PRODUCTS: SELECT ALL")
    def select_all(self) -> None:
        self.select_all_checkbox.click()

    @step("PRODUCTS: TOGGLE PRODUCT BY INDEX")
    def toggle_product_by_index(self, index: int) -> None:
        self.product_checkbox_by_index(index).click()

    @step("PRODUCTS: TOGGLE PRODUCT BY ID")
    def toggle_product_by_id(self, product_id: str) -> None:
        self.product_checkbox_by_id(product_id).click()

    @step("PRODUCTS: EXPECT LOADED")
    def expect_loaded(self) -> None:
        expect(self.unique_element).to_be_visible()
        if self.accordion_root.first.is_visible():
            expect(self.accordion_root.first).to_be_visible()

    @step("PRODUCTS: IS PRODUCT RECEIVED BY NAME")
    def is_product_received_by_name(self, name: str) -> bool:
        item = self.product_item_by_name(name)
        expect(item).to_be_visible()
        row = item.locator("xpath=ancestor::*[self::div or self::li][1]")
        received_label = row.locator(".received-label").first
        if bool(received_label.is_visible()):
            return True
        checkbox = row.locator('input[type="checkbox"]').first
        if bool(checkbox.is_visible()):
            return bool(checkbox.is_checked())
        return False

    @step("PRODUCTS: IS PRODUCT RECEIVED (ID-FIRST)")
    def is_product_received(self, product_id: str, name_fallback: str | None = None) -> bool:
        checkbox = self.product_checkbox_by_id(product_id)
        if checkbox.count() > 0:
            row = checkbox.locator("xpath=ancestor::*[self::div or self::li or self::tr][1]")
            received_label = row.locator(".received-label").first
            if bool(received_label.is_visible()):
                return True
            return bool(checkbox.is_checked())
        if name_fallback:
            return self.is_product_received_by_name(name_fallback)
        return False

    def is_edit_visible(self) -> bool:
        return bool(self.edit_button.is_visible())

    def is_start_receiving_visible(self) -> bool:
        return bool(self.start_receiving_button.is_visible())

    def is_save_receiving_visible(self) -> bool:
        return bool(self.save_receiving_button.is_visible())

    def is_cancel_receiving_visible(self) -> bool:
        return bool(self.cancel_receiving_button.is_visible())

    @step("PRODUCTS: WAIT FOR RECEIVING CONTROLS")
    def wait_for_receiving_controls(self, timeout_ms: int = TIMEOUT_15_S) -> None:
        expect(self.cancel_receiving_button).to_be_visible(timeout=timeout_ms)
        expect(self.save_receiving_button).to_be_visible(timeout=timeout_ms)

    @step("PRODUCTS: WAIT FOR START RECEIVING")
    def wait_for_start_receiving(self, timeout_ms: int = TIMEOUT_15_S) -> None:
        self.unique_element.locator("#start-receiving-products, #start-receiving").first.wait_for(
            state="visible", timeout=timeout_ms
        )
