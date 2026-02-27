import { test, expect } from "fixtures/api.fixture";
import { generateCustomerData } from "data/salesPortal/customers/generateCustomerData";
import { validateResponse } from "utils/validation/validateResponse.utils";
import {
  updateCustomerPositiveCases,
  updateCustomerInvalidIdCases,
  updateCustomerNegativeCases,
} from "data/salesPortal/customers/updateCustomerTestData";
import { TAGS } from "data/tags";

test.describe("[API][Customers]", () => {
  let id = "";
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.describe("[Update customer]", () => {
    for (const testCase of updateCustomerPositiveCases) {
      test(
        testCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.CUSTOMERS] },
        async ({ customersApiService, cleanup }) => {
          const createdCustomer = await customersApiService.create(token);
          id = createdCustomer._id;
          cleanup.addCustomer(id);

          const updatedCustomerData = { ...createdCustomer, ...testCase.customerData! };
          const updatedCustomer = await customersApiService.update(token, id, updatedCustomerData);
          expect.soft(updatedCustomer).toEqual(updatedCustomerData);
          expect.soft(updatedCustomer._id).toBe(id);
        },
      );
    }
  });

  test.describe("[Should NOT update customer]", () => {
    for (const testCase of updateCustomerNegativeCases) {
      test(
        testCase.title,
        { tag: [TAGS.REGRESSION, TAGS.API, TAGS.CUSTOMERS] },
        async ({ customersApiService, customersApi, cleanup }) => {
          const createdCustomer = await customersApiService.create(token);
          id = createdCustomer._id;
          cleanup.addCustomer(id);

          const updatedCustomerData = { ...createdCustomer, ...testCase.customerData! };
          const updatedCustomerResponse = await customersApi.update(token, id, updatedCustomerData);

          validateResponse(updatedCustomerResponse, {
            status: testCase.expectedStatus,
            IsSuccess: testCase.isSuccess as boolean,
            ErrorMessage: testCase.expectedErrorMessage,
          });
        },
      );
    }
  });

  test.describe("[Should NOT find customer to update]", () => {
    for (const testCase of updateCustomerInvalidIdCases) {
      test(
        testCase.title,
        { tag: [TAGS.REGRESSION, TAGS.API, TAGS.CUSTOMERS] },
        async ({ customersApiService, customersApi, cleanup }) => {
          const createdCustomer = await customersApiService.create(token);
          id = createdCustomer._id;
          cleanup.addCustomer(id);

          const updatedCustomerData = generateCustomerData();
          const updatedCustomerResponse = await customersApi.update(token, testCase.id!, updatedCustomerData);

          validateResponse(updatedCustomerResponse, {
            status: testCase.expectedStatus,
            IsSuccess: testCase.isSuccess as boolean,
            ErrorMessage: testCase.expectedErrorMessage,
          });
        },
      );
    }
  });
});
