import { test, expect } from "fixtures/api.fixture";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { TAGS } from "data/tags";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import {
  RECEIVE_PRODUCTS_INVALID_PAYLOAD_CASES,
  RECEIVE_PRODUCTS_NEGATIVE_STATUS_CASES,
  RECEIVE_PRODUCTS_POSITIVE_CASES,
} from "data/salesPortal/orders/receiveDDT";
import { STATUS_CODES } from "data/statusCodes";

test.describe("[API][Orders][Receive]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    if (token) await ordersApiService.fullDelete(token);
  });

  test.describe("[Positive][Receive order]", () => {
    for (const positiveCase of RECEIVE_PRODUCTS_POSITIVE_CASES) {
      test(
        positiveCase.title,
        { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
        async ({ ordersApiService, ordersApi }) => {
          const order = await ordersApiService.createOrderInProcess(token, positiveCase.orderProductsCount);
          expect(order.status).toBe(ORDER_STATUS.PROCESSING);

          const productIdsToReceive = order.products
            .slice(0, positiveCase.receiveProductsCount)
            .map((product) => product._id);

          const response = await ordersApi.receiveProducts(order._id, productIdsToReceive, token);
          validateResponse(response, {
            status: STATUS_CODES.OK,
            IsSuccess: true,
            ErrorMessage: null,
            schema: getOrderSchema,
          });

          expect(response.body.Order.status).toBe(positiveCase.expectedOrderStatus);

          const receivedIds = new Set(productIdsToReceive);
          for (const product of response.body.Order.products) {
            if (receivedIds.has(product._id)) {
              expect(product.received).toBe(true);
            }
          }
        },
      );
    }
  });

  test.describe("[Negative][Incorrect order status to receive]", () => {
    for (const negativeCase of RECEIVE_PRODUCTS_NEGATIVE_STATUS_CASES) {
      test(
        `Should NOT receive products: ${negativeCase.title}`,
        { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
        async ({ ordersApiService, ordersApi }) => {
          const order = await negativeCase.create(ordersApiService, token);
          const expectedErrorMessage =
            typeof negativeCase.expectedErrorMessage === "function"
              ? negativeCase.expectedErrorMessage(order)
              : negativeCase.expectedErrorMessage;
          const productIdsToReceive = order.products
            .slice(0, negativeCase.receiveProductsCount)
            .map((product) => product._id);

          const response = await ordersApi.receiveProducts(order._id, productIdsToReceive, token);
          validateResponse(response, {
            status: negativeCase.expectedStatus,
            IsSuccess: false,
            ErrorMessage: expectedErrorMessage,
          });
        },
      );
    }
  });

  test.describe("[Negative][Invalid request body]", () => {
    for (const negativeCase of RECEIVE_PRODUCTS_INVALID_PAYLOAD_CASES) {
      test(
        `Should NOT receive products: ${negativeCase.title}`,
        { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
        async ({ ordersApiService, ordersApi }) => {
          const order = await ordersApiService.createOrderInProcess(token, 5);
          const products = negativeCase.buildProducts(order);

          const response = await ordersApi.receiveProducts(order._id, products, token);
          validateResponse(response as any, {
            status: negativeCase.expectedStatus,
            IsSuccess: false,
            ErrorMessage: negativeCase.expectedErrorMessage,
          });
        },
      );
    }
  });
});
