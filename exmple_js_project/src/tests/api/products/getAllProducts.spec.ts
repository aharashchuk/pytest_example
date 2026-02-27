import { test, expect } from "fixtures/api.fixture";
import {
  getAllProductsPositiveCases,
  getAllProductsNegativeCases,
} from "data/salesPortal/products/getAllProductsTestData";
import { getAllProductsSchema } from "data/schemas/products/getAllProducts.schema";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { TAGS } from "data/tags";

test.describe("[API] [Sales Portal] [Products] [Get All]", () => {
  let token: string;

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.describe("[Positive]", () => {
    for (const testCase of getAllProductsPositiveCases) {
      test(
        testCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
        async ({ productsApi, productsApiService }) => {
          const product1 = await productsApiService.create(token);
          const product2 = await productsApiService.create(token);
          const response = await productsApi.getAll(token);
          validateResponse(response, {
            status: testCase.expectedStatus,
            schema: getAllProductsSchema,
            ErrorMessage: testCase.expectedErrorMessage,
          });
          const ids = response.body.Products.map((p) => p._id);
          expect(ids).toContain(product1._id);
          expect(ids).toContain(product2._id);
          await productsApiService.delete(token, product1._id);
          await productsApiService.delete(token, product2._id);
        },
      );
    }
  });

  test.describe("[Negative]", () => {
    for (const testCase of getAllProductsNegativeCases) {
      test(testCase.title, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] }, async ({ productsApi }) => {
        const response = await productsApi.getAll("");

        validateResponse(response, {
          status: testCase.expectedStatus,
          ErrorMessage: testCase.expectedErrorMessage,
        });
      });
    }
  });
});
