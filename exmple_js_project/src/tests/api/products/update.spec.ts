import { test, expect } from "fixtures/api.fixture";
import { generateProductData } from "data/salesPortal/products/generateProductData";
import { createProductSchema } from "data/schemas/products/create.schema";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { validateResponse } from "utils/validation/validateResponse.utils";
import {
  updateProductPositiveCases,
  updateProductInvalidIdCases,
  updateProductNegativeCases,
} from "data/salesPortal/products/updateProductTestData";
import { TAGS } from "data/tags";

test.describe("[API][Products]", () => {
  let id = "";
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.afterEach(async ({ productsApiService }) => {
    if (id) await productsApiService.delete(token, id);
  });

  test.describe("[Update product]", () => {
    for (const testCase of updateProductPositiveCases) {
      test(
        testCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
        async ({ productsApiService, productsApi }) => {
          const createdProduct = await productsApiService.create(token);
          id = createdProduct._id;

          const updatedProductData = { ...createdProduct, ...testCase.productData! };
          const updatedProductResponse = await productsApi.update(id, updatedProductData, token);

          validateResponse(updatedProductResponse, {
            status: testCase.expectedStatus,
            schema: createProductSchema,
            IsSuccess: testCase.isSuccess as boolean,
            ErrorMessage: testCase.expectedErrorMessage,
          });

          const updatedProduct = updatedProductResponse.body.Product;
          expect.soft(updatedProduct).toEqual(updatedProductData);
          expect.soft(id).toBe(updatedProduct._id);
        },
      );
    }
  });

  test.describe("[Should NOT update product]", () => {
    for (const testCase of updateProductNegativeCases) {
      test(
        testCase.title,
        { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
        async ({ productsApiService, productsApi }) => {
          const createdProduct = await productsApiService.create(token);
          id = createdProduct._id;

          const updatedProductData = { ...createdProduct, ...testCase.productData! };
          const updatedProductResponse = await productsApi.update(id, updatedProductData, token);

          validateResponse(updatedProductResponse, {
            status: testCase.expectedStatus,
            IsSuccess: testCase.isSuccess as boolean,
            ErrorMessage: testCase.expectedErrorMessage,
          });
        },
      );
    }
  });

  test.describe("[Should NOT find product to update]", () => {
    for (const testCase of updateProductInvalidIdCases) {
      test(
        testCase.title,
        { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
        async ({ productsApiService, productsApi }) => {
          const createdProduct = await productsApiService.create(token);
          id = createdProduct._id;

          const updatedProductData = generateProductData();
          const updatedProductResponse = await productsApi.update(testCase.id!, updatedProductData, token);

          validateResponse(updatedProductResponse, {
            status: testCase.expectedStatus,
            IsSuccess: testCase.isSuccess as boolean,
            ErrorMessage: testCase.expectedErrorMessage,
          });
        },
      );
    }
  });

  test.describe("Should NOT update with existing name", () => {
    test(
      "Attempt to update product name with existing one returns error",
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
      async ({ productsApi, productsApiService }) => {
        const firstProductData = generateProductData();
        const secondProductData = generateProductData();
        const firstCreatedProduct = await productsApi.create(firstProductData, token);
        const secondCreatedProduct = await productsApi.create(secondProductData, token);
        validateResponse(firstCreatedProduct, {
          status: STATUS_CODES.CREATED,
          schema: createProductSchema,
          IsSuccess: true,
          ErrorMessage: null,
        });

        id = firstCreatedProduct.body.Product._id;
        const secondProductId = secondCreatedProduct.body.Product._id;

        firstProductData["name"] = secondProductData.name;
        const updatedProductResponse = await productsApi.update(id, firstProductData, token);
        await productsApiService.delete(token, secondProductId);
        validateResponse(updatedProductResponse, {
          status: STATUS_CODES.CONFLICT,
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.CONFLICT(secondProductData.name),
        });
      },
    );
  });
});
