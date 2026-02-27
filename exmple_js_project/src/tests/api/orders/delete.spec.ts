import { test } from "fixtures";
import { STATUS_CODES } from "data/statusCodes";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { TAGS } from "data/tags";
import { DELETE_ORDER_CASES } from "data/salesPortal/orders/createOrderTestData";
import { TIMEOUT_30_S } from "data/salesPortal/constants";
test.setTimeout(TIMEOUT_30_S);

test.describe("[API][Orders][Delete Order]", () => {
  let token = "";
  let customerId = "";
  let productIds: string[] = [];

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.beforeEach(() => {
    customerId = "";
    productIds = [];
  });

  test.afterEach(async ({ customersApiService, productsApiService }) => {
    await Promise.allSettled(productIds.map((id) => productsApiService.delete(token, id)));
    if (customerId) await customersApiService.delete(token, customerId);
  });

  for (const positiveCase of DELETE_ORDER_CASES) {
    test(
      positiveCase.title,
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.ORDERS] },
      async ({ ordersApi, ordersApiService }) => {
        const order = await ordersApiService.createOrderAndEntities(token, positiveCase.productsCount);
        customerId = order.customer._id;
        productIds = order.products.map((product) => product._id);
        const deleteOrderResponse = await ordersApi.delete(token, order._id);
        validateResponse(deleteOrderResponse, {
          status: STATUS_CODES.DELETED,
        });
      },
    );
  }
});
