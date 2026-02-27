import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Refresh]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    if (token) await ordersApiService.fullDelete(token);
  });

  test(
    "Draft => Processing after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderWithDelivery(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.DRAFT);

      await ordersApiService.updateStatus(token, order._id, ORDER_STATUS.PROCESSING);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PROCESSING);
    },
  );

  test(
    "Processing => Received after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersApi, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderInProcess(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PROCESSING);

      const productIdsToReceive = order.products.map((p) => p._id);
      await ordersApi.receiveProducts(order._id, productIdsToReceive, token);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.RECEIVED);
    },
  );

  test(
    "Processing => Partially Received after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersApi, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderInProcess(token, 2);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PROCESSING);

      const oneProductId = order.products[0]!._id;
      await ordersApi.receiveProducts(order._id, [oneProductId], token);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PARTIALLY_RECEIVED);
    },
  );

  test(
    "Partially Received => Received after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersApi, orderDetailsPage }) => {
      const order = await ordersApiService.createPartiallyReceivedOrder(token, 2);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PARTIALLY_RECEIVED);

      const remainingProductIds = order.products.filter((p) => !p.received).map((p) => p._id);
      await ordersApi.receiveProducts(order._id, remainingProductIds, token);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.RECEIVED);
    },
  );

  test(
    "Draft => Canceled after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderWithDelivery(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.DRAFT);

      await ordersApiService.updateStatus(token, order._id, ORDER_STATUS.CANCELED);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.CANCELED);
    },
  );

  test(
    "Canceled => Draft after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const order = await ordersApiService.createCanceledOrder(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.CANCELED);

      await ordersApiService.updateStatus(token, order._id, ORDER_STATUS.DRAFT);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.DRAFT);
    },
  );

  test(
    "Processing => Canceled after Refresh",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderInProcess(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PROCESSING);

      await ordersApiService.updateStatus(token, order._id, ORDER_STATUS.CANCELED);

      await orderDetailsPage.clickRefreshOrder();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.CANCELED);
    },
  );
});
