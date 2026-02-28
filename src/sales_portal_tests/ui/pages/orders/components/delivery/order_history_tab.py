"""OrderHistoryTab — order details history tabpanel."""

from __future__ import annotations

from playwright.sync_api import Locator, expect

from sales_portal_tests.data.sales_portal.order_status import OrderHistoryActions, OrderStatus
from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class OrderHistoryTab(SalesPortalPage):
    @property
    def tab(self) -> Locator:
        return self.page.locator('#history.tab-pane.active.show[role="tabpanel"]')

    @property
    def title(self) -> Locator:
        return self.tab.locator("h4", has_text="Order History")

    @property
    def body(self) -> Locator:
        return self.tab.locator("#history-body")

    @property
    def unique_element(self) -> Locator:
        return self.tab

    @property
    def top_header_row(self) -> Locator:
        return self.tab.locator(":scope > div.his-header.py-3.fs-5")

    @property
    def headers(self) -> Locator:
        return self.top_header_row.locator("span.his-col.fw-bold")

    @property
    def event_rows(self) -> Locator:
        return self.body.locator(".accordion-header.his-header")

    def row_by_action_and_date(self, action: OrderHistoryActions, date_time: str) -> Locator:
        return self.event_rows.filter(has_text=str(action)).filter(has_text=date_time).first

    @step("GET INFO FOR SPECIFIC ACTION")
    def get_row_info_by_date_and_action(self, action: OrderHistoryActions, date_time: str) -> dict[str, str]:
        row = self.row_by_action_and_date(action, date_time)
        expect(row).to_be_visible()
        cols = row.locator("span.his-col").all_inner_texts()
        performed_by = cols[1] if len(cols) > 1 else ""
        dt = cols[2] if len(cols) > 2 else ""
        return {"action": str(action), "performed_by": performed_by, "date_time": dt}

    def _panel(self, row: Locator) -> Locator:
        return row.locator("xpath=following-sibling::div[contains(@class,'accordion-collapse')]").first

    def set_expanded(self, row: Locator, *, open: bool) -> None:
        btn = row.locator("button.accordion-button.his-action")
        panel = self._panel(row)
        expect(btn).to_be_visible()
        class_attr = btn.get_attribute("class") or ""
        is_open = "collapsed" not in class_attr
        if is_open != open:
            btn.click()
        if open:
            expect(panel).to_be_visible()
        else:
            expect(panel).to_be_hidden()

    def _read_history_changes(self, details: Locator) -> dict[str, dict[str, str]]:
        rows = details.locator("div.d-flex.justify-content-around")
        count = rows.count()
        previous: dict[str, str] = {}
        updated: dict[str, str] = {}
        for i in range(count):
            cols = rows.nth(i).locator("span.his-col")
            if cols.count() < 3:
                continue
            field = cols.nth(0).inner_text()
            prev = cols.nth(1).inner_text()
            upd = cols.nth(2).inner_text()
            if not field or (prev == "Previous" and upd == "Updated"):
                continue
            previous[field] = prev
            updated[field] = upd
        return {"previous": previous, "updated": updated}

    @step("GET ALL INFO FOR SPECIFIC ACTION")
    def get_history_changes_by_date(self, action: OrderHistoryActions, date_time: str) -> dict[str, dict[str, str]]:
        row = self.row_by_action_and_date(action, date_time)
        expect(row).to_be_visible()
        self.set_expanded(row, open=True)
        details = self._panel(row)
        expect(details).to_be_visible()
        return self._read_history_changes(details)

    @step("GET STATUS FOR SPECIFIC ACTION")
    def get_status_by_date(self, action: OrderHistoryActions, date_time: str) -> dict[str, str]:
        changes = self.get_history_changes_by_date(action, date_time)
        return {
            "previous": changes["previous"].get("Status", str(OrderStatus.EMPTY)),
            "updated": changes["updated"].get("Status", str(OrderStatus.EMPTY)),
        }
