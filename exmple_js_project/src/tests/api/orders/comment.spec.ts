import { IOrderFromResponse } from "data/types/order.types";
import { expect, test } from "fixtures";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import {
  commentOrderPositiveCases,
  commentOrderNegativeCases,
  deleteOrderCommentPositiveCases,
  deleteOrderCommentNegativeCases,
} from "data/salesPortal/orders/commentOrderTestData";
import { TAGS } from "data/tags";

test.describe("[API][Orders][Comment]", () => {
  let token = "";
  let order: IOrderFromResponse;

  test.beforeAll(async ({ loginApiService, ordersApiService }) => {
    token = await loginApiService.loginAsAdmin();
    order = await ordersApiService.createOrderAndEntities(token, 1);
  });

  test.afterAll(async ({ ordersApiService }) => {
    if (order) {
      await ordersApiService.fullDelete(token);
    }
  });

  test.describe("Create", () => {
    for (const testCase of commentOrderPositiveCases) {
      test(testCase.title, { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, async ({ ordersApi }) => {
        const response = await ordersApi.addComment(token, order._id, testCase.text!);
        validateResponse(response, {
          status: testCase.expectedStatus,
          IsSuccess: testCase.isSuccess as boolean,
          ErrorMessage: testCase.expectedErrorMessage,
          schema: getOrderSchema,
        });
        const comment = response.body.Order.comments.find((c) => c.text === testCase.text);
        expect(comment).toBeDefined();
      });
    }
  });

  test.describe("Not create", () => {
    for (const testCase of commentOrderNegativeCases) {
      test(testCase.title, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, async ({ ordersApi }) => {
        const response = await ordersApi.addComment(token, order._id, testCase.text!);
        validateResponse(response, {
          status: testCase.expectedStatus,
          IsSuccess: testCase.isSuccess as boolean,
        });
      });
    }
  });

  test.describe("Delete", () => {
    for (const testCase of deleteOrderCommentPositiveCases) {
      test(
        testCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
        async ({ ordersApi, ordersApiService }) => {
          const comment = await ordersApiService.addComment(token, order._id);
          const response = await ordersApi.deleteComment(token, order._id, comment!._id);
          validateResponse(response, {
            status: testCase.expectedStatus,
          });
        },
      );
    }
  });

  test.describe("Not delete", () => {
    for (const testCase of deleteOrderCommentNegativeCases) {
      test(testCase.title, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] }, async ({ ordersApi }) => {
        const response = await ordersApi.deleteComment(token, order._id, testCase._id!);
        validateResponse(response, {
          status: testCase.expectedStatus,
        });
      });
    }
  });
});
