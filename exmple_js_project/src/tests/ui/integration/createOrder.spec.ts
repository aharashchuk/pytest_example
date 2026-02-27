import { generateCustomerResponseData } from "data/salesPortal/customers/generateCustomerData";
import {
  createOrderResponseErrorCases,
  openCreateOrderModalNegativeCases,
  openCreateOrderModalUnauthorizedCases,
} from "data/salesPortal/orders/createOrderMockDDT";
import { generateProductResponseData } from "data/salesPortal/products/generateProductData";
import { TAGS } from "data/tags";
import { test, expect } from "fixtures";

test.describe("[Integration] [Orders]", () => {
  test.beforeEach(async ({ ordersListPage }) => {
    await ordersListPage.open("#/orders");
    await ordersListPage.waitForOpened();
  });

  for (const { title, customersMock, productsMock, notification } of openCreateOrderModalNegativeCases) {
    test(title, { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] }, async ({ mock, ordersListPage }) => {
      await customersMock(mock);
      await productsMock(mock);
      const createOrderModal = await ordersListPage.clickCreateOrderButton();
      await expect(createOrderModal.uniqueElement).not.toBeVisible();
      await expect(ordersListPage.toastMessage).toBeVisible();
      await expect(ordersListPage.toastMessage).toHaveText(notification);
    });
  }

  for (const { title, customersMock, productsMock } of openCreateOrderModalUnauthorizedCases) {
    test(
      title,
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ mock, ordersListPage, loginPage, context }) => {
        await customersMock(mock);
        await productsMock(mock);
        const createOrderModal = await ordersListPage.clickCreateOrderButton();
        await expect(createOrderModal.uniqueElement).not.toBeVisible();
        await expect(loginPage.uniqueElement).toBeVisible();
        const authToken = (await context.cookies()).some((c) => c.name === "Authorization");
        expect(authToken).toBeFalsy();
      },
    );
  }

  for (const { title, responseMock, notification } of createOrderResponseErrorCases) {
    test(title, { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] }, async ({ ordersListPage, mock }) => {
      const customer = generateCustomerResponseData();
      const product = generateProductResponseData();
      await responseMock(mock);
      await mock.getCustomersAll({
        Customers: [customer],
        IsSuccess: true,
        ErrorMessage: null,
      });
      await mock.getProductsAll({
        Products: [product],
        IsSuccess: true,
        ErrorMessage: null,
      });
      const createOrderModal = await ordersListPage.clickCreateOrderButton();
      await createOrderModal.waitForOpened();
      await createOrderModal.selectCustomer(customer.name);
      await createOrderModal.selectProduct(0, product.name);
      await createOrderModal.clickCreate();
      await expect(createOrderModal.uniqueElement).not.toBeVisible();
      await expect(ordersListPage.toastMessage).toBeVisible();
      await expect(ordersListPage.toastMessage).toHaveText(notification);
    });
  }

  test(
    "Should display mocked customers in customers dropdown",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ mock, ordersListPage }) => {
      const customer1 = generateCustomerResponseData();
      const customer2 = generateCustomerResponseData();
      await mock.getCustomersAll({
        Customers: [customer1, customer2],
        IsSuccess: true,
        ErrorMessage: null,
      });
      await mock.getProductsAll({
        Products: [generateProductResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      });
      const createOrderModal = await ordersListPage.clickCreateOrderButton();
      await createOrderModal.waitForOpened();
      expect(await createOrderModal.getCustomersDropdownTexts()).toStrictEqual([customer1.name, customer2.name]);
    },
  );

  test(
    "Should display mocked products in products dropdown",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ mock, ordersListPage }) => {
      const product1 = generateProductResponseData();
      const product2 = generateProductResponseData();
      await mock.getCustomersAll({
        Customers: [generateCustomerResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      });
      await mock.getProductsAll({
        Products: [product1, product2],
        IsSuccess: true,
        ErrorMessage: null,
      });
      const createOrderModal = await ordersListPage.clickCreateOrderButton();
      await createOrderModal.waitForOpened();
      expect(await createOrderModal.getProductsDropdownTexts()).toStrictEqual([product1.name, product2.name]);
    },
  );
});
