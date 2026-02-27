import {
  CREATE_CUSTOMER_NEGATIVE_CASES,
  CREATE_CUSTOMER_POSITIVE_CASES,
} from "data/salesPortal/customers/createCustomerTestData";
import { STATUS_CODES } from "data/statusCodes";
import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import { validateResponse } from "utils/validation/validateResponse.utils";
import _ from "lodash";
import { createCustomerSchema } from "data/schemas/customers/create.schema";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { generateCustomerData } from "data/salesPortal/customers/generateCustomerData";
import { buildDuplicatePayload } from "data/salesPortal/customers/buildDuplicatePayload";
import { ICustomer } from "data/types/customer.types";

test.describe("[API][Customers][Create Customer]", () => {
  let id = "";
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ customersApiService }) => {
    if (id) await customersApiService.delete(token, id);
    id = "";
  });

  test.describe("Positive DDT", () => {
    for (const tc of CREATE_CUSTOMER_POSITIVE_CASES) {
      test(
        tc.title,
        {
          tag: [TAGS.REGRESSION, TAGS.API, TAGS.CUSTOMERS],
        },
        async ({ customersApi }) => {
          const customerData = tc.customerData;
          const createdCustomer = await customersApi.create(token, customerData as ICustomer);
          validateResponse(createdCustomer, {
            status: STATUS_CODES.CREATED,
            schema: createCustomerSchema,
            IsSuccess: true,
            ErrorMessage: null,
          });

          id = createdCustomer.body.Customer._id;

          const actualCustomerData = createdCustomer.body.Customer;
          expect(_.omit(actualCustomerData, ["_id", "createdOn"])).toEqual(customerData);
        },
      );
    }
  });

  test.describe("Negative DDT", () => {
    for (const tc of CREATE_CUSTOMER_NEGATIVE_CASES) {
      test(
        tc.title,
        {
          tag: [TAGS.API, TAGS.CUSTOMERS],
        },
        async ({ customersApi }) => {
          const customerData = tc.customerData;
          const createdCustomer = await customersApi.create(token, customerData as ICustomer);
          validateResponse(createdCustomer, {
            status: STATUS_CODES.BAD_REQUEST,
            IsSuccess: false,
            ErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
          });
        },
      );
    }
  });
  test.describe("Unique email", () => {
    test(
      "Should NOT create customer with existing email",
      { tag: [TAGS.API, TAGS.REGRESSION, TAGS.CUSTOMERS] },
      async ({ customersApi }) => {
        const initial = generateCustomerData();
        const createResponse = await customersApi.create(token, initial);

        validateResponse(createResponse, {
          status: STATUS_CODES.CREATED,
          IsSuccess: true,
          ErrorMessage: null,
        });

        const createdCustomer = createResponse.body.Customer;
        id = createdCustomer._id;

        const duplicatePayload = buildDuplicatePayload(createdCustomer);

        const dupResponse = await customersApi.create(token, duplicatePayload);

        validateResponse(dupResponse, {
          status: STATUS_CODES.CONFLICT,
          IsSuccess: false,
        });
      },
    );
  });
});
