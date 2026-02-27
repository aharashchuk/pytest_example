import { ID, ICreatedOn, IResponseFields, SortOrder, ICaseApi } from "./core.types";
import { ICustomerFromResponse } from "./customer.types";
import { IOrderProductFromResponse, IProduct } from "./product.types";
import { ORDER_STATUS, ORDER_HISTORY_ACTIONS } from "../salesPortal/order-status";
import { IDeliveryInfo } from "../salesPortal/delivery-status";
import { IAssignedManager, IUser } from "./user.types";
import { STATUS_CODES } from "data/statusCodes";
import { OrdersApiService } from "api/service/orders.service";

export interface IOrderProduct extends IProduct {
  _id: string;
  received: boolean;
}
export interface IOrderResponse extends IResponseFields {
  Order: IOrderFromResponse;
  DeliveryInfo: IDeliveryInfo;
}

export interface IGetAllOrdersQuery extends Record<string, string | number | string[]> {
  page?: number;
  limit?: number;
  search?: string;
  status?: ORDER_STATUS[];
  sortField?: OrdersTableHeader;
  sortOrder?: SortOrder;
}

export interface IOrderHistoryResponse extends IResponseFields {
  history: IOrderHistory[];
}

export interface IOrderFromResponse extends ICreatedOn, ID {
  status: ORDER_STATUS;
  customer: ICustomerFromResponse;
  products: IOrderProductFromResponse[];
  total_price: number;
  delivery: null | IDeliveryInfo;
  comments: IComment[];
  history: IOrderHistory[];
  assignedManager: IAssignedManager | null;
}
export interface IOrderHistory extends Omit<IOrderFromResponse, "comments" | "history" | "customer" | "createdOn"> {
  customer: ICustomerFromResponse["_id"];
  changedOn: string;
  action: ORDER_HISTORY_ACTIONS;
}

export interface IOrderHistoryEntry {
  assignedManager: IUser | null;
  status: ORDER_HISTORY_ACTIONS;
  customer: string;
  products: IOrderProduct[];
  total_price: number;
  delivery: IDeliveryInfo | null;
  changedOn: string;
  action: ORDER_HISTORY_ACTIONS;
  performer: IUser | null;
}

export interface IComment extends ID {
  text: string;
  createdOn: string;
}

export interface IOrder {
  _id: string;
  status: ORDER_STATUS;
  customer: ICustomerFromResponse;
  products: IOrderProduct[];
  delivery: IDeliveryInfo | null;
  total_price: number;
  createdOn: string;
  comments: IComment[];
  history: IOrderHistoryEntry[];
  assignedManager: IUser | null;
}

export interface IOrderInTable extends ICreatedOn {
  orderId: string;
  email: string;
  price: number;
  delivery: string;
  assignedManager: string;
  status: ORDER_STATUS;
}

export interface IOrdersResponse extends IResponseFields {
  Orders: IOrderFromResponse[];
  limit: number;
  page: number;
  search: string;
  status: ORDER_STATUS[];
  total: number;
  sorting: { sortField: OrdersTableHeader; sortOrder: SortOrder };
}
export type OrdersTableHeader = "_id" | "email" | "price" | "delivery" | "status" | "assignedManager" | "createdOn";

export interface IOrderCreateBody {
  customer: string;
  products: string[];
}

export interface ICommentData {
  commentText: string;
  commentator: string;
  createdOn: string;
}

export interface ICreateDeliveryCase extends ICaseApi {
  deliveryData: Partial<IDeliveryInfo>;
  expectedStatus: STATUS_CODES;
}
export type IOrderUpdateBody = {
  customer?: string;
  products?: string[];
};

export interface ICreateOrderCase extends ICaseApi {
  productsCount: number;
}

export interface ICommentOrderCase extends ICaseApi {
  text?: string;
}

export interface ICreateOrderNegativeCase extends ICaseApi {
  productsCount: number;
  orderData: Partial<IOrderCreateBody>;
}

export interface IUpdateOrderErrorCase {
  title: string;
  expectedStatus: number;
  isSuccess: boolean;
  expectedErrorMessage: string | null;
  orderId?: string;
  customerId?: string;
  shouldHaveProducts?: boolean;
  invalidProductId?: string;
}

export interface IOrderInStatusCases {
  name: string;
  create: (ordersApiService: OrdersApiService, token: string) => Promise<IOrderFromResponse>;
}

export interface IReceiveProductsPositiveCase {
  title: string;
  orderProductsCount: number;
  receiveProductsCount: number;
  expectedOrderStatus: ORDER_STATUS;
}

export interface IReceiveProductsNegativeStatusCase {
  title: string;
  create: (ordersApiService: OrdersApiService, token: string) => Promise<IOrderFromResponse>;
  receiveProductsCount: number;
  expectedStatus: STATUS_CODES;
  expectedErrorMessage: string | null | ((order: IOrderFromResponse) => string | null);
}

export interface IReceiveProductsInvalidPayloadCase {
  title: string;
  buildProducts: (order: IOrderFromResponse) => Array<string>;
  expectedStatus: STATUS_CODES;
  expectedErrorMessage: string | null;
}
