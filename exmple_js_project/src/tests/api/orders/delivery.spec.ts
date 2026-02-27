import { test, expect } from "fixtures/api.fixture";
import { validateResponse } from "utils/validation/validateResponse.utils";
import {
  CREATE_DELIVERY_POSITIVE_CASES,
  CREATE_DELIVERY_NEGATIVE_CASES,
} from "data/salesPortal/orders/createDeliveryDDT";
import { IDeliveryInfo } from "data/salesPortal/delivery-status";
import { IOrderFromResponse } from "data/types/order.types";
import { TAGS } from "data/tags";
import { getOrderSchema } from "data/schemas/orders/get.schema";
import { convertToDate } from "utils/date.utils";

test.describe("[API][Orders][Delivery]", () => {
  let token: string;
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

  test.describe("[Add Delivery Info]", () => {
    for (const [index, positiveCase] of CREATE_DELIVERY_POSITIVE_CASES.entries()) {
      test(
        `${positiveCase.title} [${index}]`,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
        async ({ ordersApi }) => {
          const addDeliveryResponse = await ordersApi.addDelivery(
            token,
            order._id,
            positiveCase.deliveryData as unknown as IDeliveryInfo,
          );
          validateResponse(addDeliveryResponse, {
            status: positiveCase.expectedStatus,
            schema: getOrderSchema,
            IsSuccess: true,
            ErrorMessage: positiveCase.expectedErrorMessage,
          });
          const actualDeliveryData = addDeliveryResponse.body.Order.delivery;

          expect(actualDeliveryData).not.toBeNull();

          const normalizedActualData = {
            ...actualDeliveryData!,
            finalDate: convertToDate(actualDeliveryData!.finalDate),
          };

          expect(normalizedActualData).toMatchObject(positiveCase.deliveryData);
        },
      );
    }

    test.describe("[Should NOT add Delivery Info]", () => {
      for (const [index, negativeCase] of CREATE_DELIVERY_NEGATIVE_CASES.entries()) {
        test(
          `${negativeCase.title} [${index}]`,
          { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
          async ({ ordersApi }) => {
            const addDeliveryResponse = await ordersApi.addDelivery(
              token,
              order._id,
              negativeCase.deliveryData as unknown as IDeliveryInfo,
            );
            validateResponse(addDeliveryResponse, {
              status: negativeCase.expectedStatus,
              IsSuccess: false,
              ErrorMessage: negativeCase.expectedErrorMessage,
            });
          },
        );
      }
    });
  });
});
