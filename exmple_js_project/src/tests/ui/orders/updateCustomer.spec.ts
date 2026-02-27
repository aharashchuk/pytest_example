import { orderInStatus } from "data/salesPortal/orders/updateCustomerDDT";
import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import _ from "lodash";
import { convertToDateAndTime } from "utils/date.utils";

test.describe("[UI] [Orders] [Update customer]", () => {
  let token = "";
  test.beforeEach(async ({ cleanup, loginApiService, ordersApiService, orderDetailsUIService }) => {
    void cleanup;
    token = await loginApiService.loginAsAdmin();
    const order = await ordersApiService.createOrderAndEntities(token, 1);
    const orderId = order._id;
    await orderDetailsUIService.openOrderById(orderId);
  });

  test(
    "Should be visible edit customer button in Draft order",
    { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
    async ({ orderDetailsPage }) => {
      await expect(orderDetailsPage.customerDetails.uniqueElement).toBeVisible();
      await expect(orderDetailsPage.customerDetails.editButton).toBeVisible();
    },
  );

  test(
    "Should update customer in Draft order",
    { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS, TAGS.E2E] },
    async ({ orderDetailsPage, cleanup, customersApiService }) => {
      const secondCustomer = await customersApiService.create(token);
      cleanup.addCustomer(secondCustomer._id);
      const customerDetails = orderDetailsPage.customerDetails;
      const editCustomerModal = await customerDetails.clickEdit();
      await editCustomerModal.waitForOpened();
      await editCustomerModal.selectCustomer(secondCustomer.name);
      await editCustomerModal.clickSave();
      await orderDetailsPage.waitForOpened();
      const updatedCustomerData = await customerDetails.getCustomerData();
      expect(updatedCustomerData).toEqual({
        ..._.omit(secondCustomer, ["_id"]),
        createdOn: convertToDateAndTime(secondCustomer.createdOn),
      });
    },
  );
});

test.describe("[UI] [Orders] [Check edit customer button]", () => {
  let token = "";
  test.beforeEach(async ({ cleanup, loginApiService }) => {
    void cleanup;
    token = await loginApiService.loginAsAdmin();
  });
  for (const orderCase of orderInStatus) {
    test(
      `Should NOT be visible edit customer button in order in ${orderCase.name} status`,
      { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
      async ({ orderDetailsPage, ordersApiService, orderDetailsUIService }) => {
        const order = await orderCase.create(ordersApiService, token);
        const orderId = order._id;
        await orderDetailsUIService.openOrderById(orderId);
        await expect(orderDetailsPage.customerDetails.uniqueElement).toBeVisible();
        await expect(orderDetailsPage.customerDetails.editButton).not.toBeVisible();
      },
    );
  }
});
