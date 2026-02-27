"""OrdersApiService — business-level order flows with built-in validation."""

from __future__ import annotations

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.config.env import MANAGER_IDS
from sales_portal_tests.data.models.delivery import DeliveryAddressModel, DeliveryInfoModel
from sales_portal_tests.data.models.order import OrderCreateBody, OrderFromResponse, OrderUpdateBody
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.sales_portal.orders.generate_delivery_data import generate_delivery
from sales_portal_tests.data.schemas.orders.schemas import CREATE_ORDER_SCHEMA, GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.report.allure_step import step
from sales_portal_tests.utils.validation.validate_response import validate_response


def _delivery_info_model() -> DeliveryInfoModel:
    """Generate a :class:`~sales_portal_tests.data.models.delivery.DeliveryInfoModel`
    from the generator that returns the dataclass variant."""
    info = generate_delivery()
    return DeliveryInfoModel(
        address=DeliveryAddressModel(
            country=str(info.address.country.value),
            city=info.address.city,
            street=info.address.street,
            house=info.address.house,
            flat=info.address.flat,
        ),
        condition=info.condition,
        finalDate=info.final_date,
    )


def _parse_order(body: object) -> OrderFromResponse:
    assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
    return OrderFromResponse.model_validate(body["Order"])


class OrdersApiService:
    """High-level orders service.

    Provides order creation helpers (with customer/product provisioning),
    status-transition flows, cleanup, and comment/manager helpers.

    Args:
        orders_api: Low-level :class:`~sales_portal_tests.api.api.orders_api.OrdersApi` wrapper.
        products_service: :class:`~sales_portal_tests.api.service.products_service.ProductsApiService` instance.
        customers_service: :class:`~sales_portal_tests.api.service.customers_service.CustomersApiService` instance.
        entities_store: Optional :class:`~sales_portal_tests.api.service.stores.entities_store.EntitiesStore`
                        for tracking created entities for cleanup.
    """

    def __init__(
        self,
        orders_api: OrdersApi,
        products_service: ProductsApiService,
        customers_service: CustomersApiService,
        entities_store: EntitiesStore | None = None,
    ) -> None:
        self._orders_api = orders_api
        self._products_service = products_service
        self._customers_service = customers_service
        self.entities_store: EntitiesStore = entities_store if entities_store is not None else EntitiesStore()

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------

    @step("CREATE ORDER - API")
    def create(self, token: str, customer_id: str, product_ids: list[str]) -> OrderFromResponse:
        """Create an order for *customer_id* with the given *product_ids*.

        Args:
            token: Bearer auth token.
            customer_id: MongoDB ``_id`` of the customer.
            product_ids: MongoDB ``_id`` values of products to include.
        """
        payload = OrderCreateBody(customer=customer_id, products=product_ids)
        response = self._orders_api.create(token, payload)
        validate_response(
            response,
            status=StatusCodes.CREATED,
            is_success=True,
            error_message=None,
            schema=CREATE_ORDER_SCHEMA,
        )
        return _parse_order(response.body)

    @step("DELETE ORDER - API")
    def delete(self, token: str, order_id: str) -> None:
        """Delete a single order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order to delete.
        """
        response = self._orders_api.delete(token, order_id)
        validate_response(response, status=StatusCodes.DELETED)

    @step("UPDATE ORDER - API")
    def update(self, token: str, order_id: str, payload: OrderUpdateBody) -> OrderFromResponse:
        """Update order fields.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            payload: Updated order fields.
        """
        response = self._orders_api.update(token, order_id, payload)
        validate_response(response, status=StatusCodes.OK, is_success=True, error_message=None)
        return _parse_order(response.body)

    @step("UPDATE ORDER STATUS - API")
    def update_status(self, token: str, order_id: str, status: OrderStatus) -> OrderFromResponse:
        """Transition an order to a new *status*.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            status: Target :class:`~sales_portal_tests.data.sales_portal.order_status.OrderStatus`.
        """
        response = self._orders_api.update_status(order_id, status, token)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )
        return _parse_order(response.body)

    # ------------------------------------------------------------------
    # Composite creation helpers
    # ------------------------------------------------------------------

    @step("CREATE ORDER AND ENTITIES - API")
    def create_order_and_entities(self, token: str, num_products: int) -> OrderFromResponse:
        """Create a customer, *num_products* products, and an order linking them.

        All created entity IDs are tracked in :attr:`entities_store` for cleanup.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach to the order.
        """
        customer = self._customers_service.create(token)
        self.entities_store.customers.add(customer.id)

        product_ids: list[str] = []
        for _ in range(num_products):
            product = self._products_service.create(token)
            product_ids.append(product.id)
        self.entities_store.products.update(product_ids)

        order = self.create(token, customer.id, product_ids)
        self.entities_store.orders.add(order.id)
        return order

    @step("CREATE ORDER WITH DELIVERY - API")
    def create_order_with_delivery(self, token: str, num_products: int) -> OrderFromResponse:
        """Create an order (with all entities) and attach a random delivery.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach to the order.
        """
        order = self.create_order_and_entities(token, num_products)
        response = self._orders_api.add_delivery(token, order.id, _delivery_info_model())
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
        )
        return _parse_order(response.body)

    @step("CREATE ORDER IN PROCESS - API")
    def create_order_in_process(self, token: str, num_products: int) -> OrderFromResponse:
        """Create an order with delivery and move it to *In Process* status.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach to the order.
        """
        order = self.create_order_with_delivery(token, num_products)
        return self.update_status(token, order.id, OrderStatus.PROCESSING)

    @step("CREATE CANCELED ORDER - API")
    def create_canceled_order(self, token: str, num_products: int) -> OrderFromResponse:
        """Create an order with delivery and cancel it.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach to the order.
        """
        order = self.create_order_with_delivery(token, num_products)
        return self.update_status(token, order.id, OrderStatus.CANCELED)

    @step("CREATE PARTIALLY RECEIVED ORDER - API")
    def create_partially_received_order(self, token: str, num_products: int) -> OrderFromResponse:
        """Create an order in process and receive only the first product.

        Args:
            token: Bearer auth token.
            num_products: Number of products — must be at least 2 for a partial receive to be
                          meaningful (first product received, rest pending).
        """
        order = self.create_order_in_process(token, num_products)
        assert order.products, "Order must have at least one product to partially receive"
        first_product_id = order.products[0].id
        response = self._orders_api.receive_products(order.id, [first_product_id], token)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )
        return _parse_order(response.body)

    @step("CREATE RECEIVED ORDER - API")
    def create_received_order(self, token: str, num_products: int) -> OrderFromResponse:
        """Create an order in process and receive all products.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach to the order.
        """
        order = self.create_order_in_process(token, num_products)
        product_ids = [p.id for p in order.products]
        response = self._orders_api.receive_products(order.id, product_ids, token)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )
        return _parse_order(response.body)

    @step("CREATE ORDER IN SPECIFIC STATUS - API")
    def create_order_in_status(
        self,
        token: str,
        num_products: int,
        status: OrderStatus,
        manager_id: str | None = None,
    ) -> OrderFromResponse:
        """Create an order and drive it to the requested *status*.

        For statuses that require a manager assignment (PROCESSING, PARTIALLY_RECEIVED,
        RECEIVED), a manager is assigned first.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create.
            status: Desired target :class:`~sales_portal_tests.data.sales_portal.order_status.OrderStatus`.
            manager_id: Optional manager ID.  Defaults to the first entry in ``MANAGER_IDS``.
        """
        order = self.create_order_with_delivery(token, num_products)
        mgr = manager_id or (MANAGER_IDS[0] if MANAGER_IDS else "")
        assign_response = self._orders_api.assign_manager(token, order.id, mgr)
        validate_response(
            assign_response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )

        if status == OrderStatus.DRAFT:
            return order

        if status == OrderStatus.CANCELED:
            return self.update_status(token, order.id, OrderStatus.CANCELED)

        if status == OrderStatus.PROCESSING:
            return self.update_status(token, order.id, OrderStatus.PROCESSING)

        if status == OrderStatus.PARTIALLY_RECEIVED:
            processing_order = self.update_status(token, order.id, OrderStatus.PROCESSING)
            assert processing_order.products, "Order must have products for partial receive"
            first_id = processing_order.products[0].id
            response = self._orders_api.receive_products(processing_order.id, [first_id], token)
            validate_response(
                response,
                status=StatusCodes.OK,
                is_success=True,
                error_message=None,
                schema=GET_ORDER_SCHEMA,
            )
            return _parse_order(response.body)

        if status == OrderStatus.RECEIVED:
            processing_order = self.update_status(token, order.id, OrderStatus.PROCESSING)
            all_ids = [p.id for p in processing_order.products]
            response = self._orders_api.receive_products(processing_order.id, all_ids, token)
            validate_response(
                response,
                status=StatusCodes.OK,
                is_success=True,
                error_message=None,
                schema=GET_ORDER_SCHEMA,
            )
            return _parse_order(response.body)

        # fallback — generic status transition
        return self.update_status(token, order.id, status)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    @step("FULL DELETE ORDERS AND ENTITIES - API")
    def full_delete(self, token: str) -> None:
        """Delete all entities tracked in :attr:`entities_store`.

        Deletes orders first, then customers, then products to respect
        referential constraints.

        Args:
            token: Bearer auth token.
        """
        for order_id in list(self.entities_store.orders):
            self.delete(token, order_id)
        for customer_id in list(self.entities_store.customers):
            self._customers_service.delete(token, customer_id)
        for product_id in list(self.entities_store.products):
            self._products_service.delete(token, product_id)

    # ------------------------------------------------------------------
    # Comments
    # ------------------------------------------------------------------

    @step("ADD COMMENT TO ORDER - API")
    def add_comment(self, token: str, order_id: str, text: str) -> OrderFromResponse:
        """Add a comment to an order and return the updated order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            text: Comment text.
        """
        response = self._orders_api.add_comment(token, order_id, text)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )
        return _parse_order(response.body)

    @step("DELETE COMMENT FROM ORDER - API")
    def delete_comment(self, token: str, order_id: str, comment_id: str) -> None:
        """Delete a comment from an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            comment_id: ``_id`` of the comment to delete.
        """
        response = self._orders_api.delete_comment(token, order_id, comment_id)
        validate_response(response, status=StatusCodes.DELETED)

    # ------------------------------------------------------------------
    # Manager assignment
    # ------------------------------------------------------------------

    @step("ASSIGN MANAGER TO ORDER - API")
    def assign_manager(self, token: str, order_id: str, manager_id: str) -> OrderFromResponse:
        """Assign a manager to an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
            manager_id: MongoDB ``_id`` of the manager user.
        """
        response = self._orders_api.assign_manager(token, order_id, manager_id)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )
        return _parse_order(response.body)

    @step("UNASSIGN MANAGER FROM ORDER - API")
    def unassign_manager(self, token: str, order_id: str) -> OrderFromResponse:
        """Remove the assigned manager from an order.

        Args:
            token: Bearer auth token.
            order_id: MongoDB ``_id`` of the order.
        """
        response = self._orders_api.unassign_manager(token, order_id)
        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
            schema=GET_ORDER_SCHEMA,
        )
        return _parse_order(response.body)
