import { Locator } from "@playwright/test";
import { SalesPortalPage } from "./salesPortal.page";
import { logStep } from "utils/report/logStep.utils";

export type HomeModuleButton = "Products" | "Customers" | "Orders";

export class HomePage extends SalesPortalPage {
  readonly welcomeText = this.page.locator(".welcome-text");
  readonly productsButton = this.page.locator("#products-from-home");
  readonly ordersButton = this.page.locator("#orders-from-home");
  readonly customersButton = this.page.locator("#customers-from-home");

  readonly metricsContainer = this.page.locator(".row.text-center.mb-5.d-flex.justify-content-between");
  readonly ordersThisYearValue = this.metricsContainer.locator("#total-orders-container p.card-text");

  readonly totalRevenueValue = this.metricsContainer.locator("#total-revenue-container p.card-text");
  readonly newCustomersValue = this.metricsContainer.locator("#total-customers-container p.card-text");
  readonly avgOrderValue = this.metricsContainer.locator("#avg-orders-value-container p.card-text");
  readonly canceledOrdersValue = this.metricsContainer.locator("#canceled-orders-container p.card-text");

  readonly uniqueElement = this.welcomeText;

  @logStep("CLICK ON VIEW MODULE BUTTON ON HOME PAGE")
  async clickOnViewModule(module: HomeModuleButton) {
    const moduleButtons: Record<HomeModuleButton, Locator> = {
      Products: this.productsButton,
      Customers: this.customersButton,
      Orders: this.ordersButton,
    };

    await moduleButtons[module].click();
  }
}
