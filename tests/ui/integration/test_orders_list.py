"""Integration tests — Orders list table rendering and sorting.

Uses Playwright network interception (via :class:`~sales_portal_tests.mock.mock.Mock`)
to mock ``GET /api/orders?…`` and verify the table renders the mocked data
and correctly issues sorted requests when a column header is clicked.
"""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.config import api_config
from sales_portal_tests.data.sales_portal.orders.generate_order_data import generate_orders_response_data
from sales_portal_tests.data.sales_portal.orders.orders_list_integration_data import (
    ORDERS_LIST_INTEGRATION_DATA,
    OrdersListIntegrationCase,
)
from sales_portal_tests.mock.mock import Mock
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage


@allure.suite("Integration")
@allure.sub_suite("Orders List")
@pytest.mark.integration
@pytest.mark.ui
@pytest.mark.orders
@pytest.mark.regression
class TestOrdersListIntegration:
    """Integration tests — orders list table sorting with mocked responses."""

    @allure.title("Orders list renders correct rows from mocked response")  # type: ignore[misc]
    def test_orders_list_renders_mocked_data(
        self,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Mock the orders endpoint with 5 orders and assert the table renders all rows.

        No real backend call is made — :class:`~sales_portal_tests.mock.mock.Mock`
        intercepts ``GET /api/orders?…`` and returns the generated payload.
        """
        orders_data = generate_orders_response_data(orders_count=5)
        mock.orders_page(body=orders_data)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        expected_orders = orders_data["Orders"]
        assert isinstance(expected_orders, list)

        row_count = orders_list_page.table_row.count()
        assert row_count == len(expected_orders), f"Expected {len(expected_orders)} rows, got {row_count}"

        # Verify each row's order ID cell matches the mocked data
        for i, expected_order in enumerate(expected_orders):
            expected_id = str(expected_order.get("_id", ""))
            row = orders_list_page.table_row_by_index(i)
            actual_id = row.locator("td").nth(0).inner_text().strip()
            assert actual_id == expected_id, f"Row {i} order_id mismatch: {actual_id!r} != {expected_id!r}"

    @allure.title("Orders list shows 'no records' message when mocked with zero orders")  # type: ignore[misc]
    def test_orders_list_empty_mock(
        self,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Mock the orders endpoint with an empty list and assert the 'no records' row is shown.

        The frontend renders a single colspan row with 'No records created yet'
        when the orders list response contains an empty ``Orders`` array.
        """
        empty_response = {
            "Orders": [],
            "search": "",
            "IsSuccess": True,
            "ErrorMessage": None,
            "total": 0,
            "page": 1,
            "limit": 10,
            "status": [],
            "sorting": {"sortField": "createdOn", "sortOrder": "desc"},
        }
        # Register mock BEFORE opening the page so the interceptor is active
        mock.orders_page(body=empty_response)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        # The frontend renders exactly one row: the "No records created yet" message
        assert orders_list_page.table_row.count() == 1
        empty_row_text = orders_list_page.table_row.first.inner_text().strip()
        assert (
            "No records" in empty_row_text
        ), f"Expected 'No records' message in empty table row, got: {empty_row_text!r}"

    @allure.title("Table sorting: {case.sorting.sort_field} {case.sorting.sort_order}")  # type: ignore[misc]
    @pytest.mark.parametrize("case", ORDERS_LIST_INTEGRATION_DATA)
    def test_orders_list_table_sorting(
        self,
        case: OrdersListIntegrationCase,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        """Click a column header and assert the correct sort request is issued.

        Flow:
        1. Mock orders with opposite sort direction so the initial page load
           renders without the desired arrow.
        2. Open the orders list.
        3. Register a new mock for the expected sorted response.
        4. Click the column header and assert the outgoing request carries the
           expected ``sortField`` / ``sortOrder`` query params.
        5. Wait for the page to re-render; assert the sort arrow is visible and
           the table rows match the mocked data.
        """
        sort_field = case.sorting.sort_field
        sort_order = case.sorting.sort_order
        opposite_order = "asc" if sort_order == "desc" else "desc"

        # Initial load — opposite direction so clicking changes the sort
        initial_data = generate_orders_response_data(
            orders_count=case.orders_count,
            sorting={"sortField": sort_field, "sortOrder": opposite_order},
        )
        mock.orders_page(body=initial_data)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        # Prepare the sorted response that will be returned after the click
        sorted_data = generate_orders_response_data(
            orders_count=case.orders_count,
            sorting={"sortField": sort_field, "sortOrder": sort_order},
        )
        mock.orders_page(body=sorted_data)

        # Click the header and assert the request carries the right query params
        orders_list_page.expect_request(
            "GET",
            api_config.ORDERS,
            {"sortField": sort_field, "sortOrder": sort_order},
            orders_list_page.click_table_header,
            sort_field,
        )

        orders_list_page.wait_for_opened()

        # Assert sort arrow is visible
        expect(orders_list_page.table_header_arrow(sort_field, sort_order)).to_be_visible()

        # Assert row IDs match the mocked data (access the first cell of each row directly)
        expected_orders = sorted_data["Orders"]
        assert isinstance(expected_orders, list)
        row_count = orders_list_page.table_row.count()
        assert row_count == len(expected_orders)
        for i, expected in enumerate(expected_orders):
            actual_id = orders_list_page.table_row_by_index(i).locator("td").nth(0).inner_text().strip()
            assert actual_id == str(expected.get("_id", ""))
