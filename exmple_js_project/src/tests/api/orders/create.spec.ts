import { IOrderCreateBody } from "data/types/order.types";
import { test } from "fixtures";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { CREATE_ORDER_NEGATIVE_CASES, CREATE_ORDER_POSITIVE_CASES } from "data/salesPortal/orders/createOrderTestData";
import { TAGS } from "data/tags";
import { TIMEOUT_30_S } from "data/salesPortal/constants";
import { createOrderSchema } from "data/schemas/orders/create.schema";
test.setTimeout(TIMEOUT_30_S);

test.describe("[API][Orders][Create Order]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ ordersApiService }) => {
    await ordersApiService.fullDelete(token);
  });

  test.describe("Positive DDT", () => {
    for (const positiveCase of CREATE_ORDER_POSITIVE_CASES) {
      test(
        positiveCase.title,
        { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
        async ({ ordersApi, ordersApiService }) => {
          const { customerId, productIds } = await ordersApiService.createCustomerAndProducts(
            token,
            positiveCase.productsCount,
          );
          const payload: IOrderCreateBody = {
            customer: customerId,
            products: productIds,
          };
          const createOrderResponse = await ordersApi.create(token, payload);
          const orderId = createOrderResponse.body?.Order?._id ?? "";
          if (orderId) ordersApiService.trackOrderId(orderId);
          validateResponse(createOrderResponse, {
            status: positiveCase.expectedStatus,
            schema: createOrderSchema,
            IsSuccess: positiveCase.isSuccess as boolean,
            ErrorMessage: positiveCase.expectedErrorMessage,
          });
        },
      );
    }
  });

  test.describe("Negative DDT", () => {
    for (const negativeCase of CREATE_ORDER_NEGATIVE_CASES) {
      test(negativeCase.title, { tag: [TAGS.API, TAGS.ORDERS] }, async ({ ordersApi, ordersApiService }) => {
        const { customerId, productIds } = await ordersApiService.createCustomerAndProducts(
          token,
          negativeCase.productsCount,
        );
        const payload: IOrderCreateBody = {
          customer: customerId,
          products: productIds,
          ...negativeCase.orderData,
        };

        const createOrderResponse = await ordersApi.create(token, payload);
        const orderId = createOrderResponse.body?.Order?._id ?? "";
        if (orderId) ordersApiService.trackOrderId(orderId);
        validateResponse(createOrderResponse, {
          status: negativeCase.expectedStatus,
          IsSuccess: negativeCase.isSuccess as boolean,
          ErrorMessage: negativeCase.expectedErrorMessage,
        });
      });
    }
  });
});
