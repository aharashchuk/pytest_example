import { logStep } from "utils/report/logStep.utils";
import { DeliveryInfo } from "data/types/delivery.types";
import { SalesPortalPage } from "ui/pages/salesPortal.page";

export class DeliveryTab extends SalesPortalPage {
  readonly tab = this.page.locator('#delivery.tab-pane.active.show[role="tabpanel"]');
  readonly title = this.tab.locator("h4", { hasText: "Delivery Information" });
  readonly scheduleDeliveryButton = this.tab.locator("#delivery-btn");
  readonly uniqueElement = this.tab;

  //delivery info
  readonly orderInfoTable = this.tab.locator("div.mb-4.p-3");
  readonly rows = this.orderInfoTable.locator("div.c-details");
  readonly labelCells = this.rows.locator("span:first-child");
  readonly valueCells = this.rows.locator("span:last-child");

  @logStep("GET ALL DATA FROM DELIVERY INFO")
  async getData(): Promise<DeliveryInfo> {
    const [fieldLabels, fieldValues] = await Promise.all([
      this.labelCells.allInnerTexts(),
      this.valueCells.allInnerTexts(),
    ]);

    const labelToValueMap = fieldLabels.reduce<Record<string, string>>((result, rawLabel, index) => {
      const label = rawLabel?.trim();
      if (!label) return result;
      const value = (fieldValues[index] ?? "").trim();
      result[label] = value;
      return result;
    }, {});
    const text = (label: string) => (labelToValueMap[label] ?? "").trim();
    const num = (label: string) => Number(text(label));
    return {
      deliveryType: text("Delivery Type"),
      deliveryDate: text("Delivery Date"),
      country: text("Country"),
      city: text("City"),
      street: text("Street"),
      house: num("House"),
      flat: num("Flat"),
    };
  }

  @logStep("OPEN DELIVERY FORM")
  async clickDeliveryForm() {
    await this.scheduleDeliveryButton.click();
  }
}
