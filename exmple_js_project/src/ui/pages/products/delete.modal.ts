import { SalesPortalPage } from "../salesPortal.page";
import { logStep } from "utils/report/logStep.utils.js";

export class ProductDeleteModal extends SalesPortalPage {
  readonly deleteModalContainer = this.page.locator(".modal-dialog");
  readonly title = this.deleteModalContainer.locator("h5");
  readonly closeBtn = this.deleteModalContainer.locator("button.btn-close hover-danger");
  readonly cancelBtn = this.deleteModalContainer.locator("button.btn btn-secondary");
  readonly deleteBtn = this.deleteModalContainer.locator("button[type = submit]");

  uniqueElement = this.deleteBtn;

  @logStep("CLICK CLOSE BUTTON ON PRODUCT DELETE MODAL")
  async clickClose() {
    await this.closeBtn.click();
  }

  @logStep("CLICK DELETE BUTTON ON PRODUCT DELETE MODAL")
  async clickDelete() {
    await this.deleteBtn.click();
  }

  @logStep("CLICK CANCEL BUTTON ON PRODUCT DELETE MODAL")
  async clickCancel() {
    await this.cancelBtn.click();
  }

  @logStep("WAIT FOR PRODUCT DELETE MODAL TO OPEN")
  async waitForOpened() {
    await this.uniqueElement.waitFor({ state: "visible" });
  }

  @logStep("WAIT FOR PRODUCT DELETE MODAL TO CLOSE")
  async waitForClosed() {
    await this.uniqueElement.waitFor({ state: "hidden" });
  }
}
