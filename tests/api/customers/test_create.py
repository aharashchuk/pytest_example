"""API tests — POST /api/customers (Create Customer)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.customers.create_customer_test_data import (
    CREATE_CUSTOMER_NEGATIVE_CASES,
    CREATE_CUSTOMER_POSITIVE_CASES,
    CreateCustomerCase,
)
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_data
from sales_portal_tests.data.schemas.customers.schemas import CREATE_CUSTOMER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Customers")
@pytest.mark.api
@pytest.mark.customers
class TestCreateCustomer:
    """Tests for POST /api/customers."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Create customer — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_CUSTOMER_POSITIVE_CASES)
    def test_create_customer_positive(
        self,
        case: CreateCustomerCase,
        customers_api: CustomersApi,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a valid customer and validate the response shape and body fields."""
        response = customers_api.create(admin_token, case.customer_data)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=CREATE_CUSTOMER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        created = body["Customer"]
        cleanup.customers.add(created["_id"])

        # Verify all sent fields are reflected in the created customer
        sent = (
            case.customer_data
            if isinstance(case.customer_data, dict)
            else case.customer_data.model_dump(exclude_none=True)
        )
        for key, value in sent.items():
            if key == "country":
                # Country may be stored as enum value string
                assert str(created.get(key)) == str(
                    value
                ), f"Field '{key}': expected {value!r}, got {created.get(key)!r}"
            else:
                assert created.get(key) == value, f"Field '{key}': expected {value!r}, got {created.get(key)!r}"

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT create customer — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_CUSTOMER_NEGATIVE_CASES)
    def test_create_customer_negative(
        self,
        case: CreateCustomerCase,
        customers_api: CustomersApi,
        admin_token: str,
    ) -> None:
        """Attempt to create an invalid customer; expect an error response."""
        response = customers_api.create(admin_token, case.customer_data)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )

    # ------------------------------------------------------------------
    # Duplicate email conflict
    # ------------------------------------------------------------------

    @allure.title("Should NOT create customer with existing email")  # type: ignore[misc]
    @pytest.mark.regression
    def test_create_customer_with_duplicate_email_returns_conflict(
        self,
        customers_api: CustomersApi,
        customers_service: CustomersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Creating a customer with an email already in the system must return 409 Conflict."""
        original = generate_customer_data()
        create_response = customers_api.create(admin_token, original)
        validate_response(create_response, status=StatusCodes.CREATED, is_success=True, error_message=None)
        body = create_response.body
        assert isinstance(body, dict)
        cleanup.customers.add(body["Customer"]["_id"])

        # Attempt to create another customer with the same email
        duplicate = generate_customer_data(email=original.email)
        dup_response = customers_api.create(admin_token, duplicate)

        validate_response(
            dup_response,
            status=StatusCodes.CONFLICT,
            is_success=False,
            error_message=None,
        )
