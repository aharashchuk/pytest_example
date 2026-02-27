import { test } from "fixtures/api.fixture";
import { TAGS } from "data/tags";
import { validateJsonSchema } from "utils/validation/validateSchema.utils";
import { getAllCustomersSchema } from "data/schemas/customers/getAllCustomers.schema";

test.describe("CST-010 Get ALL customers (Technical endpoint)", () => {
  test(
    "CST-010: GET /api/customers/all returns array of customers",
    { tag: [TAGS.API, TAGS.CUSTOMERS, TAGS.SMOKE] },
    async ({ loginApiService, customersApiService }) => {
      const token = await loginApiService.loginAsAdmin();
      const customers = await customersApiService.getAll(token);

      validateJsonSchema({ Customers: customers, IsSuccess: true, ErrorMessage: null }, getAllCustomersSchema);
    },
  );
});
