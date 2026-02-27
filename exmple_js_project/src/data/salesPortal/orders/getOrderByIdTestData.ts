import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";
import { ObjectId } from "bson";
import { faker } from "@faker-js/faker";
import { ICaseApi } from "data/types/core.types";

export const getOrderByIdPositiveCases: ICaseApi[] = [
  {
    title: "Should get order by valid id",
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
    isSuccess: true,
  },
];

const notFoundId = new ObjectId().toHexString();
export const getOrderByIdNegativeCases: ICaseApi[] = [
  {
    title: "404 returned for non-existing id of valid format",
    _id: notFoundId,
    expectedStatus: STATUS_CODES.NOT_FOUND,
    expectedErrorMessage: RESPONSE_ERRORS.ORDER_NOT_FOUND(notFoundId),
    isSuccess: false,
  },
  {
    title: "500 returned for id of invalid format (CastError from backend)",
    _id: faker.string.alphanumeric({ length: 10 }),
    expectedStatus: STATUS_CODES.SERVER_ERROR,
    expectedErrorMessage:
      "Argument passed in must be a string of 12 bytes or a string of 24 hex characters or an integer",
    isSuccess: false,
  },
];
