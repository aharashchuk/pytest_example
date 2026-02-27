import { generateProductData } from "data/salesPortal/products/generateProductData";
import { ICreateProductCase } from "data/types/product.types";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { faker } from "@faker-js/faker";
import _ from "lodash";

export const createProductPositiveCases: ICreateProductCase[] = [
  {
    title: "Create product with 3 character length in name",
    productData: generateProductData({ name: faker.string.alphanumeric({ length: 3 }) }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 40 character length in name",
    productData: generateProductData({ name: faker.string.alphanumeric({ length: 40 }) }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 1 space in name",
    productData: generateProductData({ name: `Test Product` }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 1 price",
    productData: generateProductData({ price: 1 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 99999 price",
    productData: generateProductData({ price: 99999 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 0 amount",
    productData: generateProductData({ amount: 0 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 999 amount",
    productData: generateProductData({ amount: 999 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with 250 notes",
    productData: generateProductData({ notes: faker.string.alphanumeric({ length: 250 }) }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product without notes",
    productData: _.omit(generateProductData(), "notes"),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create product with empty notes",
    productData: generateProductData({ notes: "" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const createProductNegativeCases: ICreateProductCase[] = [
  {
    title: "2 character name product not created",
    productData: generateProductData({ name: faker.string.alphanumeric({ length: 2 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "41 character name product not created",
    productData: generateProductData({ name: faker.string.alphanumeric({ length: 41 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Name with 2 spaces product not created",
    productData: generateProductData({ name: "Test  Product" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Name with special characters product not created",
    productData: generateProductData({ name: faker.string.alphanumeric({ length: 10 }) + "@#$%" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Product without name not created",
    productData: _.omit(generateProductData(), "name"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Empty name product not created",
    productData: generateProductData({ name: "" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "0 price product not created",
    productData: generateProductData({ price: 0 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Without manufacturer product not created",
    productData: _.omit(generateProductData(), "manufacturer"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "100000 price product not created",
    productData: generateProductData({ price: 100000 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Product without price not created",
    productData: _.omit(generateProductData(), "price"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Negative price product not created",
    productData: generateProductData({ price: -50 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Not integer price product not created",
    productData: generateProductData({ price: faker.string.alphanumeric({ length: 5 }) as unknown as number }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Negative amount product not created",
    productData: generateProductData({ amount: -10 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "1000 amount product not created",
    productData: generateProductData({ amount: 1000 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Product without amount not created",
    productData: _.omit(generateProductData(), "amount"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Not integer amount product not created",
    // @ts-expect-error: intentionally pass a non-integer string as amount to validate server-side input rejection
    productData: generateProductData({ amount: faker.string.alphanumeric({ length: 3 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "251 notes product not created",
    productData: generateProductData({ notes: faker.string.alphanumeric({ length: 251 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Notes with < or > symbols product not created",
    productData: generateProductData({ notes: "Invalid notes with <symbol>" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
];
