import { test, expect } from "fixtures/api.fixture";
import { STATUS_CODES } from "data/statusCodes";
import { TAGS } from "data/tags";
import { generateCustomerData } from "data/salesPortal/customers/generateCustomerData";

test.describe("CST-008/009 Delete customer", () => {
  let token: string;

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });
  test(
    "CST-008: Delete customer (Valid Id)",
    { tag: [TAGS.API, TAGS.CUSTOMERS, TAGS.SMOKE] },
    async ({ customersApiService, customersApi }) => {
      const created = await customersApiService.create(token, generateCustomerData());
      const id = created._id;

      await customersApiService.delete(token, id);

      const afterDelete = await customersApi.getById(token, id);
      expect(afterDelete.status).toBe(STATUS_CODES.NOT_FOUND);
    },
  );

  test(
    "CST-009: Delete customer (Invalid Id)",
    { tag: [TAGS.API, TAGS.CUSTOMERS, TAGS.REGRESSION] },
    async ({ loginApiService, customersApi }) => {
      const token = await loginApiService.loginAsAdmin();
      const invalidId = "507f1f77bcf86cd799439011";

      const response = await customersApi.delete(token, invalidId);
      expect(response.status).toBe(STATUS_CODES.NOT_FOUND);
    },
  );
});
