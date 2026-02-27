"""DDT cases for assigning / unassigning a manager to an order."""

from __future__ import annotations

from dataclasses import dataclass

import pytest


@dataclass
class AssignManagerCase:
    """Test case for assigning a manager to an order in a given status.

    ``order_factory`` is a string key that maps to an orders-service factory
    method in the fixture (e.g. ``"create_order_and_entities"``).
    ``products_count`` is passed to the factory.
    ``is_smoke`` marks the case for the smoke test suite.
    """

    title: str
    order_factory: str
    products_count: int
    is_smoke: bool = False


ASSIGN_MANAGER_ORDER_STATUS_CASES = [
    pytest.param(
        AssignManagerCase(
            title="Assign manager to draft order",
            order_factory="create_order_and_entities",
            products_count=1,
            is_smoke=True,
        ),
        id="assign-draft",
    ),
    pytest.param(
        AssignManagerCase(
            title="Assign manager to order in processing status",
            order_factory="create_order_in_process",
            products_count=1,
        ),
        id="assign-processing",
    ),
    pytest.param(
        AssignManagerCase(
            title="Assign manager to partially received order",
            order_factory="create_partially_received_order",
            products_count=2,
        ),
        id="assign-partially-received",
    ),
    pytest.param(
        AssignManagerCase(
            title="Assign manager to received order",
            order_factory="create_received_order",
            products_count=1,
        ),
        id="assign-received",
    ),
    pytest.param(
        AssignManagerCase(
            title="Assign manager to canceled order",
            order_factory="create_canceled_order",
            products_count=1,
        ),
        id="assign-canceled",
    ),
]
