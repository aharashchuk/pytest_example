"""API tests — POST /api/products (Create Product)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.products.create_product_test_data import (
    CREATE_PRODUCT_NEGATIVE_CASES,
    CREATE_PRODUCT_POSITIVE_CASES,
    CreateProductCase,
)
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_data
from sales_portal_tests.data.schemas.products.schemas import CREATE_PRODUCT_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Products")
@pytest.mark.api
@pytest.mark.products
class TestCreateProduct:
    """Tests for POST /api/products."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Create product — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_PRODUCT_POSITIVE_CASES)
    def test_create_product_positive(
        self,
        case: CreateProductCase,
        products_api: ProductsApi,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a valid product and validate the response shape and body fields."""
        response = products_api.create(case.product_data, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=CREATE_PRODUCT_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        created = body["Product"]
        cleanup.products.add(created["_id"])

        # Verify all sent fields are reflected in the created product
        sent = case.product_data.model_dump(exclude_none=True)
        for key, value in sent.items():
            assert created.get(key) == value, f"Field '{key}': expected {value!r}, got {created.get(key)!r}"

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT create product — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_PRODUCT_NEGATIVE_CASES)
    def test_create_product_negative(
        self,
        case: CreateProductCase,
        products_api: ProductsApi,
        admin_token: str,
    ) -> None:
        """Attempt to create an invalid product; expect an error response."""
        response = products_api.create(case.product_data, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )

    # ------------------------------------------------------------------
    # Duplicate product
    # ------------------------------------------------------------------

    @allure.title("Should NOT create duplicate product")  # type: ignore[misc]
    @pytest.mark.regression
    def test_create_duplicate_product_returns_conflict(
        self,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Creating a product with an already-existing name must return 409 Conflict."""
        product_data = generate_product_data()

        # Create the product for the first time
        first_response = products_api.create(product_data, admin_token)
        validate_response(
            first_response,
            status=StatusCodes.CREATED,
            is_success=True,
            error_message=None,
            schema=CREATE_PRODUCT_SCHEMA,
        )
        body = first_response.body
        assert isinstance(body, dict)
        cleanup.products.add(body["Product"]["_id"])

        # Attempt to create a duplicate
        duplicate_response = products_api.create(product_data, admin_token)
        validate_response(
            duplicate_response,
            status=StatusCodes.CONFLICT,
            is_success=False,
            error_message=ResponseErrors.conflict(product_data.name),
        )
