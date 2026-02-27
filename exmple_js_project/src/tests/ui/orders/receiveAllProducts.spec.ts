import { test, expect } from "fixtures";
import { TAGS } from "data/tags";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Receive All Products]", () => {
  test.beforeEach(async ({ cleanup }) => {
    void cleanup;
  });

  test(
    "Receive all products via select all",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 3);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      await orderDetailsPage.requestedProducts.startReceiving();
      await orderDetailsPage.requestedProducts.waitForReceivingReady();

      // Select all products
      await orderDetailsPage.requestedProducts.selectAll();
      await orderDetailsPage.requestedProducts.saveReceiving();

      await orderDetailsPage.waitForSpinners();

      await orderDetailsPage.header.expectStatus(ORDER_STATUS.RECEIVED);

      // Verify all products are marked as received
      for (const product of order.products) {
        const isReceived = await orderDetailsPage.requestedProducts.isProductReceived(product._id, product.name);
        await expect(isReceived).toBeTruthy();
      }

      // Verify start receiving is not visible anymore
      const startReceivingVisible = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(startReceivingVisible).toBeFalsy();
    },
  );

  test(
    "Receive all products manually one by one",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 3);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      await orderDetailsPage.requestedProducts.startReceiving();
      await orderDetailsPage.requestedProducts.waitForReceivingReady();

      // Select each product individually
      for (const product of order.products) {
        await orderDetailsPage.requestedProducts.toggleProductById(product._id);
      }
      await orderDetailsPage.requestedProducts.saveReceiving();

      await orderDetailsPage.waitForSpinners();

      await orderDetailsPage.header.expectStatus(ORDER_STATUS.RECEIVED);

      // Verify all products are marked as received
      for (const product of order.products) {
        const isReceived = await orderDetailsPage.requestedProducts.isProductReceived(product._id, product.name);
        await expect(isReceived).toBeTruthy();
      }

      // Verify start receiving is not visible anymore
      const startReceivingVisible = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(startReceivingVisible).toBeFalsy();
    },
  );

  test(
    "Fully received order shows correct status and hides receiving controls",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createReceivedOrder(token, 2);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      await orderDetailsPage.header.expectStatus(ORDER_STATUS.RECEIVED);

      // Verify all products are received
      for (const product of order.products) {
        const isReceived = await orderDetailsPage.requestedProducts.isProductReceived(product._id, product.name);
        await expect(isReceived).toBeTruthy();
      }

      // Verify start receiving is not visible anymore
      const startReceivingVisible = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(startReceivingVisible).toBeFalsy();
    },
  );
});
