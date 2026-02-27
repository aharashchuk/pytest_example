"""CustomersApiService — business-level customer flows with built-in validation."""

from __future__ import annotations

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.data.models.customer import Customer, CustomerFromResponse, CustomerListResponse
from sales_portal_tests.data.sales_portal.customers.generate_customer_data import generate_customer_data
from sales_portal_tests.data.schemas.customers.schemas import (
    CREATE_CUSTOMER_SCHEMA,
    GET_ALL_CUSTOMERS_SCHEMA,
    GET_LIST_CUSTOMERS_SCHEMA,
    UPDATE_CUSTOMER_SCHEMA,
)
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.report.allure_step import step
from sales_portal_tests.utils.validation.validate_response import validate_response


class CustomersApiService:
    """High-level customer service.

    Each method calls the corresponding
    :class:`~sales_portal_tests.api.api.customers_api.CustomersApi` wrapper,
    validates the response, and returns a typed Pydantic model.

    Args:
        customers_api: Low-level :class:`~sales_portal_tests.api.api.customers_api.CustomersApi` wrapper.
    """

    def __init__(self, customers_api: CustomersApi) -> None:
        self._customers_api = customers_api

    @step("CREATE CUSTOMER - API")
    def create(self, token: str, customer_data: Customer | None = None) -> CustomerFromResponse:
        """Create a customer and return the created
        :class:`~sales_portal_tests.data.models.customer.CustomerFromResponse`.

        Args:
            token: Bearer auth token.
            customer_data: Optional customer payload.  A random one is generated when omitted.
        """
        data = customer_data if customer_data is not None else generate_customer_data()
        response = self._customers_api.create(token, data)
        validate_response(
            response,
            status=StatusCodes.CREATED,
            is_success=True,
            error_message=None,
            schema=CREATE_CUSTOMER_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return CustomerFromResponse.from_api(body["Customer"])

    @step("DELETE CUSTOMER - API")
    def delete(self, token: str, customer_id: str) -> None:
        """Delete a customer by ID.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer to delete.
        """
        response = self._customers_api.delete(token, customer_id)
        validate_response(response, status=StatusCodes.DELETED)

    @step("GET CUSTOMER BY ID - API")
    def get_by_id(self, token: str, customer_id: str) -> CustomerFromResponse:
        """Retrieve a single customer by ID.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer.
        """
        response = self._customers_api.get_by_id(token, customer_id)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return CustomerFromResponse.from_api(body["Customer"])

    @step("GET ALL CUSTOMERS - API")
    def get_all(self, token: str) -> list[CustomerFromResponse]:
        """Retrieve all customers without pagination.

        Args:
            token: Bearer auth token.
        """
        response = self._customers_api.get_all(token)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ALL_CUSTOMERS_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return [CustomerFromResponse.from_api(c) for c in body.get("Customers", [])]

    @step("GET LIST OF CUSTOMERS - API")
    def get_list(
        self,
        token: str,
        params: dict[str, str | int | list[str]] | None = None,
    ) -> CustomerListResponse:
        """Retrieve a paginated/filtered list of customers.

        Args:
            token: Bearer auth token.
            params: Optional query parameters (``page``, ``limit``, ``search``, etc.).
        """
        response = self._customers_api.get_list(token, params)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_LIST_CUSTOMERS_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return CustomerListResponse(
            Customers=[CustomerFromResponse.from_api(c) for c in body.get("Customers", [])],
            total=int(body.get("total", 0)),
            page=int(body.get("page", 1)),
            limit=int(body.get("limit", 10)),
            search=str(body.get("search", "")),
            IsSuccess=bool(body.get("IsSuccess", True)),
            ErrorMessage=body.get("ErrorMessage"),
        )

    @step("UPDATE CUSTOMER - API")
    def update(self, token: str, customer_id: str, customer_data: Customer) -> CustomerFromResponse:
        """Replace an existing customer and return the updated model.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer to update.
            customer_data: New customer payload.
        """
        response = self._customers_api.update(token, customer_id, customer_data)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=UPDATE_CUSTOMER_SCHEMA,
        )
        body = response.body
        assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
        return CustomerFromResponse.from_api(body["Customer"])
