"""EntitiesStore — plain dataclass tracking created entity IDs for cleanup."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EntitiesStore:
    """Plain data container that tracks entity IDs created during a test.

    Attributes are plain :class:`set` objects so callers can mutate them
    directly::

        store.orders.add(order_id)
        store.customers.add(customer_id)
        store.products.update(product_ids)

    Usage in teardown::

        orders_service.full_delete(token)
        store.clear()
    """

    orders: set[str] = field(default_factory=set)
    customers: set[str] = field(default_factory=set)
    products: set[str] = field(default_factory=set)

    def clear(self) -> None:
        """Remove all tracked entity IDs."""
        self.orders.clear()
        self.customers.clear()
        self.products.clear()
