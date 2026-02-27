import { STATUS_CODES } from "data/statusCodes";
import { generateCustomerData } from "./generateCustomerData";
import { ICustomer } from "data/types/customer.types";

// Invalid payload scenarios for CREATE/UPDATE operations
// Returns fresh test data for each invocation
export const getInvalidPayloadScenarios = (): Array<{
  description: string;
  getTestData: () => ICustomer;
}> => [
  {
    description: "Email: Missing @",
    getTestData: () => generateCustomerData({ email: "plainaddress" }),
  },
  {
    description: "Email: Missing domain",
    getTestData: () => generateCustomerData({ email: "test@" }),
  },
  {
    description: "Email: Empty",
    getTestData: () => generateCustomerData({ email: "" }),
  },
  {
    description: "Name: Empty",
    getTestData: () => generateCustomerData({ name: "" }),
  },
  {
    description: "Name: Too long",
    getTestData: () => generateCustomerData({ name: "a".repeat(41) }),
  },
  {
    description: "City: Empty",
    getTestData: () => generateCustomerData({ city: "" }),
  },
  {
    description: "City: Too long",
    getTestData: () => generateCustomerData({ city: "a".repeat(21) }),
  },
  {
    description: "Street: Empty",
    getTestData: () => generateCustomerData({ street: "" }),
  },
  {
    description: "Street: Too long",
    getTestData: () => generateCustomerData({ street: "a".repeat(41) }),
  },
  {
    description: "House: Zero",
    getTestData: () => generateCustomerData({ house: 0 }),
  },
  {
    description: "House: Negative",
    getTestData: () => generateCustomerData({ house: -1 }),
  },
  {
    description: "Flat: Zero",
    getTestData: () => generateCustomerData({ flat: 0 }),
  },
  {
    description: "Flat: Negative",
    getTestData: () => generateCustomerData({ flat: -1 }),
  },
  {
    description: "Phone: Letters",
    getTestData: () => generateCustomerData({ phone: "abcdefg" }),
  },
  {
    description: "Phone: Empty",
    getTestData: () => generateCustomerData({ phone: "" }),
  },
  {
    description: "Notes: Too long",
    getTestData: () => generateCustomerData({ notes: "a".repeat(251) }),
  },
];

// Invalid ID scenarios for GET/DELETE/UPDATE operations
// Simple data definition without additional logic
export const INVALID_ID_SCENARIOS = {
  DELETE: [
    {
      description: "Short ID",
      id: "123",
      expectedStatus: STATUS_CODES.SERVER_ERROR,
    },
    {
      description: "Long ID",
      id: "a".repeat(50),
      expectedStatus: STATUS_CODES.SERVER_ERROR,
    },
  ],

  DELETE_WITH_ERROR: [
    {
      description: "Non-existent ID (valid format)",
      id: "507f1f77bcf86cd799439011",
      expectedStatus: STATUS_CODES.NOT_FOUND,
    },
  ],

  GET: [
    {
      description: "Short ID",
      id: "123",
      expectedStatus: STATUS_CODES.SERVER_ERROR,
    },
    {
      description: "Long ID",
      id: "a".repeat(50),
      expectedStatus: STATUS_CODES.SERVER_ERROR,
    },
  ],

  GET_WITH_ERROR: [
    {
      description: "Non-existent ID (valid format)",
      id: "507f1f77bcf86cd799439011",
      expectedStatus: STATUS_CODES.NOT_FOUND,
    },
  ],

  UPDATE: [
    {
      description: "Non-existent ID (valid format)",
      id: "507f1f77bcf86cd799439011",
      expectedStatus: STATUS_CODES.BAD_REQUEST,
    },
    {
      description: "Short ID",
      id: "123",
      expectedStatus: STATUS_CODES.BAD_REQUEST,
    },
    {
      description: "Long ID",
      id: "a".repeat(50),
      expectedStatus: STATUS_CODES.BAD_REQUEST,
    },
  ],
};
