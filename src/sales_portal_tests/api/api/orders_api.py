"""OrdersApi — endpoint wrappers for /api/orders resources."""

from __future__ import annotations

from sales_portal_tests.api.api_clients.types import ApiClient
from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import RequestOptions, Response
from sales_portal_tests.data.models.delivery import DeliveryInfoModel
from sales_portal_tests.data.models.order import OrderCreateBody, OrderUpdateBody
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.utils.report.allure_step import step

_JSON_AUTH_HEADERS = {"Content-Type": "application/json"}


def _auth_headers(token: str) -> dict[str, str]:
    return {**_JSON_AUTH_HEADERS, "Authorization": f"Bearer {token}"}


class OrdersApi:
    """Endpoint wrappers for the orders resource.

    Covers all order endpoints including delivery, status transitions, receiving
    products, manager assignment, and comments.

    Args:
        client: Any object satisfying the :class:`~sales_portal_tests.api.api_clients.types.ApiClient` protocol.
    """

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    @step("POST /api/orders")
    def create(self, token: str, payload: OrderCreateBody) -> Response[object | None]:
        """Create a new order.

        Args:
            token: Bearer auth token.
            payload: Order body containing ``customer`` and ``products`` IDs.
        """
        options = RequestOptions(
            url=api_config.ORDERS,
            method="POST",
            headers=_auth_headers(token),
            data=payload.model_dump(),
        )
        return self._client.send(options)

    @step("GET /api/orders/{id}")
    def get_by_id(self, order_id: str, token: str) -> Response[object | None]:
        """Retrieve a single order by *order_id*.

        Args:
            order_id: MongoDB ``_id`` of the order.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.order_by_id(order_id),
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("GET /api/orders")
    def get_all(
        self,
        token: str,
        params: dict[str, str | int | list[str]] | None = None,
    ) -> Response[object | None]:
        """Retrieve all orders with optional query parameters.

        Args:
            token: Bearer auth token.
            params: Optional query parameters (``page``, ``limit``, ``search``, etc.).
        """
        options = RequestOptions(
            url=api_config.ORDERS,
            method="GET",
            headers=_auth_headers(token),
            params=params,
        )
        return self._client.send(options)

    @step("PUT /api/orders/{id}")
    def update(self, token: str, order_id: str, payload: OrderUpdateBody) -> Response[object | None]:
        """Replace an existing order by *order_id*.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order to update.
            payload: Updated order fields.
        """
        options = RequestOptions(
            url=api_config.order_by_id(order_id),
            method="PUT",
            headers=_auth_headers(token),
            data=payload.model_dump(exclude_none=True),
        )
        return self._client.send(options)

    @step("DELETE /api/orders/{id}")
    def delete(self, token: str, order_id: str) -> Response[object | None]:
        """Delete an order by *order_id*.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order to delete.
        """
        options = RequestOptions(
            url=api_config.order_by_id(order_id),
            method="DELETE",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    # ------------------------------------------------------------------
    # Delivery
    # ------------------------------------------------------------------

    @step("POST /api/orders/{id}/delivery")
    def add_delivery(
        self,
        token: str,
        order_id: str,
        delivery: DeliveryInfoModel,
    ) -> Response[object | None]:
        """Attach delivery information to an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the target order.
            delivery: Delivery info payload.
        """
        options = RequestOptions(
            url=api_config.order_delivery(order_id),
            method="POST",
            headers=_auth_headers(token),
            data=delivery.model_dump(),
        )
        return self._client.send(options)

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    @step("PUT /api/orders/{id}/status")
    def update_status(
        self,
        order_id: str,
        status: OrderStatus,
        token: str,
    ) -> Response[object | None]:
        """Transition an order to a new *status*.

        Args:
            order_id: MongoDB ``_id`` of the order.
            status: Target :class:`~sales_portal_tests.data.sales_portal.order_status.OrderStatus`.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.order_status(order_id),
            method="PUT",
            headers=_auth_headers(token),
            data={"status": status.value},
        )
        return self._client.send(options)

    # ------------------------------------------------------------------
    # Receive products
    # ------------------------------------------------------------------

    @step("POST /api/orders/{id}/receive")
    def receive_products(
        self,
        order_id: str,
        product_ids: list[str],
        token: str,
    ) -> Response[object | None]:
        """Mark a subset of an order's products as received.

        Args:
            order_id: MongoDB ``_id`` of the order.
            product_ids: List of product IDs being received.
            token: Bearer auth token.
        """
        options = RequestOptions(
            url=api_config.order_receive(order_id),
            method="POST",
            headers=_auth_headers(token),
            data={"products": product_ids},
        )
        return self._client.send(options)

    # ------------------------------------------------------------------
    # Manager assignment
    # ------------------------------------------------------------------

    @step("PUT /api/orders/{order_id}/assign-manager/{manager_id}")
    def assign_manager(
        self,
        token: str,
        order_id: str,
        manager_id: str,
    ) -> Response[object | None]:
        """Assign a manager to an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            manager_id: MongoDB ``_id`` of the manager user.
        """
        options = RequestOptions(
            url=api_config.order_assign_manager(order_id, manager_id),
            method="PUT",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("PUT /api/orders/{order_id}/unassign-manager")
    def unassign_manager(self, token: str, order_id: str) -> Response[object | None]:
        """Remove the assigned manager from an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
        """
        options = RequestOptions(
            url=api_config.order_unassign_manager(order_id),
            method="PUT",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    # ------------------------------------------------------------------
    # Comments
    # ------------------------------------------------------------------

    @step("POST /api/orders/{order_id}/comments")
    def add_comment(self, token: str, order_id: str, comment: str) -> Response[object | None]:
        """Add a comment to an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            comment: Comment text.
        """
        options = RequestOptions(
            url=api_config.order_comments(order_id),
            method="POST",
            headers=_auth_headers(token),
            data={"comment": comment},
        )
        return self._client.send(options)

    @step("GET /api/orders/{order_id}/comments")
    def get_comments(self, token: str, order_id: str) -> Response[object | None]:
        """Retrieve all comments for an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
        """
        options = RequestOptions(
            url=api_config.order_comments(order_id),
            method="GET",
            headers=_auth_headers(token),
        )
        return self._client.send(options)

    @step("DELETE /api/orders/{order_id}/comments/{comment_id}")
    def delete_comment(
        self,
        token: str,
        order_id: str,
        comment_id: str,
    ) -> Response[object | None]:
        """Delete a specific comment from an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            comment_id: ``_id`` of the comment to delete.
        """
        options = RequestOptions(
            url=api_config.order_comment_by_id(order_id, comment_id),
            method="DELETE",
            headers=_auth_headers(token),
        )
        return self._client.send(options)
