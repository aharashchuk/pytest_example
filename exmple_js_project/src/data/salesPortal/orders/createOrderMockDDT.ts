import { Mock } from "mock/mock";
import { generateProductResponseData } from "../products/generateProductData";
import { NOTIFICATIONS } from "../notifications";
import { generateCustomerResponseData } from "../customers/generateCustomerData";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";

export const openCreateOrderModalNegativeCases = [
  {
    title: "Should NOT open create order modal with no customers",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll({
        Products: [generateProductResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    notification: NOTIFICATIONS.NO_CUSTOMERS_FOUND,
  },
  {
    title: "Should NOT open create order modal with customers/all 500 error",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll(
        {
          IsSuccess: false,
          ErrorMessage: null,
        },
        STATUS_CODES.SERVER_ERROR,
      ),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll({
        Products: [generateProductResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    notification: NOTIFICATIONS.ORDER_UNABLE_TO_CREATE,
  },
  {
    title: "Should NOT open create order modal with no products",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [generateCustomerResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll({
        Products: [],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    notification: NOTIFICATIONS.NO_PRODUCTS_FOUND,
  },
  {
    title: "Should NOT open create order modal with products/all 500 error",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [generateCustomerResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll(
        {
          IsSuccess: false,
          ErrorMessage: null,
        },
        STATUS_CODES.SERVER_ERROR,
      ),
    notification: NOTIFICATIONS.ORDER_UNABLE_TO_CREATE,
  },
];

export const openCreateOrderModalUnauthorizedCases = [
  {
    title: "Should NOT open create order modal with customers/all 401 error",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.UNAUTHORIZED,
        },
        STATUS_CODES.UNAUTHORIZED,
      ),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll({
        Products: [generateProductResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
  },
  {
    title: "Should NOT open create order modal with products/all 401 error",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [generateCustomerResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.UNAUTHORIZED,
        },
        STATUS_CODES.UNAUTHORIZED,
      ),
  },
];

export const createOrderResponseErrorCases = [
  {
    title: "Should display message when response status 400",
    responseMock: async (mock: Mock) =>
      await mock.createOrderModal(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
        },
        STATUS_CODES.BAD_REQUEST,
      ),
    notification: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Should display message when response status 404",
    responseMock: async (mock: Mock) =>
      await mock.createOrderModal(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.CUSTOMER_NOT_FOUND("test3891318231"),
        },
        STATUS_CODES.NOT_FOUND,
      ),
    notification: NOTIFICATIONS.ORDER_NOT_CREATED,
  },
  {
    title: "Should display message when response status 500",
    responseMock: async (mock: Mock) =>
      await mock.createOrderModal(
        {
          IsSuccess: false,
          ErrorMessage: null,
        },
        STATUS_CODES.SERVER_ERROR,
      ),
    notification: NOTIFICATIONS.ORDER_NOT_CREATED,
  },
];

export const createOrderModalCheckDropdowns = [
  {
    title: "Should display mocked customers in customers dropdown",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [generateCustomerResponseData(), generateCustomerResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll({
        Products: [generateProductResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
  },
  {
    title: "Should display mocked products in products dropdown",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [generateCustomerResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    productsMock: async (mock: Mock) =>
      await mock.getProductsAll({
        Products: [generateProductResponseData(), generateProductResponseData()],
        IsSuccess: true,
        ErrorMessage: null,
      }),
  },
];
