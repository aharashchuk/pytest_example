import { RESPONSE_ERRORS } from "data/salesPortal/errors";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { STATUS_CODES } from "data/statusCodes";
import { IReceiveProductsPositiveCase } from "data/types/order.types";
import { IReceiveProductsNegativeStatusCase } from "data/types/order.types";
import { IReceiveProductsInvalidPayloadCase } from "data/types/order.types";

export const RECEIVE_PRODUCTS_POSITIVE_CASES: IReceiveProductsPositiveCase[] = [
  {
    title: "Processing: receive 1 product (becomes Partially Received)",
    orderProductsCount: 5,
    receiveProductsCount: 1,
    expectedOrderStatus: ORDER_STATUS.PARTIALLY_RECEIVED,
  },
  {
    title: "Processing: receive 3 products (becomes Partially Received)",
    orderProductsCount: 5,
    receiveProductsCount: 3,
    expectedOrderStatus: ORDER_STATUS.PARTIALLY_RECEIVED,
  },
  {
    title: "Processing: receive 5 products (becomes Received)",
    orderProductsCount: 5,
    receiveProductsCount: 5,
    expectedOrderStatus: ORDER_STATUS.RECEIVED,
  },
];

export const RECEIVE_PRODUCTS_NEGATIVE_STATUS_CASES: IReceiveProductsNegativeStatusCase[] = [
  {
    title: "Draft status",
    create: (ordersApiService, token) => ordersApiService.createOrderWithDelivery(token, 1),
    receiveProductsCount: 1,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INVALID_ORDRER_STATUS,
  },
  {
    title: "Received status (already fully received)",
    create: (ordersApiService, token) => ordersApiService.createReceivedOrder(token, 1),
    receiveProductsCount: 1,
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INVALID_ORDRER_STATUS,
  },
];

export const RECEIVE_PRODUCTS_INVALID_PAYLOAD_CASES: IReceiveProductsInvalidPayloadCase[] = [
  {
    title: "More than 5 products in request",
    buildProducts: (order) => {
      const ids = order.products.slice(0, 5).map((p) => p._id);
      return ids.length > 0 ? [...ids, ids[0]!] : [];
    },
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Empty products array",
    buildProducts: () => [],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Invalid product id: null string",
    buildProducts: () => [null as unknown as string],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Invalid product id: UUID string",
    buildProducts: () => ["985a82b8-4a55-439c-b458-57341cedeb94"],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.PRODUCT_NOT_REQUESTED("985a82b8-4a55-439c-b458-57341cedeb94"),
  },
  {
    title: "Invalid product id: dummy string",
    buildProducts: () => ["dummy"],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.PRODUCT_NOT_REQUESTED("dummy"),
  },
  {
    title: "Invalid product id: negative value string",
    buildProducts: () => ["-1"],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.PRODUCT_NOT_REQUESTED("-1"),
  },
  {
    title: "Invalid product id: date string",
    buildProducts: () => ["2025-12-21"],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.PRODUCT_NOT_REQUESTED("2025-12-21"),
  },
  {
    title: "Product id with non-existing id",
    buildProducts: () => ["000000000000000000000000"],
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.PRODUCT_NOT_REQUESTED("000000000000000000000000"),
  },
];
