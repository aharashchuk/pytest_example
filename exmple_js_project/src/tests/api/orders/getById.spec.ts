import { test, expect } from "fixtures/api.fixture";
import { getOrderByIdPositiveCases, getOrderByIdNegativeCases } from "data/salesPortal/orders/getOrderByIdTestData";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { TAGS } from "data/tags";

test.describe("[API] [Sales Portal] [Orders] [Get By Id]", () => {
  let token = "";
  let orderId = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.describe("[Positive]", () => {
    for (const testCase of getOrderByIdPositiveCases) {
      test(
        testCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
        async ({ ordersApiService, ordersApi }) => {
          // Preconditions
          const createdOrder = await ordersApiService.createOrderAndEntities(token, 1);
          orderId = createdOrder._id;

          // Action
          const response = await ordersApi.getById(orderId, token);

          // Assert
          validateResponse(response, {
            status: testCase.expectedStatus,
            ...(typeof testCase.isSuccess !== "undefined" && { IsSuccess: testCase.isSuccess }),
            ErrorMessage: testCase.expectedErrorMessage,
            schema: getOrderSchema,
          });

          expect(response.body!.Order._id).toBe(orderId);
        },
      );
    }
  });

  test.describe("[Negative]", () => {
    for (const testCase of getOrderByIdNegativeCases) {
      test(testCase.title ?? "No title", { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, async ({ ordersApi }) => {
        const response = await ordersApi.getById(testCase._id!, token);

        validateResponse(response, {
          status: testCase.expectedStatus,
          ...(typeof testCase.isSuccess !== "undefined" && { IsSuccess: testCase.isSuccess }),
          ErrorMessage: testCase.expectedErrorMessage,
        });
      });
    }
  });
});
