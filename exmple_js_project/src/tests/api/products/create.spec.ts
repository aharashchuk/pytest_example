import { test, expect } from "fixtures/api.fixture";
import { generateProductData } from "data/salesPortal/products/generateProductData";
import { createProductSchema } from "data/schemas/products/create.schema";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import _ from "lodash";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { IProduct } from "data/types/product.types";
import {
  createProductPositiveCases,
  createProductNegativeCases,
} from "data/salesPortal/products/createProductTestData";
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

  test.describe("[Create product]", () => {
    for (const positiveCase of createProductPositiveCases) {
      test(
        positiveCase.title,
        { tag: [TAGS.SMOKE, TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
        async ({ productsApi }) => {
          const createdProduct = await productsApi.create(positiveCase.productData as IProduct, token);
          validateResponse(createdProduct, {
            status: positiveCase.expectedStatus,
            schema: createProductSchema,
            IsSuccess: positiveCase.isSuccess as boolean,
            ErrorMessage: positiveCase.expectedErrorMessage,
          });

          id = createdProduct.body.Product._id;

          const actualProductData = createdProduct.body.Product;
          expect(_.omit(actualProductData, ["_id", "createdOn"])).toEqual(positiveCase.productData);
        },
      );
    }
  });

  test.describe("[Should NOT create product]", () => {
    for (const negativeCase of createProductNegativeCases) {
      test(`${negativeCase.title}`, { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] }, async ({ productsApi }) => {
        const createdProduct = await productsApi.create(negativeCase.productData as IProduct, token);
        validateResponse(createdProduct, {
          status: negativeCase.expectedStatus,
          IsSuccess: negativeCase.isSuccess as boolean,
          ErrorMessage: negativeCase.expectedErrorMessage,
        });
      });
    }
  });

  test.describe("Should NOT create duplicate product", () => {
    test(
      "Attempt to create duplicate product returns error",
      { tag: [TAGS.REGRESSION, TAGS.API, TAGS.PRODUCTS] },
      async ({ productsApi }) => {
        const productData = generateProductData();
        const firstCreatedProduct = await productsApi.create(productData, token);
        validateResponse(firstCreatedProduct, {
          status: STATUS_CODES.CREATED,
          schema: createProductSchema,
          IsSuccess: true,
          ErrorMessage: null,
        });

        id = firstCreatedProduct.body.Product._id;

        const duplicateCreatedProduct = await productsApi.create(productData, token);
        validateResponse(duplicateCreatedProduct, {
          status: STATUS_CODES.CONFLICT,
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.CONFLICT(productData.name),
        });
      },
    );
  });
});
