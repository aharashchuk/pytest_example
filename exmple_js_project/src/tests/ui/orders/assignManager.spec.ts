import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import { ASSIGN_MANAGER_ORDER_STATUS_CASES } from "data/salesPortal/orders/assignManagerDDT";

test.describe("[UI][Orders][Assign Manager]", () => {
  const waitTimeout = 15_000;
  const normalizeManagerName = (managerName: string) => managerName.split("(")[0]!.trim();

  async function openAssignManagerModalWithWait(assignManagerUIService: any) {
    const { orderDetailsPage } = assignManagerUIService;
    const { header, assignManagerModal } = orderDetailsPage;
    const trigger = header.assignOrEditManager.first();
    await expect(header.assignedManagerContainer).toBeVisible({ timeout: waitTimeout });
    await expect(trigger).toBeVisible({ timeout: waitTimeout });
    await trigger.scrollIntoViewIfNeeded();
    await trigger.click();
    await assignManagerModal.waitForOpened();
  }

  async function getFirstTwoManagerNames(assignManagerUIService: any): Promise<[string, string]> {
    await openAssignManagerModalWithWait(assignManagerUIService);
    const managers: string[] = await assignManagerUIService.orderDetailsPage.assignManagerModal.getAvailableManagers();
    await assignManagerUIService.orderDetailsPage.assignManagerModal.clickCancel();
    await assignManagerUIService.orderDetailsPage.assignManagerModal.waitForClosed();
    expect(managers.length).toBeGreaterThan(1);
    const [first, second] = managers as [string, string];
    return [normalizeManagerName(first), normalizeManagerName(second)];
  }

  async function assignManagerViaModal(assignManagerUIService: any, managerName: string) {
    const { orderDetailsPage } = assignManagerUIService;
    await openAssignManagerModalWithWait(assignManagerUIService);
    await orderDetailsPage.assignManagerModal.selectManager(managerName);
    await orderDetailsPage.assignManagerModal.saveButton.click();
    await orderDetailsPage.assignManagerModal.waitForClosed();
    await orderDetailsPage.waitForSpinners();
  }

  test.beforeEach(async ({ cleanup }) => {
    // Activate API cleanup fixture teardown (calls OrdersApiService.fullDelete).
    void cleanup;
  });

  test.describe("Assign manager to order", () => {
    for (const testCase of ASSIGN_MANAGER_ORDER_STATUS_CASES) {
      test(
        testCase.title,
        {
          tag: [testCase.isSmoke ? TAGS.SMOKE : TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS, TAGS.MANAGERS],
        },
        async ({ loginApiService, ordersApiService, assignManagerUIService }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await testCase.createOrder(ordersApiService, token);

          await assignManagerUIService.openOrderForManagerAssignment(order._id);
          const [firstManagerName] = await getFirstTwoManagerNames(assignManagerUIService);
          await assignManagerViaModal(assignManagerUIService, firstManagerName);

          await expect(assignManagerUIService.orderDetailsPage.header.assignedManagerContainer).toBeVisible();
          await assignManagerUIService.expectManagerAssigned(firstManagerName);
        },
      );
    }
  });
  test(
    "Cancel manager assignment without saving",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.MANAGERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, assignManagerUIService }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      await assignManagerUIService.openOrderForManagerAssignment(order._id);
      await assignManagerUIService.expectNoManagerAssigned();

      await assignManagerUIService.cancelManagerAssignment();

      await assignManagerUIService.expectNoManagerAssigned();
    },
  );

  test(
    "Assign manager modal shows all available managers",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.MANAGERS, TAGS.SMOKE] },
    async ({ loginApiService, ordersApiService, assignManagerUIService }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      await assignManagerUIService.openOrderForManagerAssignment(order._id);
      await assignManagerUIService.openAssignManagerModal();

      // Get managers list from modal
      const managers = await assignManagerUIService.orderDetailsPage.assignManagerModal.getAvailableManagers();
      expect(managers.length).toBeGreaterThan(0);

      // All managers should be non-empty strings
      for (const manager of managers) {
        expect(manager.trim().length).toBeGreaterThan(0);
      }

      // Close modal
      await assignManagerUIService.orderDetailsPage.assignManagerModal.clickCancel();
      await assignManagerUIService.orderDetailsPage.assignManagerModal.waitForClosed();
    },
  );

  test(
    "Manager assignment persists after page refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.MANAGERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, assignManagerUIService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      await assignManagerUIService.openOrderForManagerAssignment(order._id);
      const [firstManagerName] = await getFirstTwoManagerNames(assignManagerUIService);
      await assignManagerViaModal(assignManagerUIService, firstManagerName);
      await expect(assignManagerUIService.orderDetailsPage.header.assignedManagerContainer).toBeVisible();

      // Refresh the page
      await page.reload();
      await assignManagerUIService.orderDetailsPage.waitForOpened();

      // Manager should still be assigned
      await expect(assignManagerUIService.orderDetailsPage.header.assignedManagerContainer).toBeVisible();
      await assignManagerUIService.expectManagerAssigned(firstManagerName);
    },
  );

  test(
    "Replace manager with another manager",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS, TAGS.MANAGERS] },
    async ({ loginApiService, ordersApiService, assignManagerUIService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      // Assign first manager via UI flow
      await assignManagerUIService.openOrderForManagerAssignment(order._id);
      const [firstManagerName, secondManagerName] = await getFirstTwoManagerNames(assignManagerUIService);
      await assignManagerViaModal(assignManagerUIService, firstManagerName);
      await assignManagerUIService.expectManagerAssigned(firstManagerName);

      const { header } = orderDetailsPage;
      await expect(header.assignedManagerContainer).toBeVisible();
      await openAssignManagerModalWithWait(assignManagerUIService);

      // Pick the second manager from the list
      const items = orderDetailsPage.assignManagerModal.managerItems;
      const count = await items.count();
      await expect(count).toBeGreaterThan(1);
      await orderDetailsPage.assignManagerModal.selectManager(secondManagerName);
      await orderDetailsPage.assignManagerModal.saveButton.click();

      // Wait for modal to close and page to settle
      await orderDetailsPage.assignManagerModal.waitForClosed();
      await orderDetailsPage.waitForSpinners();

      // Verify new manager is shown
      await expect(header.assignedManagerContainer).toContainText(normalizeManagerName(secondManagerName));
    },
  );
});
