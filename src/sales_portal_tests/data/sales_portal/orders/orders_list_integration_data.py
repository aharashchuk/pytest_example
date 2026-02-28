"""Integration test data for the orders list page (table sorting tests).

Translated from the TypeScript ``ordersListIntegrationData.ts``.

Each case drives a parametrised test that:
1. Mocks the orders endpoint with generated data.
2. Clicks a column header to sort.
3. Asserts the table rows match the mocked order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pytest

SortField = Literal["createdOn", "price", "status", "assignedManager", "_id", "email", "delivery"]
SortOrder = Literal["asc", "desc"]


@dataclass
class OrdersSorting:
    sort_field: SortField
    sort_order: SortOrder


@dataclass
class OrdersListIntegrationCase:
    title: str
    orders_count: int
    sorting: OrdersSorting


ORDERS_LIST_INTEGRATION_DATA = [
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Created On descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="createdOn", sort_order="desc"),
        ),
        id="created-on-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Created On ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="createdOn", sort_order="asc"),
        ),
        id="created-on-asc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Price descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="price", sort_order="desc"),
        ),
        id="price-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Price ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="price", sort_order="asc"),
        ),
        id="price-asc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Status descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="status", sort_order="desc"),
        ),
        id="status-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Status ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="status", sort_order="asc"),
        ),
        id="status-asc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Assigned Manager descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="assignedManager", sort_order="desc"),
        ),
        id="assigned-manager-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Assigned Manager ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="assignedManager", sort_order="asc"),
        ),
        id="assigned-manager-asc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Order Number descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="_id", sort_order="desc"),
        ),
        id="order-number-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Order Number ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="_id", sort_order="asc"),
        ),
        id="order-number-asc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Email descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="email", sort_order="desc"),
        ),
        id="email-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Email ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="email", sort_order="asc"),
        ),
        id="email-asc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Delivery descending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="delivery", sort_order="desc"),
        ),
        id="delivery-desc",
    ),
    pytest.param(
        OrdersListIntegrationCase(
            title="Sorting by Delivery ascending",
            orders_count=5,
            sorting=OrdersSorting(sort_field="delivery", sort_order="asc"),
        ),
        id="delivery-asc",
    ),
]
