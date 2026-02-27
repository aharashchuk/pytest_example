import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import {
  invalidStatusesCases,
  negativeOrderStatusTransitions,
  positiveOrderStatusTransitions,
} from "data/salesPortal/orders/ordersStatusDDT";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import { STATUS_CODES } from "data/statusCodes";
import { TAGS } from "data/tags";
import { expect, test } from "fixtures";
import { validateResponse } from "utils/validation/validateResponse.utils";
test.describe("[API][Orders][Positive Orders statuses transition]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    await ordersApiService.fullDelete(token);
  });

  for (const orderCase of positiveOrderStatusTransitions) {
    test(
      "Order status transition from " + orderCase.from + " to " + orderCase.to,
      { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ ordersApiService, ordersApi }) => {
        const order = await orderCase.create(ordersApiService, token);
        const response = await ordersApi.updateStatus(order._id, orderCase.to, token);
        validateResponse(response, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        const updatedStatus = response.body.Order.status;
        expect(updatedStatus).not.toBeNull();
        expect(updatedStatus).toBe(orderCase.to);
      },
    );
  }
});

test.describe("[API][Orders][Negative Orders statuses transition]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    await ordersApiService.fullDelete(token);
  });

  for (const orderCase of negativeOrderStatusTransitions) {
    test(
      "Order status transition from " + orderCase.from + " to " + orderCase.to,
      { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ ordersApiService, ordersApi }) => {
        const order = await orderCase.create(ordersApiService, token);
        const response = await ordersApi.updateStatus(order._id, orderCase.to, token);
        validateResponse(response, {
          status: orderCase.expectedStatus,
          IsSuccess: orderCase.isSuccess as boolean,
          ErrorMessage: orderCase.expectedErrorMessage,
        });
      },
    );
  }
});

test.describe("[API][Orders][Invalid Orders statuses]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    await ordersApiService.fullDelete(token);
  });

  invalidStatusesCases.forEach((invalidStatus) => {
    test(
      `Order status transition from Draft to ${String(invalidStatus)}`,
      { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
      async ({ ordersApiService, ordersApi }) => {
        const order = await ordersApiService.createOrderAndEntities(token, 1);
        const response = await ordersApi.updateStatus(order._id, invalidStatus as any, token);
        expect(response.status).toBe(STATUS_CODES.BAD_REQUEST);
        expect(response.body.IsSuccess).toBe(false);
        expect(response.body.ErrorMessage).toBe(`Incorrect request body`);
      },
    );
  });

  test(
    "Should NOT change order status with non-existing orderId",
    { tag: [TAGS.API, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApi, ordersApiService }) => {
      await ordersApiService.createOrderAndEntities(token, 1);
      const response = await ordersApi.updateStatus("000000000000000000000000", ORDER_STATUS.DRAFT, token);
      validateResponse(response, {
        status: STATUS_CODES.NOT_FOUND,
        IsSuccess: false,
        ErrorMessage: RESPONSE_ERRORS.ORDER_NOT_FOUND("000000000000000000000000"),
      });
    },
  );
});
