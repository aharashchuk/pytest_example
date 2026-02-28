"""EditProductUIService — open the edit-product form and submit changes."""

from __future__ import annotations

from playwright.sync_api import Page

from sales_portal_tests.data.models.product import Product
from sales_portal_tests.ui.pages.products.edit_product_page import EditProductPage
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage
from sales_portal_tests.utils.report.allure_step import step


class EditProductUIService:
    """High-level flows for editing an existing product via the UI.

    Composes :class:`EditProductPage` and :class:`ProductsListPage`.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.edit_product_page = EditProductPage(page)
        self.products_list_page = ProductsListPage(page)

    @step("OPEN EDIT PRODUCT PAGE")
    def open(self, product_id: str) -> None:
        """Navigate directly to the edit-product route for *product_id*.

        Args:
            product_id: MongoDB ``_id`` of the product to edit.
        """
        self.edit_product_page.open(f"#/products/{product_id}/edit")
        self.edit_product_page.wait_for_opened()

    @step("UPDATE PRODUCT VIA UI")
    def update(self, new_data: Product) -> None:
        """Fill the edit form with *new_data*, save and wait for the list page.

        Args:
            new_data: :class:`~sales_portal_tests.data.models.product.Product`
                containing the new values to write into the form.
        """
        self.edit_product_page.fill_form(new_data)
        self.edit_product_page.click_save()
        self.products_list_page.wait_for_opened()
