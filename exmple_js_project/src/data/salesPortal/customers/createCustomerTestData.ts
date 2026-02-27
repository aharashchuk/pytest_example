import { ICreateCustomerCase } from "data/types/customer.types";
import { generateCustomerData } from "./generateCustomerData";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";
import { faker } from "@faker-js/faker";
import _ from "lodash";

export const CREATE_CUSTOMER_POSITIVE_CASES: ICreateCustomerCase[] = [
  //name
  {
    title: "Create customer with 1 character length in name",
    customerData: generateCustomerData({ name: "K" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with 40 characters length in name",
    customerData: generateCustomerData({
      name: "Alexandria Catherine Montgomery Smith Jr",
    }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with with upper-case name",
    customerData: generateCustomerData({ name: "STESHA" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //email
  {
    title: "Create customer with with upper-case email",
    customerData: generateCustomerData({ email: "DONNY.BLACK@tTEST.COM" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //city
  {
    title: "Create customer with 1 character length in city",
    customerData: generateCustomerData({ city: "M" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with 20 characters length in city",
    customerData: generateCustomerData({ city: "Nolagthiosd Ghdipiso" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with with upper-case city",
    customerData: generateCustomerData({ city: "TORONTO" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //street
  {
    title: "Create customer with 1 character length in street",
    customerData: generateCustomerData({ street: "J" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with 40 characters length in street",
    customerData: generateCustomerData({
      street: "Alexandria Catherine Montgomery Smith Jr",
    }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with upper-case street",
    customerData: generateCustomerData({
      street: "SAINT JAMES",
    }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //house
  {
    title: "Create customer with 1 character length in house",
    customerData: generateCustomerData({ house: 1 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with 3 characters length in house",
    customerData: generateCustomerData({ house: 999 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //flat
  {
    title: "Create customer with 1 character length in flat",
    customerData: generateCustomerData({ flat: 1 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with 4 characters length in flat",
    customerData: generateCustomerData({ flat: 9999 }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //phone
  {
    title: "Create customer with 10 characters length in phone",
    customerData: generateCustomerData({ phone: "+1234567890" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer with 20 characters length in phone",
    customerData: generateCustomerData({ phone: "+12345678901234567890" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  //notes
  {
    title: "Create customer with empty notes",
    customerData: generateCustomerData({ notes: "" }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    title: "Create customer 250 characters length in notes",
    customerData: generateCustomerData({ notes: faker.string.alphanumeric({ length: 250 }) }),
    expectedStatus: STATUS_CODES.CREATED,
    isSuccess: true,
    expectedErrorMessage: null,
  },
];

export const CREATE_CUSTOMER_NEGATIVE_CASES: ICreateCustomerCase[] = [
  //name
  {
    title: "Customer without name is not created",
    customerData: _.omit(generateCustomerData(), "name"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Customer with empty name is not created",
    customerData: generateCustomerData({ name: "" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "41 characters name customer is not created",
    customerData: generateCustomerData({ name: faker.string.alphanumeric({ length: 41 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Name with numbers customer is not created",
    customerData: generateCustomerData({ name: "Sony87" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Name with underscore customer is not created",
    customerData: generateCustomerData({ name: "Dan_99" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Name with 2 spaces in name customer is not created",
    customerData: generateCustomerData({ name: "Test  Customer" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },

  //email
  {
    title: "Customer without email is not created",
    customerData: _.omit(generateCustomerData(), "email"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Customer with empty email is not created",
    customerData: generateCustomerData({ email: "" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Email without @ customer is not created",
    customerData: generateCustomerData({ email: "tata.com" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  //country
  {
    title: "Without country customer is not created",
    customerData: _.omit(generateCustomerData(), "country"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },

  //city
  {
    title: "Customer without city is not created",
    customerData: _.omit(generateCustomerData(), "city"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Customer with empty city is not created",
    customerData: generateCustomerData({ city: "" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "City with dash customer is not created",
    customerData: generateCustomerData({ city: "Baden-Baden" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "City with apostrophe customer is not created",
    customerData: generateCustomerData({ city: "Kapa'a" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  //street
  {
    title: "Customer without street is not created",
    customerData: _.omit(generateCustomerData(), "street"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Customer with empty street is not created",
    customerData: generateCustomerData({ street: "" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Street with dash customer is not created",
    customerData: generateCustomerData({ street: "Rose-street" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Street with apostrophe customer is not created",
    customerData: generateCustomerData({ street: "Jamie's" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Street with 2 spaces customer is not created",
    customerData: generateCustomerData({ street: "Test  Street" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  //house
  {
    title: "Customer without house is not created",
    customerData: _.omit(generateCustomerData(), "house"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "100000 house customer is not created",
    customerData: generateCustomerData({ house: 100000 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "0 house customer is not created",
    customerData: generateCustomerData({ house: 0 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Negative house customer is not created",
    customerData: generateCustomerData({ house: -10 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Not integer house customer is not created",
    customerData: generateCustomerData({ house: faker.string.alphanumeric({ length: 5 }) as unknown as number }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  //flat
  {
    title: "Customer without flat is not created",
    customerData: _.omit(generateCustomerData(), "flat"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "100000 flat customer is not created",
    customerData: generateCustomerData({ flat: 100000 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "0 flat customer is not created",
    customerData: generateCustomerData({ flat: 0 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Negative flat customer is not created",
    customerData: generateCustomerData({ flat: -10 }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Not integer flat customer is not created",
    customerData: generateCustomerData({ flat: faker.string.alphanumeric({ length: 5 }) as unknown as number }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },

  //phone
  {
    title: "Customer without phone is not created",
    customerData: _.omit(generateCustomerData(), "phone"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Customer with empty phone is not created",
    customerData: generateCustomerData({ phone: "" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "+12345678 phone customer is not created",
    customerData: generateCustomerData({ phone: "+12345678" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "+123456789123456789123 phone customer is not created",
    customerData: generateCustomerData({ phone: "+123456789123456789123" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Dash in phone customer is not created",
    customerData: generateCustomerData({ phone: "-" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },

  {
    title: "Customer without + in phone is not created",
    customerData: generateCustomerData({ phone: "12345678910" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Negative phone customer is not created",
    customerData: generateCustomerData({ phone: "-1234567890" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },

  //notes
  {
    title: "251 notes customer is not created",
    customerData: generateCustomerData({ notes: faker.string.alphanumeric({ length: 251 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Notes with < or > symbols customer is not created",
    customerData: generateCustomerData({ notes: "Invalid notes with <symbol>" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];
