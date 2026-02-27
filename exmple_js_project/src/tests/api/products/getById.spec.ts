import { test, expect } from "fixtures/api.fixture";
import {
  getProductByIdPositiveCases,
  getProductByIdNegativeCases,
} from "data/salesPortal/products/getProductByIdTestData";
import { getProductSchema } from "data/schemas/products/get.schema";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { TAGS } from "data/tags";

test.describe("[API] [Sales Portal] [Products] [Get By Id]", () => {
  let token: string;

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.describe("[Positive]", () => {
    for (const testCase of getProductByIdPositiveCases) {
      test(
        testCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
        async ({ productsApi, productsApiService }) => {
          const createdProduct = await productsApiService.create(token);
          const id = createdProduct._id;
          const response = await productsApi.getById(id, token);
          validateResponse(response, {
            status: testCase.expectedStatus,
            schema: getProductSchema,
            ErrorMessage: testCase.expectedErrorMessage,
          });
          expect(response.body.Product).toEqual(createdProduct);
          await productsApiService.delete(token, id);
        },
      );
    }
  });

  test.describe("[Negative]", () => {
    for (const testCase of getProductByIdNegativeCases) {
      test(testCase.title, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] }, async ({ productsApi }) => {
        const response = await productsApi.getById(testCase.id!, token);
        validateResponse(response, {
          status: testCase.expectedStatus,
          ErrorMessage: testCase.expectedErrorMessage,
        });
      });
    }
  });
});
