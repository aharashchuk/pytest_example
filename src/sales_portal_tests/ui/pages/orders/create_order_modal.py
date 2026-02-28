"""CreateOrderModal — modal to create a new order."""

from __future__ import annotations

from playwright.sync_api import Locator, expect

from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import Response
from sales_portal_tests.data.models.order import OrderFromResponse
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.ui.pages.base_modal import BaseModal
from sales_portal_tests.utils.report.allure_step import step


class CreateOrderModal(BaseModal):
    @property
    def unique_element(self) -> Locator:
        return self.page.locator("#add-order-modal")

    @property
    def title(self) -> Locator:
        return self.unique_element.get_by_text("Create Order")

    @property
    def close_button(self) -> Locator:
        return self.unique_element.locator("button.btn-close")

    @property
    def select_customers_dropdown(self) -> Locator:
        return self.unique_element.locator("#inputCustomerOrder")

    @property
    def products_section(self) -> Locator:
        return self.unique_element.locator("#products-section")

    @property
    def select_products_dropdown(self) -> Locator:
        return self.products_section.locator(".form-select[name='Product']")

    @property
    def add_product_button(self) -> Locator:
        return self.unique_element.locator("#add-product-btn")

    @property
    def create_button(self) -> Locator:
        return self.unique_element.locator("#create-order-btn")

    @property
    def cancel_button(self) -> Locator:
        return self.unique_element.locator("#cancel-order-modal-btn")

    @property
    def total_price(self) -> Locator:
        return self.unique_element.locator("#total-price-order-modal")

    @step("SELECT CUSTOMER IN CREATE ORDER MODAL")
    def select_customer(self, customer_name: str) -> None:
        self.select_customers_dropdown.select_option(customer_name)

    @step("SELECT PRODUCT IN CREATE ORDER MODAL")
    def select_product(self, index: int, product_name: str) -> None:
        dropdown = self.select_products_dropdown.nth(index)
        expect(dropdown).to_be_visible()
        dropdown.select_option(product_name)

    @step("CLICK ADD PRODUCT BUTTON IN CREATE ORDER MODAL")
    def click_add_product_button(self) -> None:
        expect(self.add_product_button).to_be_visible()
        self.add_product_button.click()

    @step("DELETE PRODUCT IN CREATE ORDER MODAL")
    def delete_product(self, index: int) -> None:
        delete_button = (
            self.products_section.locator("div[data-id]").nth(index).locator('button.del-btn-modal[title="Delete"]')
        )
        delete_button.click()

    @step("GET TOTAL PRICE IN CREATE ORDER MODAL")
    def get_total_price(self) -> str:
        price = self.total_price.text_content() or ""
        return price.replace("$", "")

    @step("CLICK CREATE BUTTON IN CREATE ORDER MODAL")
    def click_create(self) -> None:
        self.create_button.click()

    @step("CREATE ORDER IN CREATE ORDER MODAL")
    def create_order(self, customer_name: str, products: list[str]) -> OrderFromResponse:
        self.wait_for_opened()
        assert 1 <= len(products) <= 5, f"Expected 1-5 products, got {len(products)}"
        self.select_customer(customer_name)
        self.select_product(0, products[0])
        for i, product in enumerate(products[1:], start=1):
            self.click_add_product_button()
            self.select_product(i, product)
        response: Response[dict[str, object]] = self.intercept_response(
            api_config.ORDERS,
            self.click_create,
        )
        assert response.status == StatusCodes.CREATED, f"Expected {StatusCodes.CREATED}, got {response.status}"
        order_data = response.body.get("Order", {})
        return OrderFromResponse.model_validate(order_data)

    @step("CLICK CANCEL BUTTON IN CREATE ORDER MODAL")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("CLICK CLOSE BUTTON IN CREATE ORDER MODAL")
    def click_close(self) -> None:
        self.close_button.click()

    @step("GET CUSTOMERS DROPDOWN VALUES IN CREATE ORDER MODAL")
    def get_customers_dropdown_texts(self) -> list[str]:
        customers_options = self.select_customers_dropdown.locator("option")
        return list(customers_options.all_text_contents())

    @step("GET PRODUCTS DROPDOWN VALUES IN CREATE ORDER MODAL")
    def get_products_dropdown_texts(self) -> list[str]:
        products_options = self.select_products_dropdown.locator("option")
        return list(products_options.all_text_contents())
