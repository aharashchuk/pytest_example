import { ORDER_STATUS } from "../order-status";
import { STATUS_CODES } from "data/statusCodes";

export interface IOrderStatusTransitionCase {
  to: ORDER_STATUS;
  expectedStatus: STATUS_CODES;
  isSuccess?: boolean;
  expectedErrorMessage: string | null;
}

export const notificationOnStatusChangeCases: IOrderStatusTransitionCase[] = [
  {
    to: ORDER_STATUS.PROCESSING,
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    to: ORDER_STATUS.CANCELED,
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    to: ORDER_STATUS.PARTIALLY_RECEIVED,
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
  {
    to: ORDER_STATUS.RECEIVED,
    expectedStatus: STATUS_CODES.OK,
    isSuccess: true,
    expectedErrorMessage: null,
  },
] as const;
