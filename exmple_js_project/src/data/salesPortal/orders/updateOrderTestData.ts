import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { IUpdateOrderErrorCase } from "data/types/order.types";

export const updateOrderErrorCases: IUpdateOrderErrorCase[] = [
  {
    title: "404 returned for non-existing order",
    orderId: "ffffffffffffffffffffffff",
    expectedStatus: STATUS_CODES.NOT_FOUND,
    isSuccess: false,
    expectedErrorMessage: "Order with id 'ffffffffffffffffffffffff' wasn't found",
    shouldHaveProducts: true,
  },
  {
    title: "404 returned for non-existing product id",
    invalidProductId: "ffffffffffffffffffffffff",
    expectedStatus: STATUS_CODES.NOT_FOUND,
    isSuccess: false,
    expectedErrorMessage: "Product with id 'ffffffffffffffffffffffff' wasn't found",
    shouldHaveProducts: true,
  },
  {
    title: "400 returned for empty products array",
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
    shouldHaveProducts: false,
  },
  {
    title: "401 returned without token",
    expectedStatus: STATUS_CODES.UNAUTHORIZED,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.UNAUTHORIZED,
    shouldHaveProducts: true,
  },
  {
    title: "404 returned for non-existing customer",
    customerId: "ffffffffffffffffffffffff",
    expectedStatus: STATUS_CODES.NOT_FOUND,
    isSuccess: false,
    expectedErrorMessage: "Customer with id 'ffffffffffffffffffffffff' wasn't found",
    shouldHaveProducts: true,
  },
  {
    title: "500 returned on invalid ObjectId format for order",
    orderId: "123",
    expectedStatus: STATUS_CODES.SERVER_ERROR,
    isSuccess: false,
    expectedErrorMessage:
      "Argument passed in must be a string of 12 bytes or a string of 24 hex characters or an integer",
    shouldHaveProducts: true,
  },
  {
    title: "500 returned on invalid ObjectId format for customer",
    customerId: "123",
    expectedStatus: STATUS_CODES.SERVER_ERROR,
    isSuccess: false,
    expectedErrorMessage: 'Cast to ObjectId failed for value "123" (type string) at path "_id" for model "Customer"',
    shouldHaveProducts: true,
  },
];
