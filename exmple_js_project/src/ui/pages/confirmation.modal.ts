import { BaseModal } from "./base.modal";
import { logStep } from "utils/report/logStep.utils.js";

export class ConfirmationModal extends BaseModal {
  readonly uniqueElement = this.page.locator('[name="confirmation-modal"]');

  readonly title = this.uniqueElement.locator("h5");
  readonly confirmButton = this.uniqueElement.locator("button[type='submit']");
  readonly cancelButton = this.uniqueElement.locator("button.btn-secondary");
  readonly closeButton = this.uniqueElement.locator("button.btn-close");
  readonly confirmationMessage = this.uniqueElement.locator("div.modal-body p");

  @logStep("CLICK CLOSE BUTTON ON CONFIRMATION MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  @logStep("CLICK CANCEL BUTTON ON CONFIRMATION MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("CLICK CONFIRM BUTTON ON CONFIRMATION MODAL")
  async clickConfirm() {
    await this.confirmButton.click();
  }
}
