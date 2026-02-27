import { STATUS_CODES } from "data/statusCodes";
import { IOrderInStatusCases } from "data/types/order.types";
import { RESPONSE_ERRORS } from "../errors";

export const orderInStatus: IOrderInStatusCases[] = [
  { name: "Draft", create: (ordersApiService, token) => ordersApiService.createOrderAndEntities(token, 1) },
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

export interface IManagerAssignNegativeCase {
  title: string;
  orderId: (orderId: string) => string | undefined;
  managerId: (managerId: string) => string | undefined;
  expected: {
    status: STATUS_CODES;
    isSuccessful?: boolean;
    errorMessage?: string | null;
  };
}

export const assignUnassignManagerNegativeCases: IManagerAssignNegativeCase[] = [
  {
    title: "manager with non-existing managerId",
    managerId: () => "000000000000000000000000",
    orderId: (orderId: string) => orderId,
    expected: {
      status: STATUS_CODES.NOT_FOUND,
      isSuccessful: false,
      errorMessage: RESPONSE_ERRORS.MANAGER_NOT_FOUND("000000000000000000000000"),
    },
  },
  {
    title: "manager with non-existing orderId",
    orderId: () => "000000000000000000000000",
    managerId: (managerId: string) => managerId,
    expected: {
      status: STATUS_CODES.NOT_FOUND,
      isSuccessful: false,
      errorMessage: RESPONSE_ERRORS.ORDER_NOT_FOUND("000000000000000000000000"),
    },
  },
];
