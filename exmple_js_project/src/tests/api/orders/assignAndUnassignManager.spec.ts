import { getOrderSchema } from "data/schemas/orders/get.schema";
import { STATUS_CODES } from "data/statusCodes";
import { IOrderFromResponse } from "data/types/order.types";
import { expect, test } from "fixtures";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { TAGS } from "data/tags";
import { assignUnassignManagerNegativeCases, orderInStatus } from "data/salesPortal/orders/assignUnassignManagerDDT";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { MANAGER_IDS } from "config/env";

test.describe("[API][Orders][Manager assignment flow]", () => {
  let token = "";
  let order: IOrderFromResponse;
  const firstManagerId: string = MANAGER_IDS[0]!;
  const secondManagerId: string = MANAGER_IDS[1]!;

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  for (const orderCase of orderInStatus) {
    test.describe(`Order in ${orderCase.name} status`, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, () => {
      test.beforeEach(async ({ ordersApiService }) => {
        order = await orderCase.create(ordersApiService, token);
      });

      test.afterEach(async ({ ordersApiService }) => {
        await ordersApiService.fullDelete(token);
      });

      test("Assign manager to order", async ({ ordersApi }) => {
        const response = await ordersApi.assingManager(token, order._id, firstManagerId);
        validateResponse(response, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        const assignedManager = response.body.Order.assignedManager;
        expect(assignedManager).not.toBeNull();
        expect(assignedManager!._id).toBe(firstManagerId);
      });

      test("Update manager to another manager", async ({ ordersApi }) => {
        await ordersApi.assingManager(token, order._id, firstManagerId);
        const response = await ordersApi.assingManager(token, order._id, secondManagerId);
        validateResponse(response, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        const assignedManager = response.body.Order.assignedManager;
        expect(assignedManager).not.toBeNull();
        expect(assignedManager!._id).toBe(secondManagerId);
      });

      test("Remove manager from order", async ({ ordersApi }) => {
        await ordersApi.assingManager(token, order._id, firstManagerId);
        const response = await ordersApi.unassingManager(token, order._id);
        validateResponse(response, {
          status: STATUS_CODES.OK,
          IsSuccess: true,
          ErrorMessage: null,
          schema: getOrderSchema,
        });
        const assignedManager = response.body.Order.assignedManager;
        expect(assignedManager).toBeNull();
      });
    });
  }
});

test.describe("[API][Orders][Assign/Unassign Manager - Negative DDT]", () => {
  let token = "";
  let order: IOrderFromResponse;
  const firstManagerId: string = MANAGER_IDS[0]!;

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  for (const orderCase of orderInStatus) {
    test.describe(`Order in ${orderCase.name} status`, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, () => {
      test.beforeEach(async ({ ordersApiService }) => {
        order = await orderCase.create(ordersApiService, token);
      });

      test.afterEach(async ({ ordersApiService }) => {
        if (order) await ordersApiService.deleteOrderAndEntities(token, order._id);
      });

      for (const negativeCase of assignUnassignManagerNegativeCases) {
        test(`Should NOT assign ${negativeCase.title}`, async ({ ordersApi }) => {
          const response = await ordersApi.assingManager(
            token,
            negativeCase.orderId(order._id),
            negativeCase.managerId(firstManagerId),
          );
          validateResponse(response, negativeCase.expected);
        });
        test(`Should NOT update ${negativeCase.title}`, async ({ ordersApi }) => {
          await ordersApi.assingManager(token, order._id, firstManagerId);
          const response = await ordersApi.assingManager(
            token,
            negativeCase.orderId(order._id),
            negativeCase.managerId(firstManagerId),
          );
          validateResponse(response, negativeCase.expected);
          const orderBody = await ordersApi.getById(order._id, token);
          expect(orderBody.body.Order.assignedManager).not.toBeNull();
          expect(orderBody.body.Order.assignedManager!._id).toBe(firstManagerId);
        });
      }

      test("Should NOT unassign manager from order with non-existing orderId", async ({ ordersApi }) => {
        await ordersApi.assingManager(token, order._id, firstManagerId);
        const response = await ordersApi.unassingManager(token, "000000000000000000000000");
        validateResponse(response, {
          status: STATUS_CODES.NOT_FOUND,
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.ORDER_NOT_FOUND("000000000000000000000000"),
        });
      });
    });
  }
});
