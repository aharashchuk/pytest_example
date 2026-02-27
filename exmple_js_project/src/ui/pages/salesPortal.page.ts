import { expect, Locator } from "@playwright/test";
import { BasePage } from "./base.page";
import { SALES_PORTAL_URL } from "config/env";
import { TIMEOUT_30_S } from "data/salesPortal/constants";
import { logStep } from "utils/report/logStep.utils.js";

export abstract class SalesPortalPage extends BasePage {
  readonly spinner = this.page.locator(".spinner-border");
  readonly toastMessage = this.page.locator(".toast-body");
  abstract readonly uniqueElement: Locator;

  @logStep("WAIT FOR SALES PORTAL PAGE TO OPEN")
  async waitForOpened() {
    await expect(this.uniqueElement).toBeVisible({ timeout: TIMEOUT_30_S });
    await this.waitForSpinners();
  }

  @logStep("WAIT FOR SPINNERS TO DISAPPEAR")
  async waitForSpinners() {
    await expect(this.spinner).toHaveCount(0, { timeout: TIMEOUT_30_S });
  }

  @logStep("OPEN SALES PORTAL PAGE WITH ROUTE")
  async open(route?: string) {
    const normalizedRoute = route
      ? route
          .trim()
          // allow passing '/#/orders/123', '#/orders/123', or '/orders/123'
          .replace(/^\//, "")
      : "";
    const url = normalizedRoute ? SALES_PORTAL_URL + normalizedRoute : SALES_PORTAL_URL;
    await this.page.goto(url, { waitUntil: "domcontentloaded", timeout: TIMEOUT_30_S });
  }
}
