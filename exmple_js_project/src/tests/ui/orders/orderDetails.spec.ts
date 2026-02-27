import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import { OrderDetailsPage } from "ui/pages/orders";

test.describe("[UI][Orders][Order Details]", () => {
  test.beforeEach(async ({ cleanup }) => {
    // Activate API cleanup fixture teardown (calls OrdersApiService.fullDelete).
    void cleanup;
  });

  test(
    "Draft order without delivery: header buttons and pencils",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.SMOKE] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(order._id);
      await orderDetails.waitForOpened();

      await expect(await orderDetails.header.isCancelVisible()).toBeTruthy();
      await expect(await orderDetails.header.isReopenVisible()).toBeFalsy();
      await expect(await orderDetails.header.isProcessVisible()).toBeFalsy();

      await expect(await orderDetails.customerDetails.isVisible()).toBeTruthy();
      await expect(await orderDetails.customerDetails.isEditVisible()).toBeTruthy();

      await orderDetails.requestedProducts.expectLoaded();
      await expect(await orderDetails.requestedProducts.isEditVisible()).toBeTruthy();
      await expect(await orderDetails.requestedProducts.isStartReceivingVisible()).toBeFalsy();
    },
  );

  test(
    "Draft order with delivery: can process",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createOrderWithDelivery(token, 1);
      const orderId = created._id;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(orderId);
      await orderDetails.waitForOpened();

      await expect(await orderDetails.header.isProcessVisible()).toBeTruthy();
    },
  );

  test(
    "In Process: receiving controls visible",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createOrderInProcess(token, 2);
      const orderId = created._id;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(orderId);
      await orderDetails.waitForOpened();

      await orderDetails.requestedProducts.expectLoaded();
      await expect(await orderDetails.requestedProducts.isStartReceivingVisible()).toBeTruthy();

      await orderDetails.requestedProducts.startReceiving();
      await orderDetails.requestedProducts.waitForReceivingControls();
    },
  );

  test(
    "Canceled: reopen visible, cancel/process hidden",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createCanceledOrder(token, 1);
      const orderId = created._id;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(orderId);
      await orderDetails.waitForOpened();

      await expect(await orderDetails.header.isReopenVisible()).toBeTruthy();
      await expect(await orderDetails.header.isCancelVisible()).toBeFalsy();
      await expect(await orderDetails.header.isProcessVisible()).toBeFalsy();
    },
  );

  test(
    "Partially Received: start receiving is available",
    { tag: [TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createPartiallyReceivedOrder(token, 2);
      const orderId = created._id;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(orderId);
      await orderDetails.waitForOpened();

      await orderDetails.requestedProducts.expectLoaded();
      await expect(await orderDetails.requestedProducts.isStartReceivingVisible()).toBeTruthy();
    },
  );

  test(
    "Draft with delivery: process via header triggers receiving",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createOrderWithDelivery(token, 1);
      const orderId = created._id;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(orderId);
      await orderDetails.waitForOpened();

      await orderDetails.header.processOrder();
      await orderDetails.waitForSpinners();
      await orderDetails.requestedProducts.expectLoaded();
      await orderDetails.requestedProducts.waitForReceivingReady();
      await expect(await orderDetails.header.isProcessVisible()).toBeFalsy();
    },
  );

  test(
    "Customer Details: edit opens modal",
    { tag: [TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const order = await ordersApiService.createOrderAndEntities(token, 1);

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(order._id);
      await orderDetails.waitForOpened();

      await orderDetails.customerDetails.clickEdit();
      await expect(page.locator(".modal.show, .modal.fade.show")).toBeVisible();
      await page.keyboard.press("Escape");
    },
  );

  test(
    "Requested Products: edit opens modal",
    { tag: [TAGS.UI, TAGS.ORDERS] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createOrderWithDelivery(token, 1);
      const orderId = created._id;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(orderId);
      await orderDetails.waitForOpened();

      await orderDetails.requestedProducts.clickEdit();
      await expect(page.locator(".modal.show, .modal.fade.show")).toBeVisible();
      await page.keyboard.press("Escape");
    },
  );

  test(
    "In Process: select all and save receiving marks all received",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ loginApiService, ordersApiService, page }) => {
      const token = await loginApiService.loginAsAdmin();
      const created = await ordersApiService.createOrderInProcess(token, 2);
      const order = created;

      const orderDetails = new OrderDetailsPage(page);
      await orderDetails.openByOrderId(order._id);
      await orderDetails.waitForOpened();

      await orderDetails.requestedProducts.expectLoaded();
      await orderDetails.requestedProducts.startReceiving();
      await orderDetails.requestedProducts.waitForReceivingControls();
      await orderDetails.requestedProducts.selectAll();
      await orderDetails.requestedProducts.saveReceiving();
      await orderDetails.waitForSpinners();

      for (const product of order.products) {
        await expect(await orderDetails.requestedProducts.isProductReceived(product._id, product.name)).toBe(true);
      }
    },
  );
});
