import { expect, Page } from "@playwright/test";
import { OrderDetailsPage } from "ui/pages/orders/order-details.page";
import { logStep } from "utils/report/logStep.utils";
export class OrderDetailsUIService {
  readonly orderDetailsPage: OrderDetailsPage;

  constructor(private page: Page) {
    this.orderDetailsPage = new OrderDetailsPage(page);
  }

  @logStep("NAVIGATE TO DELIVERY TAB")
  async openOrderDelivery(orderId: string) {
    await this.orderDetailsPage.openByOrderId(orderId);
    await this.orderDetailsPage.waitForOpened();
    await this.orderDetailsPage.openDeliveryTab();
    await this.orderDetailsPage.deliveryTab.waitForOpened();
    await expect(this.orderDetailsPage.deliveryTab.title).toHaveText("Delivery Information");
  }

  @logStep("NAVIGATE TO SCHEDULE DELIVERY FORM")
  async openScheduleDeliveryForm() {
    await this.orderDetailsPage.deliveryTab.clickDeliveryForm();
    await this.orderDetailsPage.scheduleDeliveryPage.waitForOpened();
    await this.orderDetailsPage.scheduleDeliveryPage.waitForSpinners();
  }

  @logStep("SAVE DELIVERY")
  async clickSaveDelivery() {
    await this.orderDetailsPage.scheduleDeliveryPage.clickSave();
    await this.orderDetailsPage.deliveryTab.waitForOpened();
  }

  @logStep("CHECK IF DELIVERY TYPE HAS DISABLED FIELDS")
  async assertDeliveryHomeLocks() {
    const schedulePage = this.orderDetailsPage.scheduleDeliveryPage;
    await schedulePage.expectLocked(schedulePage.countryField);
    await schedulePage.expectLocked(schedulePage.cityInput);
    await schedulePage.expectLocked(schedulePage.houseInput);
    await schedulePage.expectLocked(schedulePage.flatInput);
  }

  @logStep("CHECK IF PICKUP TYPE HAS DISABLED FIELDS")
  async assertPickupLocks() {
    const schedulePage = this.orderDetailsPage.scheduleDeliveryPage;

    await expect(schedulePage.locationSelect).toBeHidden();
    await expect(schedulePage.countryField).toBeEnabled();

    await schedulePage.expectLocked(schedulePage.cityInput);
    await schedulePage.expectLocked(schedulePage.streetInput);
    await schedulePage.expectLocked(schedulePage.houseInput);
  }

  @logStep("NAVIGATE TO ORDER HISTORY TAB")
  async openOrderHistory(orderId: string) {
    await this.orderDetailsPage.openByOrderId(orderId);
    await this.orderDetailsPage.waitForOpened();
    await this.orderDetailsPage.openHistoryTab();
    await this.orderDetailsPage.orderHistoryTab.waitForOpened();
  }

  @logStep("OPEN ORDER DETAILS PAGE")
  async openOrderById(orderId: string) {
    await this.orderDetailsPage.open(`#/orders/${orderId}`);
    await this.orderDetailsPage.waitForOpened();
  }
}
