import { test, expect } from "fixtures";
import { TAGS } from "data/tags";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Processing]", () => {
  test.beforeEach(async ({ cleanup }) => {
    void cleanup;
  });

  test(
    "Processing order shows receiving controls",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      // Create order with delivery and move to PROCESSING via API
      const order = await ordersApiService.createOrderInProcess(token, 2);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      // Verify page loaded and receiving is available (order is in PROCESSING)
      await orderDetailsPage.requestedProducts.expectLoaded();
      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PROCESSING);
      await expect(await orderDetailsPage.requestedProducts.isStartReceivingVisible()).toBeTruthy();
    },
  );

  test(
    "Draft order shows edit controls",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await orderDetailsPage.requestedProducts.expectLoaded();
      await orderDetailsPage.header.expectStatus(ORDER_STATUS.DRAFT);
      await expect(await orderDetailsPage.header.isCancelVisible()).toBeTruthy();
      // Draft orders should not have Process or Receiving buttons
      await expect(await orderDetailsPage.header.isProcessVisible()).toBeFalsy();
      await expect(await orderDetailsPage.requestedProducts.isStartReceivingVisible()).toBeFalsy();
    },
  );

  test(
    "In Process order hides process button and shows receiving",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 2);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PROCESSING);

      // Once order is processing, process button should be hidden, cancel should stay
      await expect(await orderDetailsPage.header.isProcessVisible()).toBeFalsy();
      await expect(await orderDetailsPage.header.isCancelVisible()).toBeTruthy();

      // Receiving controls remain available
      await orderDetailsPage.requestedProducts.expectLoaded();
      await expect(await orderDetailsPage.requestedProducts.isStartReceivingVisible()).toBeTruthy();
    },
  );
});
