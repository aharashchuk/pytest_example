"""EditProductsModal — modal to edit products on an existing order."""

from __future__ import annotations

from playwright.sync_api import Locator, expect

from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.order import OrderFromResponse
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.ui.pages.base_modal import BaseModal
from sales_portal_tests.utils.report.allure_step import step


class EditProductsModal(BaseModal):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#edit-products-modal")

    @property
    def title(self) -> Locator:
        return self.unique_element.get_by_text("Edit Products")

    @property
    def close_button(self) -> Locator:
        return self.unique_element.locator("button.btn-close")

    @property
    def order_status_label(self) -> Locator:
        return self.page.locator("div:nth-child(1) > span.text-primary, div:nth-child(1) > span.text-danger")

    @property
    def products_section(self) -> Locator:
        return self.unique_element.locator("#edit-products-section")

    @property
    def product_rows(self) -> Locator:
        return self.products_section.locator("div[data-id]")

    @property
    def select_products_dropdown(self) -> Locator:
        return self.products_section.locator(".form-select[name='Product']")

    @property
    def add_product_button(self) -> Locator:
        return self.unique_element.locator("#add-product-btn")

    @property
    def cancel_edit_button(self) -> Locator:
        return self.unique_element.locator("#cancel-edit-products-modal-btn")

    @property
    def save_update_button(self) -> Locator:
        return self.unique_element.locator("#update-products-btn")

    @property
    def delete_product_button(self) -> Locator:
        return self.products_section.locator('button.del-btn-modal[title="Delete"]')

    @property
    def total_price(self) -> Locator:
        return self.unique_element.locator("#total-price-order-modal")

    @step("GET PRODUCTS COUNT IN EDIT PRODUCTS MODAL")
    def get_products_count(self) -> int:
        return int(self.product_rows.count())

    @step("SELECT PRODUCT IN EDIT PRODUCTS MODAL")
    def select_product(self, index: int, product_name: str) -> None:
        dropdown = self.select_products_dropdown.nth(index)
        expect(dropdown).to_be_visible()
        dropdown.select_option(product_name)

    @step("CLICK ADD PRODUCT BUTTON IN EDIT PRODUCTS MODAL")
    def click_add_product_button(self) -> None:
        expect(self.add_product_button).to_be_visible()
        self.add_product_button.click()

    @step("DELETE PRODUCT IN EDIT PRODUCTS MODAL")
    def delete_product(self, index: int) -> None:
        delete_button = (
            self.products_section.locator("div[data-id]").nth(index).locator('button.del-btn-modal[title="Delete"]')
        )
        delete_button.click()

    @step("CLICK SAVE BUTTON IN EDIT PRODUCTS MODAL")
    def click_save(self) -> None:
        self.save_update_button.click()

    @step("EDIT PRODUCTS IN EDIT PRODUCTS MODAL")
    def edit_order(self, products: list[str]) -> OrderFromResponse:
        self.wait_for_opened()
        assert 1 <= len(products) <= 5, f"Expected 1-5 products, got {len(products)}"
        target_count = len(products)
        current_rows_count = self.get_products_count()

        # Remove extra rows if modal currently has more
        if current_rows_count > target_count:
            for i in range(current_rows_count - 1, target_count - 1, -1):
                self.delete_product(i)

        # Select / add products
        for i, product in enumerate(products):
            if i >= current_rows_count:
                self.click_add_product_button()
            self.select_product(i, product)

        response = self.intercept_response(api_config.ORDERS, self.click_save)
        assert response.status == StatusCodes.OK, f"Expected {StatusCodes.OK}, got {response.status}"
        order_data = response.body.get("Order", {})
        return OrderFromResponse.model_validate(order_data)

    @step("CLICK CANCEL BUTTON IN EDIT PRODUCTS MODAL")
    def click_cancel(self) -> None:
        self.cancel_edit_button.click()

    @step("CLICK CLOSE BUTTON IN EDIT PRODUCTS MODAL")
    def click_close(self) -> None:
        self.close_button.click()
