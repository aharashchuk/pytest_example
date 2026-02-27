"""API tests — DELETE /api/products/:id (Delete Product)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.products.delete_product_test_data import (
    DELETE_PRODUCT_NEGATIVE_CASES,
    DELETE_PRODUCT_POSITIVE_CASES,
    DeleteProductCase,
)
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Products")
@pytest.mark.api
@pytest.mark.products
class TestDeleteProduct:
    """Tests for DELETE /api/products/:id."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Delete product — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", DELETE_PRODUCT_POSITIVE_CASES)
    def test_delete_product_positive(
        self,
        case: CaseApi,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
    ) -> None:
        """Create a product, delete it (204), then verify it is gone (404)."""
        created = products_service.create(admin_token)

        delete_response = products_api.delete(created.id, admin_token)

        validate_response(
            delete_response,
            status=case.expected_status,
            error_message=case.expected_error_message,
        )

        # Verify the product no longer exists
        get_response = products_api.get_by_id(created.id, admin_token)
        validate_response(
            get_response,
            status=StatusCodes.NOT_FOUND,
        )

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT delete product — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", DELETE_PRODUCT_NEGATIVE_CASES)
    def test_delete_product_negative(
        self,
        case: DeleteProductCase,
        products_api: ProductsApi,
        admin_token: str,
    ) -> None:
        """Attempt to delete with an invalid/non-existing ID; expect an error response."""
        response = products_api.delete(case.product_id, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
