import { ICreateProductCase } from "data/types/product.types";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";
import { ObjectId } from "bson";
import { faker } from "@faker-js/faker";

export const getProductByIdPositiveCases: ICreateProductCase[] = [
  {
    title: "Should get product by valid id",
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
];

export const getProductByIdNegativeCases: ICreateProductCase[] = [
  {
    title: "404 returned for empty id",
    id: "",
    expectedStatus: STATUS_CODES.NOT_FOUND,
    expectedErrorMessage: null,
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
    title: "500 returned for id of invalid format",
    id: faker.string.alphanumeric({ length: 10 }),
    expectedStatus: STATUS_CODES.SERVER_ERROR,
    expectedErrorMessage: null,
  },
];
