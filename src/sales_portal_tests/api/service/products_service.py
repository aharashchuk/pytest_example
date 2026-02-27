"""ProductsApiService — business-level product flows with built-in validation."""

from __future__ import annotations

from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.data.models.product import Product, ProductFromResponse
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_data
from sales_portal_tests.data.schemas.products.schemas import CREATE_PRODUCT_SCHEMA, GET_ALL_PRODUCTS_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.report.allure_step import step
from sales_portal_tests.utils.validation.validate_response import validate_response


class ProductsApiService:
    """High-level product service.

    Each method calls the corresponding :class:`~sales_portal_tests.api.api.products_api.ProductsApi`
    wrapper, validates the response with
    :func:`~sales_portal_tests.utils.validation.validate_response.validate_response`,
    and returns a typed Pydantic model parsed from the response body.

    Args:
        products_api: Low-level :class:`~sales_portal_tests.api.api.products_api.ProductsApi` wrapper.
    """

    def __init__(self, products_api: ProductsApi) -> None:
        self._products_api = products_api

    @step("CREATE PRODUCT - API")
    def create(self, token: str, product_data: Product | None = None) -> ProductFromResponse:
        """Create a product and return the created :class:`~sales_portal_tests.data.models.product.ProductFromResponse`.

        Args:
            token: Bearer auth token.
            product_data: Optional product payload.  A random one is generated when omitted.
        """
        data = product_data if product_data is not None else generate_product_data()
        response = self._products_api.create(data, token)
        validate_response(
            response,
            status=StatusCodes.CREATED,
            is_success=True,
            error_message=None,
            schema=CREATE_PRODUCT_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return ProductFromResponse.from_api(body["Product"])

    @step("UPDATE PRODUCT - API")
    def update(self, token: str, product_id: str, product_data: Product) -> ProductFromResponse:
        """Replace an existing product and return the updated model.

        Args:
            token: Bearer auth token.
            product_id: MongoDB ``_id`` of the product to update.
            product_data: New product payload.
        """
        data = generate_product_data(**product_data.model_dump(exclude_none=True))
        response = self._products_api.update(product_id, data, token)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=CREATE_PRODUCT_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return ProductFromResponse.from_api(body["Product"])

    @step("DELETE PRODUCT - API")
    def delete(self, token: str, product_id: str) -> None:
        """Delete a single product.

        Args:
            token: Bearer auth token.
            product_id: MongoDB ``_id`` of the product to delete.
        """
        response = self._products_api.delete(product_id, token)
        validate_response(response, status=StatusCodes.DELETED)

    @step("DELETE MULTIPLE PRODUCTS - API")
    def delete_products(self, token: str, product_ids: list[str]) -> None:
        """Delete a list of products one by one.

        Args:
            token: Bearer auth token.
            product_ids: List of product ``_id`` values to delete.
        """
        for product_id in product_ids:
            self.delete(token, product_id)

    @step("DELETE ALL PRODUCTS - API")
    def delete_all_products(self, token: str) -> None:
        """Fetch all products and delete each one.

        Args:
            token: Bearer auth token.
        """
        response = self._products_api.get_all(token)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ALL_PRODUCTS_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        product_ids: list[str] = [p["_id"] for p in body.get("Products", [])]
        self.delete_products(token, product_ids)

    @step("BULK CREATE PRODUCTS - API")
    def bulk_create(
        self,
        token: str,
        amount: int,
        custom_data: list[Product] | None = None,
    ) -> list[ProductFromResponse]:
        """Create *amount* products, optionally using per-item *custom_data*.

        Args:
            token: Bearer auth token.
            amount: Number of products to create.
            custom_data: Optional list of :class:`~sales_portal_tests.data.models.product.Product`
                         instances.  Index ``i`` is used for product ``i``; missing entries fall
                         back to randomly generated data.
        """
        results: list[ProductFromResponse] = []
        for i in range(amount):
            data: Product | None = None
            if custom_data and i < len(custom_data):
                data = custom_data[i]
            results.append(self.create(token, data))
        return results
