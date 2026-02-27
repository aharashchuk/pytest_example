import { Page, expect } from "@playwright/test";
import { OrderDetailsPage } from "ui/pages/orders";
import { logStep } from "utils/report/logStep.utils.js";
import { TIMEOUT_10_S } from "data/salesPortal/constants";

export class AssignManagerUIService {
  orderDetailsPage: OrderDetailsPage;

  constructor(private page: Page) {
    this.orderDetailsPage = new OrderDetailsPage(page);
  }

  @logStep("OPEN ORDER AND NAVIGATE TO MANAGER ASSIGNMENT")
  async openOrderForManagerAssignment(orderId: string) {
    await this.orderDetailsPage.openByOrderId(orderId);
    await this.orderDetailsPage.waitForOpened();
  }

  @logStep("OPEN ASSIGN MANAGER MODAL")
  async openAssignManagerModal() {
    await this.orderDetailsPage.header.openAssignManagerModal();
    await this.orderDetailsPage.assignManagerModal.waitForOpened();
  }

  @logStep("ASSIGN MANAGER BY NAME")
  async assignManagerByName(managerName: string) {
    await this.openAssignManagerModal();
    await this.orderDetailsPage.assignManagerModal.selectManager(managerName);
    await expect(this.orderDetailsPage.assignManagerModal.saveButton).toBeEnabled({ timeout: TIMEOUT_10_S });
    await this.orderDetailsPage.assignManagerModal.clickSave();
    await this.orderDetailsPage.assignManagerModal.waitForClosed();
    await this.orderDetailsPage.waitForSpinners();
  }

  @logStep("ASSIGN FIRST AVAILABLE MANAGER")
  async assignFirstAvailableManager(): Promise<string> {
    await this.openAssignManagerModal();
    const managers = await this.orderDetailsPage.assignManagerModal.getAvailableManagers();
    await expect(managers.length).toBeGreaterThan(0);
    const managerName = managers[0]!;
    await this.orderDetailsPage.assignManagerModal.selectManager(managerName);
    await expect(this.orderDetailsPage.assignManagerModal.saveButton).toBeEnabled({ timeout: TIMEOUT_10_S });
    await this.orderDetailsPage.assignManagerModal.clickSave();
    await this.orderDetailsPage.assignManagerModal.waitForClosed();
    await this.orderDetailsPage.waitForSpinners();
    return managerName;
  }

  @logStep("GET AVAILABLE MANAGERS IN MODAL")
  async getAvailableManagers(): Promise<string[]> {
    await this.openAssignManagerModal();
    const managers = await this.orderDetailsPage.assignManagerModal.getAvailableManagers();
    await this.orderDetailsPage.assignManagerModal.clickCancel();
    await this.orderDetailsPage.assignManagerModal.waitForClosed();
    return managers;
  }

  @logStep("CANCEL MANAGER ASSIGNMENT")
  async cancelManagerAssignment() {
    await this.openAssignManagerModal();
    await this.orderDetailsPage.assignManagerModal.clickCancel();
    await this.orderDetailsPage.assignManagerModal.waitForClosed();
  }

  @logStep("VERIFY MANAGER ASSIGNED")
  async expectManagerAssigned(expectedManagerName: string) {
    // Manager info should be visible in the header's assigned manager container
    const expectedDisplayName = expectedManagerName.split("(")[0]!.trim();
    await expect(this.orderDetailsPage.header.assignedManagerContainer).toContainText(expectedDisplayName, {
      timeout: TIMEOUT_10_S,
    });
  }

  @logStep("VERIFY NO MANAGER ASSIGNED")
  async expectNoManagerAssigned() {
    // When no manager assigned, the trigger button should be available
    await expect(this.orderDetailsPage.header.assignManagerTrigger).toBeVisible({ timeout: TIMEOUT_10_S });
  }

  @logStep("UNASSIGN MANAGER")
  async unassignManager() {
    await this.orderDetailsPage.header.openUnassignManagerModal();

    // Confirmation modal should open for unassigning
    const confirmationModal = this.orderDetailsPage.confirmationModal;
    await confirmationModal.waitForOpened();
    await confirmationModal.clickConfirm();

    // Wait for modal to close and page to stabilize
    await confirmationModal.waitForClosed();
    await this.orderDetailsPage.waitForSpinners();
  }
}
