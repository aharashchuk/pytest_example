import { OrdersApiService } from "api/service/orders.service";
import { IOrderFromResponse } from "data/types/order.types";
import { ORDER_STATUS } from "../order-status";
import { STATUS_CODES } from "data/statusCodes";

export interface IOrderStatusTransitionCase {
  from: string;
  create: (ordersApiService: OrdersApiService, token: string) => Promise<IOrderFromResponse>;
  to: ORDER_STATUS;
  expectedStatus: STATUS_CODES;
  isSuccess?: boolean;
  expectedErrorMessage: string | null;
}

export const positiveOrderStatusTransitions: IOrderStatusTransitionCase[] = [
  {
    from: "Draft with delivery",
    create: (ordersApiService, token) => ordersApiService.createOrderWithDelivery(token, 1),
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    from: "Draft with delivery",
    create: (ordersApiService, token) => ordersApiService.createOrderWithDelivery(token, 1),
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    from: ORDER_STATUS.DRAFT,
    create: (ordersApiService, token) => ordersApiService.createOrderAndEntities(token, 1),
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    from: ORDER_STATUS.CANCELED,
    create: (ordersApiService, token) => ordersApiService.createCanceledOrder(token, 1),
    to: ORDER_STATUS.DRAFT,
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    from: ORDER_STATUS.PROCESSING,
    create: (ordersApiService, token) => ordersApiService.createOrderInProcess(token, 1),
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
] as const;

export const negativeOrderStatusTransitions: IOrderStatusTransitionCase[] = [
  {
    from: "Draft",
    create: (ordersApiService, token) => ordersApiService.createOrderAndEntities(token, 1),
    to: ORDER_STATUS.DRAFT,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Can't reopen not canceled order",
  },
  {
    from: "Draft",
    create: (ordersApiService, token) => ordersApiService.createOrderAndEntities(token, 1),
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Can't process order. Please, schedule delivery",
  },
  {
    from: "In Process",
    create: (ordersApiService, token) => ordersApiService.createOrderInProcess(token, 1),
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
  {
    from: "In Process",
    create: (ordersApiService, token) => ordersApiService.createOrderInProcess(token, 1),
    to: ORDER_STATUS.DRAFT,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Can't reopen not canceled order",
  },
  {
    from: "Partially Received",
    create: (ordersApiService, token) => ordersApiService.createPartiallyReceivedOrder(token, 2),
    to: ORDER_STATUS.DRAFT,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Can't reopen not canceled order",
  },
  {
    from: "Partially Received",
    create: (ordersApiService, token) => ordersApiService.createPartiallyReceivedOrder(token, 2),
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
  {
    from: "Partially Received",
    create: (ordersApiService, token) => ordersApiService.createPartiallyReceivedOrder(token, 2),
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
  {
    from: "Received",
    create: (ordersApiService, token) => ordersApiService.createReceivedOrder(token, 1),
    to: ORDER_STATUS.DRAFT,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Can't reopen not canceled order",
  },
  {
    from: "Received",
    create: (ordersApiService, token) => ordersApiService.createReceivedOrder(token, 1),
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
  {
    from: "Received",
    create: (ordersApiService, token) => ordersApiService.createReceivedOrder(token, 1),
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
  {
    from: "Canceled",
    create: (ordersApiService, token) => ordersApiService.createCanceledOrder(token, 1),
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
  {
    from: "Canceled",
    create: (ordersApiService, token) => ordersApiService.createCanceledOrder(token, 1),
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    isSuccess: false,
    expectedErrorMessage: "Invalid order status",
  },
] as const;

export const invalidStatusesCases: Array<string | null | number | undefined> = [
  "testStatus",
  "",
  null,
  12345,
  undefined,
];
