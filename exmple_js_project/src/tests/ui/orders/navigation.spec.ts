import { test, expect } from "fixtures";
import { TAGS } from "data/tags";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Navigation]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.beforeEach(async ({ cleanup }) => {
    // Activate API cleanup fixture teardown (calls OrdersApiService.fullDelete).
    void cleanup;
  });

  test(
    "Open Orders List from Home Page",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.SMOKE] },
    async ({ homeUIService, ordersListPage }) => {
      await homeUIService.open();
      await homeUIService.homePage.waitForOpened();
      await homeUIService.openModule("Orders");
      await homeUIService.ordersListPage.waitForOpened();
      await expect(ordersListPage.navBar.ordersButton).toContainClass("active");
    },
  );

  test(
    "Open Orders List on direct URL",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersListPage }) => {
      await ordersListPage.open("#/orders");
      await ordersListPage.waitForOpened();
      await expect(ordersListPage.navBar.ordersButton).toContainClass("active");
    },
  );

  test(
    "Open Order Details from Orders List",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersListPage, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderInStatus(token, 1, ORDER_STATUS.PROCESSING);
      await ordersListPage.open("#/orders");
      await ordersListPage.waitForOpened();
      await ordersListPage.clickAction(order._id, "details");
      await orderDetailsPage.waitForOpened();
      const openedOrderId = await orderDetailsPage.header.getOrderNumberText();
      expect.soft(openedOrderId).toBe(order._id);
      await expect(orderDetailsPage.navBar.ordersButton).toContainClass("active");
    },
  );

  test(
    "Open Order Details on direct URL",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderInStatus(token, 1, ORDER_STATUS.PROCESSING);
      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      const openedOrderId = await orderDetailsPage.header.getOrderNumberText();
      expect.soft(openedOrderId).toBe(order._id);
      await expect(orderDetailsPage.navBar.ordersButton).toContainClass("active");
    },
  );

  test(
    "Open Orders List from NavBar",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ homeUIService, ordersListPage }) => {
      await homeUIService.open();
      await homeUIService.homePage.waitForOpened();
      await ordersListPage.navBar.clickOnNavButton("Orders");
      await ordersListPage.waitForOpened();
      await expect(ordersListPage.navBar.ordersButton).toContainClass("active");
    },
  );
});
