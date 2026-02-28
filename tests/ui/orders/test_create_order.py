"""UI tests — Create Order via the Create Order modal."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.notifications import Notifications
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestCreateOrder:
    """UI tests for creating orders via the Create Order modal."""

    @allure.title("Create order with 1 product")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_order_with_1_product(
        self,
        orders_list_page: OrdersListPage,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a customer and 1 product via API, then create an order via UI and verify it."""
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        product = products_service.create(admin_token)
        cleanup.products.add(product.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        create_modal = orders_list_page.click_create_order_button()
        created_order = create_modal.create_order(customer.name, [product.name])
        orders_list_page.wait_for_opened()
        cleanup.orders.add(created_order.id)

        expect(orders_list_page.toast_message).to_contain_text(Notifications.ORDER_CREATED)
        assert created_order.customer.id == customer.id
        assert created_order.total_price == product.price
        assert created_order.status == OrderStatus.DRAFT

    @allure.title("Create order with 5 products")  # type: ignore[misc]
    @pytest.mark.regression
    def test_create_order_with_5_products(
        self,
        orders_list_page: OrdersListPage,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a customer and 5 products via API, then create an order via UI and verify it."""
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        products = []
        for _ in range(5):
            product = products_service.create(admin_token)
            cleanup.products.add(product.id)
            products.append(product)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        create_modal = orders_list_page.click_create_order_button()
        created_order = create_modal.create_order(customer.name, [p.name for p in products])
        orders_list_page.wait_for_opened()
        cleanup.orders.add(created_order.id)

        expect(orders_list_page.toast_message).to_contain_text(Notifications.ORDER_CREATED)
        assert created_order.customer.id == customer.id
        expected_price = sum(p.price for p in products)
        assert created_order.total_price == expected_price
        assert created_order.status == OrderStatus.DRAFT

    @allure.title("Remove product from modal before creation — total price updated")  # type: ignore[misc]
    @pytest.mark.regression
    def test_remove_product_before_creation(
        self,
        orders_list_page: OrdersListPage,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add 2 products to modal, remove the first one, verify total price and created order."""
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        products = []
        for _ in range(2):
            product = products_service.create(admin_token)
            cleanup.products.add(product.id)
            products.append(product)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        create_modal = orders_list_page.click_create_order_button()
        create_modal.wait_for_opened()
        create_modal.select_customer(customer.name)
        create_modal.select_product(0, products[0].name)
        create_modal.click_add_product_button()
        create_modal.select_product(1, products[1].name)

        total_before = float(create_modal.get_total_price())
        assert total_before == products[0].price + products[1].price

        create_modal.delete_product(0)

        total_after = float(create_modal.get_total_price())
        assert total_after == products[1].price

        # Now create (product[0] was removed, only product[1] remains selected)
        from sales_portal_tests.config import api_config
        from sales_portal_tests.data.status_codes import StatusCodes

        response = create_modal.intercept_response(api_config.ORDERS, create_modal.click_create)
        assert response.status == StatusCodes.CREATED, f"Expected 201, got {response.status}"
        orders_list_page.wait_for_opened()
        from sales_portal_tests.data.models.order import OrderFromResponse

        created_order = OrderFromResponse.model_validate(response.body.get("Order", {}))
        cleanup.orders.add(created_order.id)

        expect(orders_list_page.toast_message).to_contain_text(Notifications.ORDER_CREATED)
        assert created_order.total_price == products[1].price
        assert created_order.status == OrderStatus.DRAFT

    @allure.title("Close modal with cancel button — no order created")  # type: ignore[misc]
    @pytest.mark.regression
    def test_close_modal_with_cancel_button(
        self,
        orders_list_page: OrdersListPage,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Open create-order modal and click Cancel — no order created, no toast visible."""
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        product = products_service.create(admin_token)
        cleanup.products.add(product.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        create_modal = orders_list_page.click_create_order_button()
        create_modal.wait_for_opened()
        create_modal.select_customer(customer.name)
        create_modal.select_product(0, product.name)
        create_modal.cancel_button.click()
        create_modal.wait_for_closed()
        orders_list_page.wait_for_opened()

        expect(orders_list_page.toast_message).not_to_be_visible()
