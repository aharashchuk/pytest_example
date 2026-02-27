import { expect } from "@playwright/test";
import { SalesPortalPage } from "./salesPortal.page";
import { TIMEOUT_10_S } from "data/salesPortal/constants";

export abstract class BaseModal extends SalesPortalPage {
  async waitForClosed() {
    await expect(this.uniqueElement).not.toBeVisible({ timeout: TIMEOUT_10_S });
  }
}
