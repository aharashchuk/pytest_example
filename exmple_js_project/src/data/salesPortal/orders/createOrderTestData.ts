import { STATUS_CODES } from "data/statusCodes";
import { ICreateOrderCase, ICreateOrderNegativeCase } from "data/types/order.types";
import { RESPONSE_ERRORS } from "../errors";

export const CREATE_ORDER_POSITIVE_CASES: ICreateOrderCase[] = [
  {
    title: "Create order with product quantity = 1 (min)",
    productsCount: 1,
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create order with product quantity = 5 (max)",
    productsCount: 5,
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const CREATE_ORDER_NEGATIVE_CASES: ICreateOrderNegativeCase[] = [
  {
    title: "Should NOT create order with empty products",
    productsCount: 1,
    orderData: {
      products: [],
    },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Should NOT create order without customer",
    productsCount: 1,
    orderData: {
      customer: "",
    },
    expectedStatus: STATUS_CODES.NOT_FOUND,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.CUSTOMER_MISSING,
  },
  {
    title: "Should NOT create order with more than 5 products",
    productsCount: 6,
    orderData: {},
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];

export const DELETE_ORDER_CASES: ICreateOrderCase[] = [
  {
    title: "Delete order with product quantity = 1 (min)",
    productsCount: 1,
    expectedStatus: STATUS_CODES.DELETED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Delete order with product quantity = 5 (max)",
    productsCount: 5,
    expectedStatus: STATUS_CODES.DELETED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];
