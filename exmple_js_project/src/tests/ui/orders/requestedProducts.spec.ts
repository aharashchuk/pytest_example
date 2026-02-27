import { test, expect } from "fixtures";
import { NOTIFICATIONS } from "data/salesPortal/notifications";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { IOrderFromResponse } from "data/types/order.types";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import { STATUS_CODES } from "data/statusCodes";
import { TAGS } from "data/tags";
import { getFieldValues } from "api/service/products.service";

const PRODUCTS_MAX_COUNT = 5;

test.describe("[UI][Orders][Requested Products]", () => {
  let token = "";

  test.beforeEach(async ({ orderDetailsPage, cleanup }) => {
    void cleanup;
    token = await orderDetailsPage.getAuthToken();
  });

  test(
    "Edit requested products: increase products count to 5",
    { tag: [TAGS.REGRESSION, TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, productsApiService, ordersApi, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createOrderAndEntities(token, 1);
      cleanup.addOrder(order._id);

      // Create extra products to expand order to 5 items
      const products = await productsApiService.bulkCreate(token, PRODUCTS_MAX_COUNT - 1);
      cleanup.addProduct(...getFieldValues(products, "_id"));
      const extraProductNames = getFieldValues(products, "name");

      const initialName = order.products[0]!.name;
      const desiredProductNames = [initialName, ...extraProductNames];

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.editProductsModal.openFromOrderDetails(
        orderDetailsPage.requestedProducts,
        ORDER_STATUS.DRAFT,
      );
      await expect(orderDetailsPage.editProductsModal.productRows).toHaveCount(1);

      const updatedFromUi = await orderDetailsPage.editProductsModal.editOrder(desiredProductNames);
      expect(updatedFromUi.products).toHaveLength(PRODUCTS_MAX_COUNT);

      await expect.soft(orderDetailsPage.notificationToast).toHaveText(NOTIFICATIONS.ORDER_UPDATED);
      await orderDetailsPage.editProductsModal.waitForClosed();
      // Verify changes are saved in BE
      const getResponse = await ordersApi.getById(order._id, token);
      validateResponse(getResponse, {
        status: STATUS_CODES.OK,
        IsSuccess: true,
        ErrorMessage: null,
        schema: getOrderSchema,
      });
      const updatedOrder = getResponse.body.Order as IOrderFromResponse;
      expect(updatedOrder.products).toHaveLength(PRODUCTS_MAX_COUNT);
      const actualNames = updatedOrder.products.map((p) => p.name).sort();
      const expectedNames = desiredProductNames.slice().sort();
      expect(actualNames).toEqual(expectedNames);
    },
  );

  test(
    "Edit requested products: decrease products count to 1",
    { tag: [TAGS.REGRESSION, TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, ordersApi, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createOrderAndEntities(token, PRODUCTS_MAX_COUNT);
      cleanup.addOrder(order._id);

      const keepProductName = order.products[0]!.name;

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.editProductsModal.openFromOrderDetails(
        orderDetailsPage.requestedProducts,
        ORDER_STATUS.DRAFT,
      );

      await expect(orderDetailsPage.editProductsModal.productRows).toHaveCount(PRODUCTS_MAX_COUNT);
      await orderDetailsPage.editProductsModal.editOrder([keepProductName]);
      await expect.soft(orderDetailsPage.notificationToast).toHaveText(NOTIFICATIONS.ORDER_UPDATED);
      await orderDetailsPage.editProductsModal.waitForClosed();

      // Verify changes are saved in BE
      const getResponse = await ordersApi.getById(order._id, token);
      validateResponse(getResponse, {
        status: STATUS_CODES.OK,
        IsSuccess: true,
        ErrorMessage: null,
        schema: getOrderSchema,
      });
      const updatedOrder = getResponse.body.Order as IOrderFromResponse;
      expect(updatedOrder.products).toHaveLength(1);
      expect(updatedOrder.products[0]!.name).toBe(keepProductName);
    },
  );

  test(
    "Edit requested products: delete product option is not available when order has 1 product",
    { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createOrderAndEntities(token, 1);
      cleanup.addOrder(order._id);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.editProductsModal.openFromOrderDetails(
        orderDetailsPage.requestedProducts,
        ORDER_STATUS.DRAFT,
      );
      await expect(orderDetailsPage.editProductsModal.productRows).toHaveCount(1);

      await expect(orderDetailsPage.editProductsModal.deleteProductButton.first()).not.toBeVisible();
    },
  );

  test(
    "Edit requested products: replace all products in the order",
    { tag: [TAGS.REGRESSION, TAGS.SMOKE, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, productsApiService, ordersApi, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createOrderAndEntities(token, 2);
      cleanup.addOrder(order._id);

      const originalNames = order.products.map((p) => p.name).sort();

      const replacement1 = await productsApiService.create(token);
      const replacement2 = await productsApiService.create(token);
      cleanup.addProduct(replacement1._id);
      cleanup.addProduct(replacement2._id);
      const desiredProductNames = [replacement1.name, replacement2.name];

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.editProductsModal.openFromOrderDetails(
        orderDetailsPage.requestedProducts,
        ORDER_STATUS.DRAFT,
      );
      await expect(orderDetailsPage.editProductsModal.productRows).toHaveCount(2);

      const updatedFromUi = await orderDetailsPage.editProductsModal.editOrder(desiredProductNames);
      expect(updatedFromUi.products).toHaveLength(2);

      await expect.soft(orderDetailsPage.notificationToast).toHaveText(NOTIFICATIONS.ORDER_UPDATED);
      await orderDetailsPage.editProductsModal.waitForClosed();
      // Verify changes are saved in BE
      const getResponse = await ordersApi.getById(order._id, token);
      validateResponse(getResponse, {
        status: STATUS_CODES.OK,
        IsSuccess: true,
        ErrorMessage: null,
        schema: getOrderSchema,
      });
      const updatedOrder = getResponse.body.Order as IOrderFromResponse;
      expect(updatedOrder.products).toHaveLength(2);

      const actualNames = updatedOrder.products.map((p) => p.name).sort();
      expect(actualNames).toEqual(desiredProductNames.slice().sort());
      expect(actualNames).not.toEqual(originalNames);
    },
  );

  test(
    "Edit requested products: add product functionality is not available when order already has 5 products",
    { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createOrderAndEntities(token, PRODUCTS_MAX_COUNT);
      cleanup.addOrder(order._id);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await orderDetailsPage.editProductsModal.openFromOrderDetails(
        orderDetailsPage.requestedProducts,
        ORDER_STATUS.DRAFT,
      );
      await expect(orderDetailsPage.editProductsModal.productRows).toHaveCount(PRODUCTS_MAX_COUNT);
      await expect(orderDetailsPage.editProductsModal.addProductButton).not.toBeVisible();
    },
  );

  test(
    "Edit requested products: edit functionality is NOT available for In Process order",
    { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createOrderInProcess(token, 1);
      cleanup.addOrder(order._id);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.PROCESSING);
      await orderDetailsPage.requestedProducts.expectLoaded();
      await expect(orderDetailsPage.requestedProducts.editButton).not.toBeVisible();
    },
  );

  test(
    "Edit requested products: edit functionality is NOT available for Canceled order",
    { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
    async ({ ordersApiService, orderDetailsPage, cleanup }) => {
      const order = await ordersApiService.createCanceledOrder(token, 1);
      cleanup.addOrder(order._id);

      await orderDetailsPage.openByOrderId(order._id);
      await orderDetailsPage.waitForOpened();
      await expect(orderDetailsPage.statusOrderLabel).toHaveText(ORDER_STATUS.CANCELED);
      await orderDetailsPage.requestedProducts.expectLoaded();
      await expect(orderDetailsPage.requestedProducts.editButton).not.toBeVisible();
    },
  );
});
