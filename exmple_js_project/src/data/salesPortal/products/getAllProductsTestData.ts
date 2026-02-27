import { ICreateProductCase } from "data/types/product.types";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";

export const getAllProductsPositiveCases: ICreateProductCase[] = [
  {
    title: "Should return list of all products",
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
];

export const getAllProductsNegativeCases: ICreateProductCase[] = [
  {
    title: "401 returned for request without token",
    expectedStatus: STATUS_CODES.UNAUTHORIZED,
    expectedErrorMessage: RESPONSE_ERRORS.UNAUTHORIZED,
  },
];
