import { IOrderInStatusCases } from "data/types/order.types";
import { Mock } from "mock/mock";
import { NOTIFICATIONS } from "../notifications";
import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";

export const orderInStatus: IOrderInStatusCases[] = [
  {
    name: "In Process",
    create: (ordersApiService, token) => ordersApiService.createOrderInProcess(token, 1),
  },
  {
    name: "Partially Received",
    create: (ordersApiService, token) => ordersApiService.createPartiallyReceivedOrder(token, 2),
  },
  {
    name: "Received",
    create: (ordersApiService, token) => ordersApiService.createReceivedOrder(token, 1),
  },
  {
    name: "Canceled",
    create: (ordersApiService, token) => ordersApiService.createCanceledOrder(token, 1),
  },
];

export const editCustomerinOrderNegativeCases = [
  {
    title: "Should NOT open edit customer modal with no customers",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll({
        Customers: [],
        IsSuccess: true,
        ErrorMessage: null,
      }),
    notification: NOTIFICATIONS.NO_CUSTOMERS_FOUND,
  },
  {
    title: "Should NOT open edit customer modal with customers/all 500 error",
    customersMock: async (mock: Mock) =>
      await mock.getCustomersAll(
        {
          IsSuccess: false,
          ErrorMessage: null,
        },
        STATUS_CODES.SERVER_ERROR,
      ),
    notification: NOTIFICATIONS.CUSTOMER_UNABLE_TO_UPDATE,
  },
];

export const editOrderCustomerResponseErrorCases = [
  {
    title: "Should display message when response status 400",
    responseMock: async (mock: Mock, orderId: string) =>
      await mock.orderById(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
        },
        orderId,
        STATUS_CODES.BAD_REQUEST,
      ),
  },
  {
    title: "Should display message when response status 404",
    responseMock: async (mock: Mock, orderId: string) =>
      await mock.orderById(
        {
          IsSuccess: false,
          ErrorMessage: RESPONSE_ERRORS.CUSTOMER_NOT_FOUND("test3891318231"),
        },
        orderId,
        STATUS_CODES.NOT_FOUND,
      ),
  },
  {
    title: "Should display message when response status 500",
    responseMock: async (mock: Mock, orderId: string) =>
      await mock.orderById(
        {
          IsSuccess: false,
          ErrorMessage: null,
        },
        orderId,
        STATUS_CODES.SERVER_ERROR,
      ),
  },
];
