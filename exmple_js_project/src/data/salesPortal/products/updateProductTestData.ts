import { generateProductData } from "data/salesPortal/products/generateProductData";
import { ICreateProductCase } from "data/types/product.types";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { faker } from "@faker-js/faker";
import _ from "lodash";
import { ObjectId } from "bson";

export const updateProductPositiveCases: ICreateProductCase[] = [
  {
    title: "Update product name to 3 characters",
    productData: { name: faker.string.alphanumeric({ length: 3 }) },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update product name to 40 characters",
    productData: { name: faker.string.alphanumeric({ length: 40 }) },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update product name with 1 space",
    productData: { name: "Test" + faker.string.alphanumeric({ length: 5 }) },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update price to minimum (1)",
    productData: { price: 1 },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update price to maximum (99999)",
    productData: { price: 99999 },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update amount to minimum (0)",
    productData: { amount: 0 },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update amount to maximum (999)",
    productData: { amount: 999 },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update notes to 250 characters",
    productData: { notes: faker.string.alphanumeric({ length: 250 }) },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Clear notes (empty string)",
    productData: { notes: "" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update only manufacturer",
    productData: _.pick(generateProductData(), ["manufacturer"]),
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update full product data",
    productData: generateProductData(),
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const updateProductInvalidIdCases: ICreateProductCase[] = [
  {
    title: "404 returned for empty id",
    id: "",
    expectedStatus: STATUS_CODES.NOT_FOUND,
    get expectedErrorMessage() {
      return RESPONSE_ERRORS.PRODUCT_NOT_FOUND(this.id!);
    },
  },
  {
    title: "404 returned for non-existing id of valid format",
    id: new ObjectId().toHexString(),
    expectedStatus: STATUS_CODES.NOT_FOUND,
    get expectedErrorMessage() {
      return RESPONSE_ERRORS.PRODUCT_NOT_FOUND(this.id!);
    },
  },
  {
    title: "400 returned for id of invalid format",
    id: faker.string.alphanumeric({ length: 10 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];

export const updateProductNegativeCases: ICreateProductCase[] = [
  {
    title: "Update with 2 character name — bad request",
    productData: { name: faker.string.alphanumeric({ length: 2 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update with 41 character name — bad request",
    productData: { name: faker.string.alphanumeric({ length: 41 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update name with double spaces — bad request",
    productData: { name: "Test  Product" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update name with special characters — bad request",
    productData: { name: faker.string.alphanumeric({ length: 10 }) + "@#$%" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update price to 0 — bad request",
    productData: { price: 0 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update price to 100000 — bad request",
    productData: { price: 100000 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update price to negative value — bad request",
    productData: { price: -50 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update price with non-integer — bad request",
    productData: { price: faker.string.alphanumeric({ length: 5 }) as unknown as number },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update amount to negative — bad request",
    productData: { amount: -10 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update amount to 1000 — bad request",
    productData: { amount: 1000 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update amount with non-integer — bad request",
    // @ts-expect-error: intentionally provide non-integer to validate server-side input rejection
    productData: { amount: faker.string.alphanumeric({ length: 3 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update notes to 251 characters — bad request",
    productData: { notes: faker.string.alphanumeric({ length: 251 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
  {
    title: "Update notes with < or > — bad request",
    productData: { notes: "Invalid notes with <symbol>" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    isSuccess: false,
  },
];
