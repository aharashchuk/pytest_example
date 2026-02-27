import { test, expect } from "fixtures";
import { TAGS } from "data/tags";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Receive Partial Products]", () => {
  test.beforeEach(async ({ cleanup }) => {
    void cleanup;
  });

  test(
    "Receive part of products - select one",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 3);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      // Start receiving to show receiving controls
      await orderDetailsPage.requestedProducts.startReceiving();
      await orderDetailsPage.requestedProducts.waitForReceivingReady();

      // Select and receive first product only
      await orderDetailsPage.requestedProducts.toggleProductById(order.products[0]!._id);
      await orderDetailsPage.requestedProducts.saveReceiving();

      // Verify order is now partially received
      await orderDetailsPage.waitForSpinners();
      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PARTIALLY_RECEIVED);
      const isFirstReceived = await orderDetailsPage.requestedProducts.isProductReceived(
        order.products[0]!._id,
        order.products[0]!.name,
      );
      await expect(isFirstReceived).toBeTruthy();

      // Start receiving should still be visible for remaining items
      const startReceivingVisible = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(startReceivingVisible).toBeTruthy();
    },
  );

  test(
    "Receive multiple products but not all",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderInProcess(token, 4);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      await orderDetailsPage.requestedProducts.startReceiving();
      await orderDetailsPage.requestedProducts.waitForReceivingReady();

      // Select multiple products (first and third)
      await orderDetailsPage.requestedProducts.toggleProductById(order.products[0]!._id);
      await orderDetailsPage.requestedProducts.toggleProductById(order.products[2]!._id);
      await orderDetailsPage.requestedProducts.saveReceiving();

      await orderDetailsPage.waitForSpinners();
      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PARTIALLY_RECEIVED);
      const isFirstReceived = await orderDetailsPage.requestedProducts.isProductReceived(
        order.products[0]!._id,
        order.products[0]!.name,
      );
      const isThirdReceived = await orderDetailsPage.requestedProducts.isProductReceived(
        order.products[2]!._id,
        order.products[2]!.name,
      );
      await expect(isFirstReceived).toBeTruthy();
      await expect(isThirdReceived).toBeTruthy();

      // Start receiving should still be visible for remaining items
      const startReceivingVisible = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(startReceivingVisible).toBeTruthy();
    },
  );

  test(
    "Partially received order allows receiving remaining",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      // Create order that is partially received (3 products, 1 received)
      const order = await ordersApiService.createPartiallyReceivedOrder(token, 3);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PARTIALLY_RECEIVED);

      // Should still have start receiving available for remaining items
      const canReceiveRemaining = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(canReceiveRemaining).toBeTruthy();

      await orderDetailsPage.requestedProducts.startReceiving();
      await orderDetailsPage.requestedProducts.waitForReceivingReady();

      // Receive another product
      await orderDetailsPage.requestedProducts.toggleProductById(order.products[1]!._id);
      await orderDetailsPage.requestedProducts.saveReceiving();

      await orderDetailsPage.waitForSpinners();
      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PARTIALLY_RECEIVED);
      const isProductReceived = await orderDetailsPage.requestedProducts.isProductReceived(
        order.products[1]!._id,
        order.products[1]!.name,
      );
      await expect(isProductReceived).toBeTruthy();

      // Verify first product is still received (regression check)
      const isFirstStillReceived = await orderDetailsPage.requestedProducts.isProductReceived(
        order.products[0]!._id,
        order.products[0]!.name,
      );
      await expect(isFirstStillReceived).toBeTruthy();
    },
  );

  test(
    "Partially received order can be finished to Received",
    { tag: [TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, orderDetailsPage }) => {
      const token = await loginApiService.loginAsAdmin();
      // Create order with first product already received
      const order = await ordersApiService.createPartiallyReceivedOrder(token, 3);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.requestedProducts.expectLoaded();

      await orderDetailsPage.header.expectStatus(ORDER_STATUS.PARTIALLY_RECEIVED);

      await orderDetailsPage.requestedProducts.startReceiving();
      await orderDetailsPage.requestedProducts.waitForReceivingReady();

      // Receive remaining products (skip already received first one)
      for (const product of order.products.slice(1)) {
        await orderDetailsPage.requestedProducts.toggleProductById(product._id);
      }
      await orderDetailsPage.requestedProducts.saveReceiving();

      await orderDetailsPage.waitForSpinners();
      await orderDetailsPage.requestedProducts.expectLoaded();
      await orderDetailsPage.header.expectStatus(ORDER_STATUS.RECEIVED);

      // All products should be received, and receiving entry point hidden
      for (const product of order.products) {
        const isReceived = await orderDetailsPage.requestedProducts.isProductReceived(product._id, product.name);
        await expect(isReceived).toBeTruthy();
      }

      const canStartReceiving = await orderDetailsPage.requestedProducts.isStartReceivingVisible();
      await expect(canStartReceiving).toBeFalsy();
    },
  );
});
