"""OrdersFacadeService — raw-response facades for order setup in UI/mock tests."""

from __future__ import annotations

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.data.models.core import Response
from sales_portal_tests.data.models.delivery import DeliveryAddressModel, DeliveryInfoModel
from sales_portal_tests.data.models.order import OrderCreateBody
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryCondition
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.data.sales_portal.orders.generate_delivery_data import generate_delivery
from sales_portal_tests.utils.report.allure_step import step


def _delivery_info_model() -> DeliveryInfoModel:
    """Convert the generator dataclass to the Pydantic
    :class:`~sales_portal_tests.data.models.delivery.DeliveryInfoModel` expected by the API.
    """
    info = generate_delivery()
    return DeliveryInfoModel(
        address=DeliveryAddressModel(
            country=str(info.address.country.value),
            city=info.address.city,
            street=info.address.street,
            house=info.address.house,
            flat=info.address.flat,
        ),
        condition=DeliveryCondition(info.condition),
        finalDate=info.final_date,
    )


class OrdersFacadeService:
    """Lightweight facade that composes services and the orders API wrapper.

    Unlike :class:`~sales_portal_tests.api.service.orders_service.OrdersApiService`, this
    class returns **raw** :class:`~sales_portal_tests.data.models.core.Response` objects and
    performs no internal validation.  It is intended for UI/mock test setup where you need
    the full raw response for intercepting / asserting on a lower level.

    Args:
        orders_api: Low-level :class:`~sales_portal_tests.api.api.orders_api.OrdersApi` wrapper.
        customers_service: :class:`~sales_portal_tests.api.service.customers_service.CustomersApiService` instance.
        products_service: :class:`~sales_portal_tests.api.service.products_service.ProductsApiService` instance.
    """

    def __init__(
        self,
        orders_api: OrdersApi,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
    ) -> None:
        self._orders_api = orders_api
        self._customers_service = customers_service
        self._products_service = products_service

    @step("CREATE ORDER (FACADE) - API")
    def create(self, token: str, num_products: int) -> Response[object | None]:
        """Create a customer, *num_products* products, and an order.

        Returns the raw order creation response.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach.
        """
        customer = self._customers_service.create(token)
        payload = OrderCreateBody(customer=customer.id, products=[])
        for _ in range(num_products):
            product = self._products_service.create(token)
            payload.products.append(product.id)
        return self._orders_api.create(token, payload)

    @step("CREATE ORDER WITH DELIVERY (FACADE) - API")
    def create_order_with_delivery(self, token: str, num_products: int) -> Response[object | None]:
        """Create an order and attach a random delivery.

        Returns the raw add-delivery response.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach.
        """
        order_response = self.create(token, num_products)
        assert isinstance(order_response.body, dict)
        order_id: str = order_response.body["Order"]["_id"]
        return self._orders_api.add_delivery(token, order_id, _delivery_info_model())

    @step("CREATE ORDER IN PROCESS (FACADE) - API")
    def create_order_in_process(self, token: str, num_products: int) -> Response[object | None]:
        """Create an order with delivery and move it to *In Process* status.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach.
        """
        delivery_response = self.create_order_with_delivery(token, num_products)
        assert isinstance(delivery_response.body, dict)
        order_id: str = delivery_response.body["Order"]["_id"]
        return self._orders_api.update_status(order_id, OrderStatus.PROCESSING, token)

    @step("CREATE CANCELED ORDER (FACADE) - API")
    def create_canceled_order(self, token: str, num_products: int) -> Response[object | None]:
        """Create an order with delivery and cancel it.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach.
        """
        delivery_response = self.create_order_with_delivery(token, num_products)
        assert isinstance(delivery_response.body, dict)
        order_id: str = delivery_response.body["Order"]["_id"]
        return self._orders_api.update_status(order_id, OrderStatus.CANCELED, token)

    @step("CREATE PARTIALLY RECEIVED ORDER (FACADE) - API")
    def create_partially_received_order(self, token: str, num_products: int) -> Response[object | None]:
        """Create an order in process and receive the first product.

        Args:
            token: Bearer auth token.
            num_products: Number of products — must be ≥ 1.
        """
        process_response = self.create_order_in_process(token, num_products)
        assert isinstance(process_response.body, dict)
        order = process_response.body["Order"]
        order_id: str = order["_id"]
        first_product_id: str = order["products"][0]["_id"]
        return self._orders_api.receive_products(order_id, [first_product_id], token)

    @step("CREATE RECEIVED ORDER (FACADE) - API")
    def create_received_order(self, token: str, num_products: int) -> Response[object | None]:
        """Create an order in process and receive all products.

        Args:
            token: Bearer auth token.
            num_products: Number of products to create and attach.
        """
        process_response = self.create_order_in_process(token, num_products)
        assert isinstance(process_response.body, dict)
        order = process_response.body["Order"]
        order_id: str = order["_id"]
        all_product_ids: list[str] = [p["_id"] for p in order["products"]]
        return self._orders_api.receive_products(order_id, all_product_ids, token)
