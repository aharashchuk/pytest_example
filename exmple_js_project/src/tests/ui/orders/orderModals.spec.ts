import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import {
  NOTIFICATIONS,
  CANCEL_ORDER_MODAL,
  PROCESS_ORDER_MODAL,
  REOPEN_ORDER_MODAL,
} from "data/salesPortal/notifications";
import { assertConfirmationModal } from "utils/assertions/confirmationModal.assert";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Modals]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    if (token) await ordersApiService.fullDelete(token);
  });

  test(
    "Process order on Process Confirmation modal",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const order = await ordersApiService.createOrderWithDelivery(token, 1);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();

      await orderDetailsPage.clickProcess();
      await orderDetailsPage.processModal.waitForOpened();

      await assertConfirmationModal(orderDetailsPage.processModal, PROCESS_ORDER_MODAL);

      await orderDetailsPage.processModal.clickConfirm();
      await expect(orderDetailsPage.notificationToast).toHaveText(NOTIFICATIONS.ORDER_PROCESSED);
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PROCESSING);
    },
  );

  test(
    "Cancel order on Cancel Confirmation modal",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const created = await ordersApiService.createOrderWithDelivery(token, 1);
      const orderId = created._id;

      await orderDetailsPage.openByOrderId(orderId);
      await orderDetailsPage.waitForOpened();

      await orderDetailsPage.clickCancel();
      await orderDetailsPage.cancelModal.waitForOpened();

      await assertConfirmationModal(orderDetailsPage.cancelModal, CANCEL_ORDER_MODAL);

      await orderDetailsPage.cancelModal.clickConfirm();
      await expect(orderDetailsPage.notificationToast).toHaveText(NOTIFICATIONS.ORDER_CANCELED);
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.CANCELED);
    },
  );

  test(
    "Reopen order on Reopen Confirmation modal",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, orderDetailsPage }) => {
      const created = await ordersApiService.createCanceledOrder(token, 2);
      const orderId = created._id;

      await orderDetailsPage.openByOrderId(orderId);
      await orderDetailsPage.waitForOpened();

      await orderDetailsPage.clickReopen();
      await orderDetailsPage.reopenModal.waitForOpened();

      await assertConfirmationModal(orderDetailsPage.reopenModal, REOPEN_ORDER_MODAL);

      await orderDetailsPage.reopenModal.clickConfirm();
      await expect(orderDetailsPage.notificationToast).toHaveText(NOTIFICATIONS.ORDER_REOPENED);
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.DRAFT);
    },
  );
});
