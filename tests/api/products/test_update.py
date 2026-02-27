"""API tests — PUT /api/products/:id (Update Product)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.product import Product
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_data
from sales_portal_tests.data.sales_portal.products.update_product_test_data import (
    UPDATE_PRODUCT_NEGATIVE_CASES,
    UPDATE_PRODUCT_POSITIVE_CASES,
    UpdateProductCase,
)
from sales_portal_tests.data.schemas.products.schemas import CREATE_PRODUCT_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Products")
@pytest.mark.api
@pytest.mark.products
class TestUpdateProduct:
    """Tests for PUT /api/products/:id."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Update product — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", UPDATE_PRODUCT_POSITIVE_CASES)
    def test_update_product_positive(
        self,
        case: UpdateProductCase,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a product, apply partial update, validate response and updated fields."""
        created = products_service.create(admin_token)
        cleanup.products.add(created.id)

        # Merge the partial update fields on top of the created product's current data
        merged_data = Product(
            name=case.product_data.get("name", created.name),
            manufacturer=case.product_data.get("manufacturer", created.manufacturer),
            price=case.product_data.get("price", created.price),
            amount=case.product_data.get("amount", created.amount),
            notes=case.product_data.get("notes", created.notes),
        )

        response = products_api.update(created.id, merged_data, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=CREATE_PRODUCT_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        updated = body["Product"]

        # The ID must be unchanged
        assert (
            updated["_id"] == created.id
        ), f"Product ID changed after update: expected {created.id!r}, got {updated['_id']!r}"
        # Verify all updated fields are reflected
        for key, value in case.product_data.items():
            assert (
                updated.get(key) == value
            ), f"Field '{key}' after update: expected {value!r}, got {updated.get(key)!r}"

    # ------------------------------------------------------------------
    # Negative DDT — invalid payload but valid product ID
    # ------------------------------------------------------------------

    @allure.title("Should NOT update product — negative payload: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", UPDATE_PRODUCT_NEGATIVE_CASES)
    def test_update_product_negative(
        self,
        case: UpdateProductCase,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to update with an invalid ID or bad payload; expect an error response."""
        if case.product_id is None:
            # Negative payload cases: create a product to use its ID
            created = products_service.create(admin_token)
            cleanup.products.add(created.id)
            product_id = created.id
            merged_data = Product(
                name=case.product_data.get("name", created.name),
                manufacturer=case.product_data.get("manufacturer", created.manufacturer),
                price=case.product_data.get("price", created.price),
                amount=case.product_data.get("amount", created.amount),
                notes=case.product_data.get("notes", created.notes),
            )
        else:
            # Invalid-ID cases: use whatever payload makes the request valid-looking
            product_id = case.product_id
            merged_data = generate_product_data()

        response = products_api.update(product_id, merged_data, admin_token)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )

    # ------------------------------------------------------------------
    # Duplicate name conflict
    # ------------------------------------------------------------------

    @allure.title("Should NOT update product name to an already-existing name")  # type: ignore[misc]
    @pytest.mark.regression
    def test_update_product_with_duplicate_name_returns_conflict(
        self,
        products_api: ProductsApi,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Updating a product name to match another existing product must return 409 Conflict."""
        first = products_service.create(admin_token)
        second = products_service.create(admin_token)
        cleanup.products.add(first.id)
        cleanup.products.add(second.id)

        # Attempt to rename 'first' to 'second's name
        merged_data = Product(
            name=second.name,
            manufacturer=first.manufacturer,
            price=first.price,
            amount=first.amount,
            notes=first.notes if first.notes else None,
        )

        response = products_api.update(first.id, merged_data, admin_token)

        validate_response(
            response,
            status=StatusCodes.CONFLICT,
            is_success=False,
            error_message=ResponseErrors.conflict(second.name),
        )
