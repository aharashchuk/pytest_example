import { ICreateCustomerCase } from "data/types/customer.types";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";
import { ObjectId } from "bson";

export const getCustomerByIdPositiveCases: ICreateCustomerCase[] = [
  {
    title: "Should get customer by valid id",
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const getCustomerByIdNegativeCases: ICreateCustomerCase[] = [
  {
    title: "404 returned for non-existing id of valid format",
    id: new ObjectId().toHexString(),
    expectedStatus: STATUS_CODES.NOT_FOUND,
    isSuccess: false,
    get expectedErrorMessage() {
      return RESPONSE_ERRORS.CUSTOMER_NOT_FOUND(this.id!);
    },
  },
];
