"""API tests — POST /api/orders/:id/delivery (Add Delivery)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.config import api_config
from sales_portal_tests.data.models.core import RequestOptions
from sales_portal_tests.data.sales_portal.delivery_status import DeliveryInfo
from sales_portal_tests.data.sales_portal.orders.create_delivery_ddt import (
    CREATE_DELIVERY_NEGATIVE_CASES,
    CREATE_DELIVERY_POSITIVE_CASES,
    CreateDeliveryCase,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.utils.validation.validate_response import validate_response


def _to_api_payload(delivery_data: DeliveryInfo | dict[str, object]) -> dict[str, object]:
    """Convert a ``DeliveryInfo`` dataclass or raw dict into a JSON-serialisable dict."""
    if isinstance(delivery_data, dict):
        # Ensure enum values are serialised to strings
        raw: dict[str, object] = delivery_data.copy()
        addr = raw.get("address")
        if isinstance(addr, dict):
            country = addr.get("country")
            raw["address"] = {
                **addr,
                "country": country.value if hasattr(country, "value") else country,  # type: ignore[union-attr]
            }
        condition = raw.get("condition")
        if hasattr(condition, "value"):
            raw["condition"] = condition.value
        return raw
    # DeliveryInfo dataclass
    return {
        "address": {
            "country": str(delivery_data.address.country.value),
            "city": delivery_data.address.city,
            "street": delivery_data.address.street,
            "house": delivery_data.address.house,
            "flat": delivery_data.address.flat,
        },
        "condition": str(delivery_data.condition),
        "finalDate": delivery_data.final_date,
    }


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestAddDelivery:
    """Tests for POST /api/orders/:id/delivery."""

    # ------------------------------------------------------------------
    # Positive DDT
    # ------------------------------------------------------------------

    @allure.title("Add delivery — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_DELIVERY_POSITIVE_CASES)
    def test_add_delivery_positive(
        self,
        case: CreateDeliveryCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create a draft order then attach valid delivery info; expect 200 with order schema."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        payload_dict = _to_api_payload(case.delivery_data)

        options = RequestOptions(
            url=api_config.order_delivery(order.id),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {admin_token}",
            },
            data=payload_dict,
        )
        response = orders_api._client.send(options)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=GET_ORDER_SCHEMA,
        )

    # ------------------------------------------------------------------
    # Negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT add delivery — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_DELIVERY_NEGATIVE_CASES)
    def test_add_delivery_negative(
        self,
        case: CreateDeliveryCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attach invalid delivery info to an order; expect the specified error response."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        payload_dict = _to_api_payload(case.delivery_data)

        options = RequestOptions(
            url=api_config.order_delivery(order.id),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {admin_token}",
            },
            data=payload_dict,
        )
        response = orders_api._client.send(options)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
