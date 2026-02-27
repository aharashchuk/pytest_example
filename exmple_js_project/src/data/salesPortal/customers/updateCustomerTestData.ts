import { generateCustomerData } from "data/salesPortal/customers/generateCustomerData";
import { ICreateCustomerCase } from "data/types/customer.types";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { faker } from "@faker-js/faker";
import { ObjectId } from "bson";

export const updateCustomerPositiveCases: ICreateCustomerCase[] = [
  {
    title: "Update customer name to 1 character",
    customerData: { name: "K" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update customer name to 40 characters",
    customerData: { name: "Alexandria Catherine Montgomery Smith Jr" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update customer name with mixed case",
    customerData: { name: "JoHn DoE" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update email to valid format",
    customerData: { email: faker.internet.email() },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update phone to valid format",
    customerData: { phone: "+1" + faker.string.numeric({ length: 10 }) },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update city to 1 character",
    customerData: { city: "M" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update city to 20 characters",
    customerData: { city: "San Francisco City" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update street to valid format",
    customerData: { street: "Main Street 123" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update house number",
    customerData: { house: 42 },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update flat number",
    customerData: { flat: 101 },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update notes to 250 characters",
    customerData: { notes: faker.string.alphanumeric({ length: 250 }) },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Clear notes (empty string)",
    customerData: { notes: "" },
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Update full customer data",
    customerData: generateCustomerData(),
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const updateCustomerInvalidIdCases: ICreateCustomerCase[] = [
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

export const updateCustomerNegativeCases: ICreateCustomerCase[] = [
  {
    title: "Update name with empty string — bad request",
    customerData: { name: "" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update name with 41 characters — bad request",
    customerData: { name: faker.string.alpha({ length: 41 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update name with special characters — bad request",
    customerData: { name: "John@#$%Doe" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update with invalid email format — bad request",
    customerData: { email: "invalid-email" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update with empty email — bad request",
    customerData: { email: "" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update phone with invalid format — bad request",
    customerData: { phone: "1234567" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update phone without + sign — bad request",
    customerData: { phone: "1234567890123" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update city with 21 characters — bad request",
    customerData: { city: faker.string.alpha({ length: 21 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update city with empty string — bad request",
    customerData: { city: "" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update street with 41 characters — bad request",
    customerData: { street: faker.string.alphanumeric({ length: 41 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update street with empty string — bad request",
    customerData: { street: "" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update house with negative number — bad request",
    customerData: { house: -1 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update house with 1000 — bad request",
    customerData: { house: 1000 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update flat with negative number — bad request",
    customerData: { flat: -5 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update flat with 10000 — bad request",
    customerData: { flat: 10000 },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update notes with 251 characters — bad request",
    customerData: { notes: faker.string.alphanumeric({ length: 251 }) },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Update notes with < or > symbols — bad request",
    customerData: { notes: "Invalid notes with <symbol>" },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];
