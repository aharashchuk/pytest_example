"""API tests — GET /api/products (Get All Products)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.products.get_all_products_test_data import (
    GET_ALL_PRODUCTS_NEGATIVE_CASES,
    GET_ALL_PRODUCTS_POSITIVE_CASES,
)
from sales_portal_tests.data.schemas.products.schemas import GET_ALL_PRODUCTS_SCHEMA
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Products")
@pytest.mark.api
@pytest.mark.products
class TestGetAllProducts:
    """Tests for GET /api/products."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Get all products — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_ALL_PRODUCTS_POSITIVE_CASES)
    def test_get_all_products_positive(
        self,
        case: CaseApi,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Bulk-create two products, fetch all, and verify both appear in the list."""
        product1 = products_service.create(admin_token)
        product2 = products_service.create(admin_token)
        cleanup.products.add(product1.id)
        cleanup.products.add(product2.id)

        response = products_api.get_all(admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=True,
            error_message=case.expected_error_message,
            schema=GET_ALL_PRODUCTS_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        ids = [p["_id"] for p in body.get("Products", [])]
        assert product1.id in ids, f"Product {product1.id!r} not found in get-all response"
        assert product2.id in ids, f"Product {product2.id!r} not found in get-all response"

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT get products without auth — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_ALL_PRODUCTS_NEGATIVE_CASES)
    def test_get_all_products_negative(
        self,
        case: CaseApi,
        products_api: ProductsApi,
    ) -> None:
        """Fetching all products without a token should return 401 Unauthorized."""
        response = products_api.get_all("")

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
