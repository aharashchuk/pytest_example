import { logStep } from "utils/report/logStep.utils.js";
import { BaseModal } from "ui/pages/base.modal";

export class EditOrderCustomerModal extends BaseModal {
  readonly uniqueElement = this.page.locator("#edit-customer-modal");
  readonly selectCustomersDropdown = this.page.locator("#inputCustomerOrder");
  readonly saveButton = this.page.locator("#update-customer-btn");
  readonly cancelButton = this.page.locator("#cancel-edit-customer-modal-btn");
  readonly closeButton = this.page.locator("button.btn-close");

  @logStep("SELECT CUSTOMER IN EDIT ORDER CUSTOMER MODAL")
  async selectCustomer(customerName: string) {
    await this.selectCustomersDropdown.selectOption(customerName);
  }

  @logStep("CLICK CANCEL BUTTON IN EDIT ORDER CUSTOMER MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("CLICK SAVE BUTTON IN EDIT ORDER CUSTOMER MODAL")
  async clickSave() {
    await this.saveButton.click();
  }
  @logStep("CLICK CLOSE BUTTON IN EDIT ORDER CUSTOMER MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  @logStep("GET CUSTOMERS DROPDOWN VALUES IN EDIT ORDER CUSTOMER MODAL")
  async getCustomersDropdownTexts(): Promise<string[]> {
    const customersOptions = this.selectCustomersDropdown.locator("option");
    return customersOptions.allTextContents();
  }
}
