"""AddNewProductUIService — open the add-product form and submit it."""

from __future__ import annotations

from playwright.sync_api import Page

from sales_portal_tests.data.models.product import Product
from sales_portal_tests.ui.pages.products.add_new_product_page import AddNewProductPage
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage
from sales_portal_tests.utils.report.allure_step import step


class AddNewProductUIService:
    """High-level flows for creating a new product via the UI.

    Composes :class:`AddNewProductPage` and :class:`ProductsListPage`.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.add_new_product_page = AddNewProductPage(page)
        self.products_list_page = ProductsListPage(page)

    @step("OPEN ADD NEW PRODUCT PAGE")
    def open(self) -> None:
        """Navigate directly to the add-new-product route."""
        self.add_new_product_page.open("#/products/add")
        self.add_new_product_page.wait_for_opened()

    @step("CREATE NEW PRODUCT VIA UI")
    def create(self, product_data: Product) -> None:
        """Fill the form with *product_data*, save and wait for the list page.

        Args:
            product_data: The :class:`~sales_portal_tests.data.models.product.Product`
                instance whose fields are used to populate the form.
        """
        self.add_new_product_page.fill_form(product_data)
        self.add_new_product_page.click_save()
        self.products_list_page.wait_for_opened()
