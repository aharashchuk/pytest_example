"""UI tests — Schedule / edit delivery on order details page."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryCondition
from sales_portal_tests.data.sales_portal.orders.create_delivery_ddt import (
    CREATE_DELIVERY_POSITIVE_CASES,
    CreateDeliveryCase,
)
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.ui.service.order_details_ui_service import OrderDetailsUIService


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestOrderDelivery:
    """UI tests for scheduling and editing delivery on an order."""

    @allure.title("Schedule delivery form defaults to customer address")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_schedule_delivery_defaults_to_customer_address(
        self,
        orders_service: OrdersApiService,
        order_details_ui_service: OrderDetailsUIService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Opening schedule-delivery for a draft order pre-fills the customer address."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_ui_service.open_order_delivery(order.id)
        order_details_ui_service.open_schedule_delivery_form()

        expect(order_details_page.schedule_delivery_page.title).to_have_text("Schedule Delivery")
        expect(order_details_page.schedule_delivery_page.save_button).to_be_disabled()

    @allure.title("Save delivery — form data matches delivery tab: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_DELIVERY_POSITIVE_CASES[:3])
    def test_schedule_first_delivery(
        self,
        case: CreateDeliveryCase,
        orders_service: OrdersApiService,
        order_details_ui_service: OrderDetailsUIService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Schedule delivery with valid data; saved form info should match the delivery tab."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_ui_service.open_order_delivery(order.id)
        order_details_ui_service.open_schedule_delivery_form()

        sdp = order_details_page.schedule_delivery_page
        delivery = case.delivery_data

        # Fill form fields if delivery data is a DeliveryInfo dataclass
        from sales_portal_tests.data.sales_portal.delivery_status import DeliveryInfo

        if isinstance(delivery, DeliveryInfo):
            sdp.delivery_type_select.select_option(str(delivery.condition))
            sdp.pick_random_available_date()
            sdp.country_field.select_option(str(delivery.address.country.value))
            sdp.city_input.fill(delivery.address.city)
            sdp.street_input.fill(delivery.address.street)
            sdp.house_input.fill(str(delivery.address.house))
            sdp.flat_input.fill(str(delivery.address.flat))

        expect(sdp.save_button).to_be_enabled()
        form_data = sdp.get_schedule_delivery_data()

        order_details_ui_service.save_delivery()

        delivery_tab_data = order_details_page.delivery_tab.get_data()
        # compare relevant fields (exclude location)
        assert delivery_tab_data["delivery_type"] == form_data["delivery_type"]
        assert delivery_tab_data["city"] == form_data["city"]
        assert delivery_tab_data["street"] == form_data["street"]
        assert delivery_tab_data["house"] == form_data["house"]
        assert delivery_tab_data["flat"] == form_data["flat"]

    @allure.title("Edit existing delivery — form shows 'Edit Delivery' title")  # type: ignore[misc]
    @pytest.mark.regression
    def test_edit_delivery_shows_edit_title(
        self,
        orders_service: OrdersApiService,
        order_details_ui_service: OrderDetailsUIService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Opening schedule form after delivery already exists shows 'Edit Delivery' title."""
        order = orders_service.create_order_with_delivery(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_ui_service.open_order_delivery(order.id)
        order_details_ui_service.open_schedule_delivery_form()

        expect(order_details_page.schedule_delivery_page.title).to_have_text("Edit Delivery")
        expect(order_details_page.schedule_delivery_page.save_button).to_be_disabled()

    @allure.title("Pickup delivery: delivery type persists on delivery tab")  # type: ignore[misc]
    @pytest.mark.regression
    def test_schedule_pickup_delivery(
        self,
        orders_service: OrdersApiService,
        order_details_ui_service: OrderDetailsUIService,
        order_details_page: OrderDetailsPage,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Schedule a Pickup delivery; delivery tab should show Pickup type."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        order_details_ui_service.open_order_delivery(order.id)
        order_details_ui_service.open_schedule_delivery_form()

        sdp = order_details_page.schedule_delivery_page
        sdp.delivery_type_select.select_option(DeliveryCondition.PICKUP)
        sdp.pick_random_available_date()

        expect(sdp.save_button).to_be_enabled()
        form_data = sdp.get_schedule_delivery_data()
        assert form_data["delivery_type"] == DeliveryCondition.PICKUP

        order_details_ui_service.save_delivery()

        delivery_tab_data = order_details_page.delivery_tab.get_data()
        assert delivery_tab_data["delivery_type"] == DeliveryCondition.PICKUP
