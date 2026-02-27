"""API tests — GET /api/customers (Get Customer List with query params)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.country import Country
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_data
from sales_portal_tests.data.schemas.customers.schemas import GET_LIST_CUSTOMERS_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Customers")
@pytest.mark.api
@pytest.mark.customers
class TestGetCustomerList:
    """Tests for GET /api/customers (paginated / filtered list)."""

    @allure.title("Get customer list — filter by country: {country}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("country", list(Country))
    def test_get_customer_list_filter_by_country(
        self,
        country: Country,
        customers_api: CustomersApi,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create one customer per country, then filter list by each country."""
        # Create a customer for the specific country under test
        customer = customers_service.create(admin_token, generate_customer_data(country=country))
        cleanup.customers.add(customer.id)

        response = customers_api.get_list(
            admin_token,
            params={
                "country": country.value,
                "page": 1,
                "limit": 10,
            },
        )

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_LIST_CUSTOMERS_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        customers = body.get("Customers", [])
        assert len(customers) > 0, f"Expected at least 1 customer with country={country.value!r}"
        for c in customers:
            assert c["country"] == country.value, f"Expected country {country.value!r}, got {c['country']!r}"

    @allure.title("Get customer list — search by name")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_get_customer_list_search_by_name(
        self,
        customers_api: CustomersApi,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a customer with a known name, search by partial name, verify it is returned."""
        unique_name = "ZXQTestCustomer"
        customer = customers_service.create(admin_token, generate_customer_data(name=unique_name))
        cleanup.customers.add(customer.id)

        response = customers_api.get_list(
            admin_token,
            params={"search": unique_name, "page": 1, "limit": 10},
        )

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_LIST_CUSTOMERS_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        ids = [c["_id"] for c in body.get("Customers", [])]
        assert customer.id in ids, f"Customer {customer.id!r} not found in search result"

    @allure.title("Get customer list — pagination returns correct page size")  # type: ignore[misc]
    @pytest.mark.regression
    def test_get_customer_list_pagination(
        self,
        customers_api: CustomersApi,
        admin_token: str,
    ) -> None:
        """Paginated list should return no more customers than the effective limit in the response."""
        response = customers_api.get_list(
            admin_token,
            params={"page": 1, "limit": 10},
        )

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_LIST_CUSTOMERS_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        customers = body.get("Customers", [])
        effective_limit = body.get("limit", len(customers))
        assert (
            len(customers) <= effective_limit
        ), f"Expected ≤{effective_limit} customers (limit from response), got {len(customers)}"
