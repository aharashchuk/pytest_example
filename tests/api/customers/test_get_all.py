"""API tests — GET /api/customers/all (Get All Customers)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.schemas.customers.schemas import GET_ALL_CUSTOMERS_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Customers")
@pytest.mark.api
@pytest.mark.customers
class TestGetAllCustomers:
    """Tests for GET /api/customers/all."""

    @allure.title("Get all customers — returns list including newly created customers")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_all_customers_returns_created(
        self,
        customers_api: CustomersApi,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Bulk-create two customers, fetch all, and verify both appear in the list."""
        customer1 = customers_service.create(admin_token)
        customer2 = customers_service.create(admin_token)
        cleanup.customers.add(customer1.id)
        cleanup.customers.add(customer2.id)

        response = customers_api.get_all(admin_token)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ALL_CUSTOMERS_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        ids = [c["_id"] for c in body.get("Customers", [])]
        assert customer1.id in ids, f"Customer {customer1.id!r} not found in get-all response"
        assert customer2.id in ids, f"Customer {customer2.id!r} not found in get-all response"

    @allure.title("Get all customers — unauthorized request returns 401")  # type: ignore[misc]
    @pytest.mark.regression
    def test_get_all_customers_unauthorized(
        self,
        customers_api: CustomersApi,
    ) -> None:
        """Fetching all customers without a token should return 401 Unauthorized."""
        from sales_portal_tests.data.sales_portal.errors import ResponseErrors

        response = customers_api.get_all("")

        validate_response(
            response,
            status=StatusCodes.UNAUTHORIZED,
            is_success=False,
            error_message=ResponseErrors.UNAUTHORIZED,
        )
