"""API tests — GET /api/customers/:id (Get Customer By ID)."""

from __future__ import annotations

import allure
import pytest
from bson import ObjectId

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.customers.get_by_id_customer_test_data import (
    GET_BY_ID_CUSTOMER_NEGATIVE_CASES,
    GET_BY_ID_CUSTOMER_POSITIVE_CASES,
)
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.schemas.customers.schemas import GET_BY_ID_CUSTOMER_SCHEMA
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Customers")
@pytest.mark.api
@pytest.mark.customers
class TestGetCustomerById:
    """Tests for GET /api/customers/:id."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Get customer by valid ID — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_BY_ID_CUSTOMER_POSITIVE_CASES)
    def test_get_customer_by_id_positive(
        self,
        case: CaseApi,
        customers_api: CustomersApi,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a customer then fetch it by ID; response fields must match the created customer."""
        created = customers_service.create(admin_token)
        cleanup.customers.add(created.id)

        response = customers_api.get_by_id(admin_token, created.id)

        validate_response(
            response,
            status=case.expected_status,
            is_success=True,
            error_message=case.expected_error_message,
            schema=GET_BY_ID_CUSTOMER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        fetched = body["Customer"]

        assert fetched["_id"] == created.id, f"Expected customer id {created.id!r}, got {fetched['_id']!r}"
        assert fetched["name"] == created.name
        assert fetched["email"] == created.email
        assert fetched["city"] == created.city

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT get customer by invalid ID — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", GET_BY_ID_CUSTOMER_NEGATIVE_CASES)
    def test_get_customer_by_id_negative(
        self,
        case: CaseApi,
        customers_api: CustomersApi,
        admin_token: str,
    ) -> None:
        """Fetching with a non-existing ID should return 404."""
        not_found_id = str(ObjectId())
        response = customers_api.get_by_id(admin_token, not_found_id)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=ResponseErrors.customer_not_found(not_found_id),
        )
