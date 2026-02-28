"""ProductsListUIService — search, delete and navigate from the products list."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from sales_portal_tests.ui.pages.products.add_new_product_page import AddNewProductPage
from sales_portal_tests.ui.pages.products.edit_product_page import EditProductPage
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage
from sales_portal_tests.utils.report.allure_step import step


class ProductsListUIService:
    """High-level flows for the products list page.

    Composes :class:`ProductsListPage`, :class:`AddNewProductPage` and
    :class:`EditProductPage`.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.products_list_page = ProductsListPage(page)
        self.add_new_product_page = AddNewProductPage(page)
        self.edit_product_page = EditProductPage(page)

    @step("OPEN PRODUCTS LIST PAGE")
    def open(self) -> None:
        """Navigate directly to the products list route."""
        self.products_list_page.open("#/products")
        self.products_list_page.wait_for_opened()

    @step("OPEN ADD NEW PRODUCT PAGE FROM LIST")
    def open_add_new_product_page(self) -> None:
        """Click the Add New Product button and wait for the form page."""
        self.products_list_page.click_add_new_product()
        self.add_new_product_page.wait_for_opened()

    @step("OPEN PRODUCT DETAILS MODAL")
    def open_details(self, product_name: str) -> None:
        """Click the details button for *product_name* and wait for the modal.

        Args:
            product_name: Name of the product whose details modal to open.
        """
        self.products_list_page.details_button(product_name).click()
        self.products_list_page.details_modal.wait_for_opened()

    @step("OPEN DELETE PRODUCT MODAL")
    def open_delete_modal(self, product_name: str) -> None:
        """Click the delete button for *product_name* and wait for the modal.

        Args:
            product_name: Name of the product to delete.
        """
        self.products_list_page.click_action(product_name, "delete")
        self.products_list_page.delete_modal.wait_for_opened()

    @step("DELETE PRODUCT VIA UI")
    def delete(self, product_name: str) -> None:
        """Delete *product_name*: click delete → confirm → wait for modal close.

        Args:
            product_name: Name of the product to delete.
        """
        self.products_list_page.click_action(product_name, "delete")
        self.products_list_page.delete_modal.wait_for_opened()
        self.products_list_page.delete_modal.click_confirm()
        self.products_list_page.delete_modal.wait_for_closed()

    @step("SEARCH PRODUCT ON PRODUCTS LIST PAGE")
    def search(self, text: str) -> None:
        """Fill the search box with *text* and submit.

        Args:
            text: The search string to enter.
        """
        self.products_list_page.fill_search_input(text)
        self.products_list_page.click_search()
        self.products_list_page.wait_for_opened()

    @step("ASSERT PRODUCT IS VISIBLE IN TABLE")
    def assert_product_visible(self, product_name: str, *, visible: bool = True) -> None:
        """Assert that *product_name* is (or is not) visible in the table.

        Args:
            product_name: Name of the product row to check.
            visible: ``True`` (default) to assert presence; ``False`` to assert absence.
        """
        expect(self.products_list_page.table_row_by_name(product_name)).to_be_visible(visible=visible)
