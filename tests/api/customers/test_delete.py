"""API tests — DELETE /api/customers/:id (Delete Customer)."""

from __future__ import annotations

import allure
import pytest
from bson import ObjectId

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Customers")
@pytest.mark.api
@pytest.mark.customers
class TestDeleteCustomer:
    """Tests for DELETE /api/customers/:id."""

    # ------------------------------------------------------------------
    # Positive
    # ------------------------------------------------------------------

    @allure.title("Delete customer — delete existing customer (valid ID)")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_delete_existing_customer(
        self,
        customers_api: CustomersApi,
        customers_service: CustomersApiService,
        admin_token: str,
    ) -> None:
        """Create a customer, delete it (204), then verify it is gone (404)."""
        created = customers_service.create(admin_token)

        delete_response = customers_api.delete(admin_token, created.id)

        validate_response(
            delete_response,
            status=StatusCodes.DELETED,
            error_message=None,
        )

        # Verify the customer no longer exists
        get_response = customers_api.get_by_id(admin_token, created.id)
        validate_response(
            get_response,
            status=StatusCodes.NOT_FOUND,
        )

    # ------------------------------------------------------------------
    # Negative
    # ------------------------------------------------------------------

    @allure.title("Delete customer — non-existing ID returns 404")  # type: ignore[misc]
    @pytest.mark.regression
    def test_delete_non_existing_customer(
        self,
        customers_api: CustomersApi,
        admin_token: str,
    ) -> None:
        """Attempting to delete a customer that does not exist should return 404."""
        non_existing_id = str(ObjectId())

        response = customers_api.delete(admin_token, non_existing_id)

        validate_response(
            response,
            status=StatusCodes.NOT_FOUND,
            is_success=False,
        )
