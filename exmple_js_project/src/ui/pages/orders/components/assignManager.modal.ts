import { expect } from "@playwright/test";
import { BaseModal } from "../../base.modal";
import { logStep } from "utils/report/logStep.utils.js";
import { TIMEOUT_10_S, TIMEOUT_15_S } from "data/salesPortal/constants";

export class AssignManagerModal extends BaseModal {
  readonly uniqueElement = this.page.locator(`#assign-manager-modal`);

  // Modal structure
  readonly modal = this.uniqueElement;
  readonly title = this.modal.locator("h5");
  readonly managerSearchInput = this.modal.locator("#manager-search-input");
  readonly managerList = this.modal.locator("#manager-list");
  readonly managerItems = this.managerList.locator("li.list-group-item");
  readonly saveButton = this.modal.locator("#update-manager-btn");
  readonly closeButton = this.modal.locator("button.btn-close");
  readonly cancelButton = this.modal.locator("#cancel-edit-manager-modal-btn");

  async waitForOpened() {
    await expect(this.uniqueElement).toBeVisible({ timeout: TIMEOUT_15_S });
    await expect(this.managerList).toBeVisible({ timeout: TIMEOUT_10_S });
  }

  @logStep("SEARCH MANAGER BY NAME")
  async searchManager(managerName: string) {
    await expect(this.managerSearchInput).toBeVisible({ timeout: TIMEOUT_10_S });
    await this.managerSearchInput.fill(managerName);
    await this.page.waitForTimeout(300); // Wait for filtering
  }

  async selectManager(managerName: string) {
    // Don't use searchManager first - just get all items and find by text
    // This avoids issues where search input text doesn't match displayed text exactly

    const items = await this.managerItems.all();
    for (const item of items) {
      const text = await item.innerText();
      // Check if this item contains the manager name (partial match)
      if (text.toLowerCase().includes(managerName.toLowerCase())) {
        // Click to activate (sets .active class and enables Save button)
        await item.click();
        return;
      }
    }

    // If not found, do not throw; tests will validate availability separately
  }

  @logStep("GET ALL AVAILABLE MANAGERS")
  async getAvailableManagers(): Promise<string[]> {
    // Clear search to get all managers
    await this.managerSearchInput.clear();
    await this.page.waitForTimeout(300);

    const items = await this.managerItems.all();
    const managers: string[] = [];

    for (const item of items) {
      const text = (await item.innerText()).trim();
      if (text) {
        managers.push(text);
      }
    }

    return managers;
  }

  @logStep("CLICK SAVE BUTTON ON ASSIGN MANAGER MODAL")
  async clickSave() {
    await this.saveButton.click();
  }

  @logStep("CLICK CANCEL BUTTON ON ASSIGN MANAGER MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("CLICK CLOSE BUTTON ON ASSIGN MANAGER MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  async isSaveEnabled(): Promise<boolean> {
    return !(await this.saveButton.isDisabled());
  }
}
