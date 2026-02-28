"""UI tests — Export orders to CSV / JSON."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.order_status import OrderStatus
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage
from sales_portal_tests.utils.files.export_file_utils import parse_downloaded_export


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestExportOrders:
    """UI tests for exporting the orders table to CSV and JSON."""

    @allure.title("JSON export — all options selected contains order data")  # type: ignore[misc]
    @pytest.mark.regression
    def test_json_export_all_fields(
        self,
        orders_service: OrdersApiService,
        orders_list_page: OrdersListPage,
        admin_token: str,
        cleanup: EntitiesStore,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Create orders in various statuses; export to JSON with all fields selected."""
        for factory, n in [
            ("create_order_and_entities", 1),
            ("create_order_in_process", 1),
            ("create_partially_received_order", 1),
            ("create_received_order", 1),
            ("create_canceled_order", 1),
        ]:
            order = getattr(orders_service, factory)(admin_token, num_products=n)
            cleanup.orders.add(order.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()
        orders_list_page.open_export_modal()
        orders_list_page.export_modal.select_format("JSON")
        orders_list_page.export_modal.check_all_fields()

        download = orders_list_page.export_modal.download_file()
        exported = parse_downloaded_export(download, tmp_path)  # type: ignore[arg-type]

        assert exported["format"] == "json"
        data = exported["data"]
        assert isinstance(data, list)
        assert len(data) > 0
        assert isinstance(data[0], dict)

    @allure.title("CSV export — single field (Status) — only valid statuses present")  # type: ignore[misc]
    @pytest.mark.regression
    def test_csv_export_status_only(
        self,
        orders_service: OrdersApiService,
        orders_list_page: OrdersListPage,
        admin_token: str,
        cleanup: EntitiesStore,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Export orders to CSV with only the Status field; verify all statuses are valid."""
        for factory, n in [
            ("create_order_and_entities", 1),
            ("create_order_in_process", 1),
            ("create_partially_received_order", 1),
            ("create_received_order", 1),
            ("create_canceled_order", 1),
        ]:
            order = getattr(orders_service, factory)(admin_token, num_products=n)
            cleanup.orders.add(order.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()
        orders_list_page.open_export_modal()
        orders_list_page.export_modal.select_format("CSV")
        orders_list_page.export_modal.uncheck_all_fields()
        orders_list_page.export_modal.check_fields_bulk(["Status"])

        download = orders_list_page.export_modal.download_file()
        exported = parse_downloaded_export(download, tmp_path)  # type: ignore[arg-type]

        assert exported["format"] == "csv"
        records = exported["data"]
        assert isinstance(records, list)
        assert len(records) >= 1

        allowed_statuses = {s.value for s in OrderStatus} - {OrderStatus.EMPTY}
        exported_statuses = [r.get("Status") for r in records if r.get("Status")]
        assert len(exported_statuses) > 0
        for status in exported_statuses:
            assert status in allowed_statuses, f"Unexpected status in export: {status}"

    @allure.title("CSV export — default pre-selected fields")  # type: ignore[misc]
    @pytest.mark.regression
    def test_csv_export_default_fields(
        self,
        orders_service: OrdersApiService,
        orders_list_page: OrdersListPage,
        admin_token: str,
        cleanup: EntitiesStore,
        tmp_path: pytest.TempPathFactory,
    ) -> None:
        """Export with default pre-selected fields; resulting CSV should have multiple columns."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()
        orders_list_page.open_export_modal()
        orders_list_page.export_modal.select_format("CSV")
        # Do NOT change selections — use defaults

        download = orders_list_page.export_modal.download_file()
        exported = parse_downloaded_export(download, tmp_path)  # type: ignore[arg-type]

        assert exported["format"] == "csv"
        records = exported["data"]
        assert isinstance(records, list)
        assert len(records) >= 1
        # Default pre-selected columns (Status + Total Price + ...) produce at least 2 keys
        assert len(records[0].keys()) >= 2
