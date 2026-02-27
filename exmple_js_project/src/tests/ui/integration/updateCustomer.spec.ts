import { generateCustomerResponseData } from "data/salesPortal/customers/generateCustomerData";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { NOTIFICATIONS } from "data/salesPortal/notifications";
import {
  editOrderCustomerResponseErrorCases,
  editCustomerinOrderNegativeCases,
} from "data/salesPortal/orders/updateCustomerDDT";
import { STATUS_CODES } from "data/statusCodes";
import { TAGS } from "data/tags";
import { test, expect } from "fixtures";

test.describe("[Integration] [Orders]", () => {
  let token = "";
  let orderId = "";
  test.beforeEach(async ({ cleanup, loginApiService, ordersApiService, orderDetailsPage }) => {
    void cleanup;
    token = await loginApiService.loginAsAdmin();
    const order = await ordersApiService.createOrderAndEntities(token, 1);
    orderId = order._id;
    await orderDetailsPage.open(`#/orders/${orderId}`);
    await orderDetailsPage.waitForOpened();
  });

  for (const { title, customersMock, notification } of editCustomerinOrderNegativeCases) {
    test(
      title,
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION, TAGS.INTEGRATION] },
      async ({ mock, orderDetailsPage }) => {
        await customersMock(mock);
        const customerDetails = orderDetailsPage.customerDetails;
        const editCustomerModal = await customerDetails.clickEdit();
        await expect(editCustomerModal.uniqueElement).not.toBeVisible();
        await expect(orderDetailsPage.toastMessage).toBeVisible();
        await expect(orderDetailsPage.toastMessage).toHaveText(notification);
      },
    );
  }

  test(
    "Should display mocked customers in customers dropdown",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION, TAGS.INTEGRATION] },
    async ({ mock, orderDetailsPage }) => {
      const customer1 = generateCustomerResponseData();
      const customer2 = generateCustomerResponseData();
      await mock.getCustomersAll({
        Customers: [customer1, customer2],
        IsSuccess: true,
        ErrorMessage: null,
      });
      const customerDetails = orderDetailsPage.customerDetails;
      const editCustomerModal = await customerDetails.clickEdit();
      await editCustomerModal.waitForOpened();
      expect(await editCustomerModal.getCustomersDropdownTexts()).toStrictEqual(
        [customer1.name, customer2.name].sort(),
      );
    },
  );

  test(
    "Should NOT open edit customer modal with customers/all 401 error",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION, TAGS.INTEGRATION] },
    async ({ mock, orderDetailsPage, loginPage }) => {
      await mock.getCustomersAll(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.UNAUTHORIZED,
        },
        STATUS_CODES.UNAUTHORIZED,
      );
      const customerDetails = orderDetailsPage.customerDetails;
      const editCustomerModal = await customerDetails.clickEdit();
      await expect(editCustomerModal.uniqueElement).not.toBeVisible();
      await expect(loginPage.uniqueElement).toBeVisible();
      const authToken = await loginPage.getCookieByName("Authorization");
      expect(authToken).toBeFalsy();
    },
  );

  for (const { title, responseMock } of editOrderCustomerResponseErrorCases) {
    test(
      title,
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION, TAGS.INTEGRATION] },
      async ({ orderDetailsPage, mock, customersApiService, cleanup }) => {
        const secondCustomer = await customersApiService.create(token);
        cleanup.addCustomer(secondCustomer._id);
        const customerDetails = orderDetailsPage.customerDetails;
        const editCustomerModal = await customerDetails.clickEdit();
        await editCustomerModal.waitForOpened();
        await editCustomerModal.selectCustomer(secondCustomer.name);
        await responseMock(mock, orderId);
        await editCustomerModal.clickSave();
        await expect(editCustomerModal.uniqueElement).not.toBeVisible();
        await expect(orderDetailsPage.toastMessage).toBeVisible();
        await expect(orderDetailsPage.toastMessage).toHaveText(NOTIFICATIONS.CUSTOMER_FAILED_TO_UPDATE);
      },
    );
  }

  test(
    "Should logout when response status 401",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION, TAGS.INTEGRATION] },
    async ({ mock, orderDetailsPage, loginPage, customersApiService, cleanup }) => {
      const secondCustomer = await customersApiService.create(token);
      cleanup.addCustomer(secondCustomer._id);
      const customerDetails = orderDetailsPage.customerDetails;
      const editCustomerModal = await customerDetails.clickEdit();
      await editCustomerModal.waitForOpened();
      await editCustomerModal.selectCustomer(secondCustomer.name);
      await mock.orderById(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.UNAUTHORIZED,
        },
        orderId,
        STATUS_CODES.UNAUTHORIZED,
      );
      await editCustomerModal.clickSave();
      await expect(editCustomerModal.uniqueElement).not.toBeVisible();
      await expect(loginPage.uniqueElement).toBeVisible();
      const authToken = await loginPage.getCookieByName("Authorization");
      expect(authToken).toBeFalsy();
    },
  );
});
