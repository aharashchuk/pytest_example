import { Locator } from "@playwright/test";
import { DeliveryDateAction, DeliveryInfo } from "data/types/delivery.types";
import { logStep } from "utils/report/logStep.utils";
import { SalesPortalPage } from "ui/pages/salesPortal.page";

export class ScheduleDeliveryPage extends SalesPortalPage {
  readonly container = this.page.locator("#delivery-container");
  readonly title = this.container.locator("h2.fw-bold"); // "Schedule Delivery" | "Edit Delivery"
  readonly uniqueElement = this.container;

  // fields
  readonly deliveryTypeSelect = this.container.locator("#inputType");
  readonly locationSelect = this.container.locator("#inputLocation");
  readonly dateInput = this.container.locator("#date-input");
  readonly countryField = this.container.getByLabel("Country");
  readonly cityInput = this.container.locator("#inputCity");
  readonly streetInput = this.container.locator("#inputStreet");
  readonly houseInput = this.container.locator("#inputHouse");
  readonly flatInput = this.container.locator("#inputFlat");

  // actions
  readonly saveButton = this.container.locator("#save-delivery");
  readonly cancelButton = this.container.locator("#back-to-order-details-page");

  //calendar
  readonly activeDaysOfCurrentMonth = this.page.locator(".datepicker-days td.day:not(.disabled):not(.old):not(.new)");

  @logStep("READING STRING FIELDS")
  private async readField(field: Locator): Promise<string> {
    const tag = await field.evaluate((el) => el.tagName);
    if (tag === "SELECT") {
      return (await field.locator("option:checked").innerText()).trim();
    }
    return (await field.inputValue()).trim();
  }

  @logStep("READING NUMBER FIELDS")
  private async readNumberField(field: Locator): Promise<number> {
    const raw = await this.readField(field);
    return Number(raw);
  }

  @logStep("GET SCHEDULE DELIVERY DATA")
  async getScheduleDeliveryData(): Promise<DeliveryInfo> {
    const deliveryType = await this.readField(this.deliveryTypeSelect);

    return {
      deliveryType: deliveryType ?? "",
      deliveryDate: await this.readField(this.dateInput),
      country: await this.readField(this.countryField),
      city: await this.readField(this.cityInput),
      street: await this.readField(this.streetInput),
      house: Number(await this.readField(this.houseInput)),
      flat: Number(await this.readField(this.flatInput)),
    };
  }

  @logStep("CLICK SAVE BUTTON")
  async clickSave() {
    await this.saveButton.click();
  }

  @logStep("CLICK CANCEL BUTTON")
  async clickCancel() {
    await this.cancelButton.click();
  }

  async pickRandomAvailableDate(): Promise<Date> {
    const days = this.activeDaysOfCurrentMonth;
    const count = await days.count();
    if (!count) throw new Error("No enabled days in datepicker");
    const idx = Math.floor(Math.random() * count);
    const cell = days.nth(idx);
    const ts = Number(await cell.getAttribute("data-date"));
    await cell.click();
    return new Date(ts);
  }

  @logStep("PICK DELIVERY DATE")
  async pickDateIfNeeded(action?: DeliveryDateAction) {
    if (!action) return;
    await this.dateInput.click();
    await action(this);
  }
}
