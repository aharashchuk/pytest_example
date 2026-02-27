import { ORDER_STATUS } from "data/salesPortal/order-status";
import { notificationOnStatusChangeCases } from "data/salesPortal/orders/notificationsTestData";
import { STATUS_CODES } from "data/statusCodes";
import { TAGS } from "data/tags";
import { expect, test } from "fixtures";
import { validateResponse } from "utils/validation/validateResponse.utils";

test.describe("[API][Orders][Notifications]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    await ordersApiService.fullDelete(token);
  });

  for (const orderCase of notificationOnStatusChangeCases) {
    test(
      `Got notification on ${ORDER_STATUS.DRAFT} to ${orderCase.to} status change`,
      { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ ordersApiService, notificationsApi }) => {
        const order = await ordersApiService.createOrderInStatus(token, 2, orderCase.to);
        const notifications = await notificationsApi.getUsersNotifications(token);
        validateResponse(notifications, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
        });
        const notification = notifications.body.Notifications.find((n) => order._id === n._id);
        if (notification) {
          expect.soft(notification.message).toContain(`Order #${order._id} status changed to ${orderCase.to}`);
        }
      },
    );
  }
});
