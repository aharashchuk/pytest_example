"""API tests — GET /api/products/:id (Get Product By ID)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.products.get_product_by_id_test_data import (
    GET_PRODUCT_BY_ID_NEGATIVE_CASES,
    GET_PRODUCT_BY_ID_POSITIVE_CASES,
    GetProductByIdCase,
)
from sales_portal_tests.data.schemas.products.schemas import GET_PRODUCT_SCHEMA
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Products")
@pytest.mark.api
@pytest.mark.products
class TestGetProductById:
    """Tests for GET /api/products/:id."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Get product by valid ID — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_PRODUCT_BY_ID_POSITIVE_CASES)
    def test_get_product_by_id_positive(
        self,
        case: CaseApi,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a product then fetch it by ID; response fields must match the created product."""
        created = products_service.create(admin_token)
        cleanup.products.add(created.id)

        response = products_api.get_by_id(created.id, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=True,
            error_message=case.expected_error_message,
            schema=GET_PRODUCT_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        fetched = body["Product"]

        assert fetched["_id"] == created.id, f"Expected product id {created.id!r}, got {fetched['_id']!r}"
        assert fetched["name"] == created.name
        assert fetched["manufacturer"] == created.manufacturer
        assert fetched["price"] == created.price
        assert fetched["amount"] == created.amount

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT get product by invalid ID — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_PRODUCT_BY_ID_NEGATIVE_CASES)
    def test_get_product_by_id_negative(
        self,
        case: GetProductByIdCase,
        products_api: ProductsApi,
        admin_token: str,
    ) -> None:
        """Fetching with a bad ID should return the expected error status and message."""
        response = products_api.get_by_id(case.product_id, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success if case.expected_error_message is not None else None,
            error_message=case.expected_error_message,
        )
