"""ScheduleDeliveryPage — form to schedule or edit delivery."""

from __future__ import annotations

import random

from playwright.sync_api import Locator

from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class ScheduleDeliveryPage(SalesPortalPage):
    @property
    def container(self) -> Locator:
        return self.page.locator("#delivery-container")

    @property
    def title(self) -> Locator:
        return self.container.locator("h2.fw-bold")

    @property
    def unique_element(self) -> Locator:
        return self.container

    @property
    def delivery_type_select(self) -> Locator:
        return self.container.locator("#inputType")

    @property
    def location_select(self) -> Locator:
        return self.container.locator("#inputLocation")

    @property
    def date_input(self) -> Locator:
        return self.container.locator("#date-input")

    @property
    def country_field(self) -> Locator:
        return self.container.get_by_label("Country")

    @property
    def city_input(self) -> Locator:
        return self.container.locator("#inputCity")

    @property
    def street_input(self) -> Locator:
        return self.container.locator("#inputStreet")

    @property
    def house_input(self) -> Locator:
        return self.container.locator("#inputHouse")

    @property
    def flat_input(self) -> Locator:
        return self.container.locator("#inputFlat")

    @property
    def save_button(self) -> Locator:
        return self.container.locator("#save-delivery")

    @property
    def cancel_button(self) -> Locator:
        return self.container.locator("#back-to-order-details-page")

    @property
    def active_days_of_current_month(self) -> Locator:
        return self.page.locator(".datepicker-days td.day:not(.disabled):not(.old):not(.new)")

    def _read_field(self, field: Locator) -> str:
        tag = str(field.evaluate("el => el.tagName"))
        if tag == "SELECT":
            return str(field.locator("option:checked").inner_text()).strip()
        return str(field.input_value()).strip()

    @step("GET SCHEDULE DELIVERY DATA")
    def get_schedule_delivery_data(self) -> dict[str, object]:
        return {
            "delivery_type": self._read_field(self.delivery_type_select),
            "delivery_date": self._read_field(self.date_input),
            "country": self._read_field(self.country_field),
            "city": self._read_field(self.city_input),
            "street": self._read_field(self.street_input),
            "house": int(self._read_field(self.house_input) or "0"),
            "flat": int(self._read_field(self.flat_input) or "0"),
        }

    @step("CLICK SAVE BUTTON")
    def click_save(self) -> None:
        self.save_button.click()

    @step("CLICK CANCEL BUTTON")
    def click_cancel(self) -> None:
        self.cancel_button.click()

    @step("PICK RANDOM AVAILABLE DATE")
    def pick_random_available_date(self) -> int:
        """Click a random active day and return its ``data-date`` timestamp."""
        days = self.active_days_of_current_month
        count = days.count()
        if not count:
            raise RuntimeError("No enabled days in datepicker")
        idx = random.randint(0, count - 1)
        cell = days.nth(idx)
        ts_str = cell.get_attribute("data-date") or "0"
        cell.click()
        return int(ts_str)
