"""API tests — PUT /api/orders/:id/assign-manager and unassign-manager."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.config.env import MANAGER_IDS
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.sales_portal.orders.assign_manager_ddt import (
    ASSIGN_MANAGER_ORDER_STATUS_CASES,
    AssignManagerCase,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestAssignUnassignManager:
    """Tests for PUT /api/orders/:id/assign-manager and unassign-manager."""

    # ------------------------------------------------------------------
    # Assign manager DDT
    # ------------------------------------------------------------------

    @allure.title("Assign manager to order — {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", ASSIGN_MANAGER_ORDER_STATUS_CASES)
    def test_assign_manager(
        self,
        case: AssignManagerCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create an order in the required status and assign the first manager to it."""
        order = getattr(orders_service, case.order_factory)(admin_token, case.products_count)
        cleanup.orders.add(order.id)

        first_manager_id = MANAGER_IDS[0]
        response = orders_api.assign_manager(admin_token, order.id, first_manager_id)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        assigned_manager = body["Order"].get("assignedManager")
        assert assigned_manager is not None, "Expected assignedManager to be set"
        assert (
            assigned_manager["_id"] == first_manager_id
        ), f"Expected manager id {first_manager_id!r}, got {assigned_manager['_id']!r}"

    @allure.title("Update assigned manager to another manager")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_update_assigned_manager(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Assign the first manager, then reassign to the second (skipped if only one manager configured)."""
        if len(MANAGER_IDS) < 2:
            pytest.skip("Need at least 2 manager IDs configured to test manager reassignment")

        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        first_manager_id = MANAGER_IDS[0]
        second_manager_id = MANAGER_IDS[1]

        orders_api.assign_manager(admin_token, order.id, first_manager_id)

        response = orders_api.assign_manager(admin_token, order.id, second_manager_id)

        if response.status == StatusCodes.NOT_FOUND:
            pytest.skip(f"Second manager ID '{second_manager_id}' not found in this environment")

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict)
        assigned_manager = body["Order"].get("assignedManager")
        assert assigned_manager is not None
        assert assigned_manager["_id"] == second_manager_id

    # ------------------------------------------------------------------
    # Unassign manager
    # ------------------------------------------------------------------

    @allure.title("Unassign manager from order")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_unassign_manager(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Assign a manager then unassign; assignedManager must be null."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        first_manager_id = MANAGER_IDS[0]
        orders_api.assign_manager(admin_token, order.id, first_manager_id)

        response = orders_api.unassign_manager(admin_token, order.id)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict)
        assert (
            body["Order"]["assignedManager"] is None
        ), f"Expected assignedManager to be null after unassign, got {body['Order']['assignedManager']!r}"

    # ------------------------------------------------------------------
    # Negative — invalid order/manager IDs
    # ------------------------------------------------------------------

    @allure.title("Should NOT assign manager — non-existing order ID")  # type: ignore[misc]
    @pytest.mark.regression
    def test_assign_manager_non_existing_order(
        self,
        orders_api: OrdersApi,
        admin_token: str,
    ) -> None:
        """Assigning a manager to a non-existing order should return 404."""
        non_existing_order_id = "000000000000000000000000"
        first_manager_id = MANAGER_IDS[0]

        response = orders_api.assign_manager(admin_token, non_existing_order_id, first_manager_id)

        validate_response(
            response,
            status=StatusCodes.NOT_FOUND,
            is_success=False,
            error_message=ResponseErrors.order_not_found(non_existing_order_id),
        )

    @allure.title("Should NOT assign manager — non-existing manager ID")  # type: ignore[misc]
    @pytest.mark.regression
    def test_assign_non_existing_manager(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Assigning a non-existing manager should return 404."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        non_existing_manager_id = "000000000000000000000000"
        response = orders_api.assign_manager(admin_token, order.id, non_existing_manager_id)

        validate_response(
            response,
            status=StatusCodes.NOT_FOUND,
            is_success=False,
            error_message=ResponseErrors.manager_not_found(non_existing_manager_id),
        )

    @allure.title("Should NOT unassign manager — non-existing order ID")  # type: ignore[misc]
    @pytest.mark.regression
    def test_unassign_manager_non_existing_order(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Unassigning a manager from a non-existing order should return 404."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        first_manager_id = MANAGER_IDS[0]
        orders_api.assign_manager(admin_token, order.id, first_manager_id)

        non_existing_order_id = "000000000000000000000000"
        response = orders_api.unassign_manager(admin_token, non_existing_order_id)

        validate_response(
            response,
            status=StatusCodes.NOT_FOUND,
            is_success=False,
            error_message=ResponseErrors.order_not_found(non_existing_order_id),
        )
