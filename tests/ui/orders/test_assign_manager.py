"""UI tests — Assign / unassign manager on order details page."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.orders.assign_manager_ddt import (
    ASSIGN_MANAGER_ORDER_STATUS_CASES,
    AssignManagerCase,
)
from sales_portal_tests.ui.service.assign_manager_ui_service import AssignManagerUIService


def _normalize_manager_name(name: str) -> str:
    """Strip the parenthesised role qualifier, e.g. 'John Doe (admin)' → 'John Doe'."""
    return name.split("(")[0].strip()


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
@pytest.mark.managers
class TestAssignManager:
    """UI tests for assigning and unassigning managers on order details page."""

    # ------------------------------------------------------------------
    # DDT: assign to orders in different statuses
    # ------------------------------------------------------------------

    @allure.title("Assign manager — {case}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", ASSIGN_MANAGER_ORDER_STATUS_CASES)
    def test_assign_manager_ddt(
        self,
        case: AssignManagerCase,
        orders_service: OrdersApiService,
        assign_manager_ui_service: AssignManagerUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Assign the first available manager to an order in the given status; verify assignment."""
        factory = getattr(orders_service, case.order_factory)
        order = factory(admin_token, num_products=case.products_count)
        cleanup.orders.add(order.id)

        assign_manager_ui_service.open_order_for_manager_assignment(order.id)
        manager_name = assign_manager_ui_service.assign_first_available()

        assign_manager_ui_service.expect_manager_assigned(manager_name)

    # ------------------------------------------------------------------
    # Cancel assignment — no manager assigned
    # ------------------------------------------------------------------

    @allure.title("Cancel manager assignment — no manager assigned")  # type: ignore[misc]
    @pytest.mark.regression
    def test_cancel_manager_assignment(
        self,
        orders_service: OrdersApiService,
        assign_manager_ui_service: AssignManagerUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open assign-manager modal, cancel; manager remains unassigned."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        assign_manager_ui_service.open_order_for_manager_assignment(order.id)
        assign_manager_ui_service.expect_no_manager_assigned()

        assign_manager_ui_service.cancel_manager_assignment()

        assign_manager_ui_service.expect_no_manager_assigned()

    # ------------------------------------------------------------------
    # Assign manager modal shows all available managers
    # ------------------------------------------------------------------

    @allure.title("Assign manager modal lists all available managers")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_modal_lists_all_managers(
        self,
        orders_service: OrdersApiService,
        assign_manager_ui_service: AssignManagerUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open assign-manager modal; verify manager list is non-empty."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        assign_manager_ui_service.open_order_for_manager_assignment(order.id)
        managers = assign_manager_ui_service.get_available_managers()

        assert len(managers) > 0, "Expected at least one manager in the modal"
        for name in managers:
            assert len(name.strip()) > 0, "Manager name should be non-empty"

    # ------------------------------------------------------------------
    # Manager assignment persists after page refresh
    # ------------------------------------------------------------------

    @allure.title("Manager assignment persists after page refresh")  # type: ignore[misc]
    @pytest.mark.regression
    def test_manager_persists_after_refresh(
        self,
        orders_service: OrdersApiService,
        assign_manager_ui_service: AssignManagerUIService,
        page: Page,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Assign a manager, reload the page, verify the manager is still shown."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        assign_manager_ui_service.open_order_for_manager_assignment(order.id)
        manager_name = assign_manager_ui_service.assign_first_available()
        assign_manager_ui_service.expect_manager_assigned(manager_name)

        page.reload()
        assign_manager_ui_service.order_details_page.wait_for_opened()

        assign_manager_ui_service.expect_manager_assigned(manager_name)

    # ------------------------------------------------------------------
    # Unassign manager
    # ------------------------------------------------------------------

    @allure.title("Unassign manager")  # type: ignore[misc]
    @pytest.mark.regression
    def test_unassign_manager(
        self,
        orders_service: OrdersApiService,
        assign_manager_ui_service: AssignManagerUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Assign then unassign a manager; assign-trigger should be visible again."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        assign_manager_ui_service.open_order_for_manager_assignment(order.id)
        assign_manager_ui_service.assign_first_available()

        assign_manager_ui_service.unassign()

        assign_manager_ui_service.expect_no_manager_assigned()
