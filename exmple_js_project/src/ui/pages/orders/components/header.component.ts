import { expect, Page } from "@playwright/test";
import { logStep } from "utils/report/logStep.utils.js";
import { TIMEOUT_10_S, TIMEOUT_15_S, TIMEOUT_30_S } from "data/salesPortal/constants";
import { BasePage } from "../../base.page";

/**
 * Header section of Order Details page.
 * Contains order status/actions and assigned manager block.
 */
export class OrderDetailsHeader extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  // Containers
  readonly uniqueElement = this.page.locator("#order-info-container");
  readonly assignedManagerContainer = this.page.locator("#assigned-manager-container");
  readonly statusBarContainer = this.page.locator("#order-status-bar-container");
  readonly orderNumberContainer = this.page.locator("//div[./span[contains(text(), 'Order number')]]");
  readonly orderNumberText = this.orderNumberContainer.locator("//span[@class='fst-italic']");

  // Action buttons (conditionally rendered by status)
  readonly cancelButton = this.page.locator("#cancel-order");
  readonly reopenButton = this.page.locator("#reopen-order");
  readonly processButton = this.page.locator("#process-order");
  readonly refreshButton = this.page.locator("#refresh-order");

  // Assigned manager actions (use onclick attribute as stable marker in FE)
  readonly assignOrEditManager = this.assignedManagerContainer.locator('[onclick^="renderAssigneManagerModal"]');
  readonly unassignManager = this.assignedManagerContainer.locator('[onclick^="renderRemoveAssignedManagerModal"]');
  readonly assignManagerTrigger = this.assignedManagerContainer
    .locator('[onclick^="renderAssigneManagerModal"], a[href], button')
    .first();

  // Status text label living inside status bar
  readonly statusText = this.statusBarContainer.locator(
    ".status-text, span.text-primary, span.text-danger, span.text-warning, span.text-success",
  );

  @logStep("HEADER: GET ORDER STATUS TEXT")
  async getStatusText() {
    const status = this.statusText.first();
    return (await status.innerText()).trim();
  }

  @logStep("HEADER: GET ORDER NUMBER TEXT")
  async getOrderNumberText() {
    const orderNumber = this.orderNumberText;
    return (await orderNumber.innerText()).trim();
  }

  @logStep("HEADER: EXPECT ORDER STATUS")
  async expectStatus(status: string) {
    const statusLabel = this.statusText.first();
    await expect(statusLabel).toHaveText(status, { timeout: TIMEOUT_10_S });
  }

  @logStep("HEADER: CLICK CANCEL ORDER")
  async cancelOrder() {
    await this.cancelButton.click();
  }

  @logStep("HEADER: CLICK REFRESH ORDER")
  async refresh() {
    await this.refreshButton.click();
  }

  @logStep("HEADER: CLICK PROCESS ORDER")
  async processOrder() {
    // Click auto-waits for visibility/stability
    await this.processButton.click();

    // Modal is a NEW element, needs explicit wait
    const confirmationModal = this.page.locator(
      '[name="confirmation-modal"].modal.show, [name="confirmation-modal"].modal.fade.show',
    );
    await expect(confirmationModal.first()).toBeVisible({ timeout: TIMEOUT_10_S });

    // Confirm button is inside modal, auto-wait works after modal is visible
    const confirmBtn = confirmationModal
      .locator(".modal-footer button.btn-primary, .modal-footer button.btn-danger, .modal-footer button.btn-success")
      .first();
    await confirmBtn.click();

    // After confirm, FE re-renders the entire page; wait for spinners to clear and stable state
    await expect(this.page.locator(".spinner-border")).toHaveCount(0, { timeout: TIMEOUT_30_S });
    await expect(this.processButton).toBeHidden({ timeout: TIMEOUT_30_S });
    await expect(this.uniqueElement).toBeVisible({ timeout: TIMEOUT_15_S });
  }

  @logStep("HEADER: OPEN ASSIGN MANAGER MODAL")
  async openAssignManagerModal() {
    // Deterministic trigger within #assigned-manager-container (no text selectors).
    await expect(this.assignedManagerContainer).toBeVisible({ timeout: TIMEOUT_10_S });
    await this.assignManagerTrigger.click();
  }

  @logStep("HEADER: OPEN UNASSIGN MANAGER MODAL")
  async openUnassignManagerModal() {
    await this.unassignManager.first().click();
  }

  // Visibility helpers (status-dependent)
  async isCancelVisible() {
    return this.cancelButton.isVisible();
  }
  async isReopenVisible() {
    return this.reopenButton.isVisible();
  }
  async isProcessVisible() {
    return this.processButton.isVisible();
  }
  async isRefreshVisible() {
    return this.refreshButton.isVisible();
  }

  @logStep("HEADER: EXPECT STATUS TO BE VISIBLE")
  async expectStatusVisible() {
    await expect(this.statusBarContainer).toBeVisible();
  }
}
