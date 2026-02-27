import { test, expect } from "fixtures/api.fixture";
import { TAGS } from "data/tags";
import { STATUS_CODES } from "data/statusCodes";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { IOrderFromResponse } from "data/types/order.types";
import { ORDER_HISTORY_ACTIONS, ORDER_STATUS } from "data/salesPortal/order-status";
import type { IProduct } from "data/types/product.types";
import { updateOrderErrorCases } from "data/salesPortal/orders/updateOrderTestData";
import { productIdsOf, calcTotal } from "utils/orders/helpers";

test.describe("[API][Orders]", () => {
  let token = "";
  let orderId = "";
  let orderObj: IOrderFromResponse | null = null;

  test.beforeEach(async ({ loginApiService, ordersApiService, cleanup }) => {
    token = await loginApiService.loginAsAdmin();
    const order = await ordersApiService.createOrderAndEntities(token, 1);
    orderId = order._id;
    orderObj = order;
    cleanup.addOrder(orderId);
  });

  test.describe("[Update order]", () => {
    test(
      "ORD-PUT-001: Successful products update recalculates total_price",
      { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ ordersApiService, productsApiService }) => {
        const original = orderObj!;

        expect.soft(original.products.length).toBeGreaterThan(0);
        const originalFirst = original.products[0]!;

        const updatedProduct: IProduct = {
          name: originalFirst.name,
          manufacturer: originalFirst.manufacturer,
          amount: originalFirst.amount,
          price: originalFirst.price + 100,
        };
        await productsApiService.update(token, originalFirst._id, updatedProduct);

        const updated = await ordersApiService.update(token, orderId, {
          customer: original.customer._id,
          products: [originalFirst._id],
        });
        const expectedTotal = calcTotal(updated);
        expect.soft(updated.total_price).toBe(expectedTotal);
        expect.soft(updated.products[0]!.price).toBe(originalFirst.price + 100);
        expect.soft(updated._id).toBe(orderId);
      },
    );

    test(
      "ORD-PUT-002: Successful update of customer in order",
      { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ ordersApiService, customersApiService, cleanup }) => {
        const original = orderObj!;
        const newCustomer = await customersApiService.create(token);
        cleanup.addCustomer(newCustomer._id);

        const productIds = productIdsOf(original);
        const updated = await ordersApiService.update(token, orderId, {
          customer: newCustomer._id,
          products: productIds,
        });
        expect.soft(updated.customer._id).toBe(newCustomer._id);
        const expectedTotal = calcTotal(updated);
        expect.soft(updated.total_price).toBe(expectedTotal);
      },
    );

    test(
      "ORD-PUT-003: Order status is DRAFT after update",
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ ordersApiService }) => {
        const before = orderObj!;

        const productIds = productIdsOf(before);
        const after = await ordersApiService.update(token, orderId, {
          customer: before.customer._id,
          products: productIds,
        });
        expect.soft(after.status).toBe(ORDER_STATUS.DRAFT);
      },
    );

    test(
      "ORD-PUT-004: History entry recorded when order composition changes",
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ ordersApiService, productsApiService, cleanup }) => {
        const before = orderObj!;
        const beforeHistoryLen = before.history.length;

        const extraProduct = await productsApiService.create(token);
        cleanup.addProduct(extraProduct._id);
        const productIds = [before.products[0]!._id, extraProduct._id];

        const after = await ordersApiService.update(token, orderId, {
          customer: before.customer._id,
          products: productIds,
        });
        expect.soft(after.history.length).toBeGreaterThan(beforeHistoryLen);
        const changed = after.history.find((h) => h.action === ORDER_HISTORY_ACTIONS.REQUIRED_PRODUCTS_CHANGED);
        expect.soft(changed).toBeTruthy();
        expect.soft(changed?.changedOn).toBeTruthy();
      },
    );

    test(
      "ORD-PUT-012: Cannot delete linked product/customer until order is deleted",
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ productsApi, customersApi }) => {
        const original: IOrderFromResponse = orderObj!;
        const deleteProductResponse = await productsApi.delete(original.products[0]!._id, token);
        expect.soft(deleteProductResponse.status).toBe(STATUS_CODES.BAD_REQUEST);

        const deleteCustomerResponse = await customersApi.delete(token, original.customer._id);
        expect.soft(deleteCustomerResponse.status).toBe(STATUS_CODES.BAD_REQUEST);
      },
    );

    test(
      "ORD-PUT-013: PUT without changes does not add REQUIRED_PRODUCTS_CHANGED history entry",
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ ordersApiService }) => {
        const before = orderObj!;

        const productIds = productIdsOf(before);
        const after = await ordersApiService.update(token, orderId, {
          customer: before.customer._id,
          products: productIds,
        });

        const beforeCount = before.history.filter(
          (h) => h.action === ORDER_HISTORY_ACTIONS.REQUIRED_PRODUCTS_CHANGED,
        ).length;
        const afterCount = after.history.filter(
          (h) => h.action === ORDER_HISTORY_ACTIONS.REQUIRED_PRODUCTS_CHANGED,
        ).length;
        expect.soft(afterCount).toBe(beforeCount);
      },
    );
  });

  test.describe("[Should NOT update order]", () => {
    for (const testCase of updateOrderErrorCases) {
      test(testCase.title, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, async ({ ordersApi }) => {
        const order = orderObj!;

        // Determine parameters based on test case
        const updateOrderId = testCase.orderId || orderId;
        const updateCustomerId = testCase.customerId || order.customer._id;
        const updateProducts = testCase.invalidProductId
          ? [testCase.invalidProductId]
          : testCase.shouldHaveProducts
            ? [order.products[0]!._id]
            : [];

        // Skip token for auth test
        const updateToken = testCase.title.includes("without token") ? "" : token;

        const response = await ordersApi.update(updateToken, updateOrderId, {
          customer: updateCustomerId,
          products: updateProducts,
        });

        validateResponse(response, {
          status: testCase.expectedStatus,
          IsSuccess: testCase.isSuccess,
          ErrorMessage: testCase.expectedErrorMessage,
        });
      });
    }
  });
});
