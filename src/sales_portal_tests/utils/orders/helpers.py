"""Order-specific helper functions for use in tests and UI services."""

from __future__ import annotations

from sales_portal_tests.data.models.order import OrderFromResponse


def product_ids_of(order: OrderFromResponse) -> list[str]:
    """Return a list of product IDs from an order response.

    Args:
        order: A parsed ``OrderFromResponse`` model.

    Returns:
        List of product ``_id`` strings.
    """
    return [p.id for p in order.products]


def calc_total(order: OrderFromResponse) -> float:
    """Calculate the expected total price of an order by summing product prices.

    Args:
        order: A parsed ``OrderFromResponse`` model.

    Returns:
        Sum of all product prices as a float.
    """
    return sum(p.price for p in order.products)
