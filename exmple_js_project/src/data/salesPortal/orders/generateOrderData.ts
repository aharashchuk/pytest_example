import { faker } from "@faker-js/faker";
import { SortOrder } from "data/types/core.types";
import { IOrderFromResponse, IOrderResponse, IOrdersResponse, OrdersTableHeader } from "data/types/order.types";
import { getRandomEnumValue } from "utils/enum.utils";
import { ObjectId } from "bson";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { generateCustomerResponseData } from "data/salesPortal/customers/generateCustomerData";
import { generateIOrderProductFromResponse } from "data/salesPortal/products/generateProductData";
import { generateDelivery } from "./generateDeliveryData";

export function generateOrderData(params?: Partial<IOrderFromResponse>): IOrderFromResponse {
  return {
    _id: new ObjectId().toHexString(),
    status: params?.status || getRandomEnumValue(ORDER_STATUS),
    customer: params?.customer || generateCustomerResponseData(),
    products: params?.products || [generateIOrderProductFromResponse()],
    total_price: params?.total_price || faker.number.int({ min: 1, max: 99999 }),
    delivery: params?.delivery || generateDelivery(),
    comments: params?.comments || [],
    history: params?.history || [],
    assignedManager: params?.assignedManager || null,
    createdOn: new Date().toISOString(),
  };
}

export function generateOrderResponseData(params?: Partial<IOrderFromResponse>): IOrderResponse {
  const initial = generateOrderData(params);
  return {
    Order: initial,
    DeliveryInfo: params?.delivery || generateDelivery(),
    IsSuccess: true,
    ErrorMessage: null,
  };
}

export function generateOrdersResponseData(
  ordersCount: number,
  sorting?: { sortField: OrdersTableHeader; sortOrder: SortOrder },
  params?: Partial<IOrderFromResponse>,
): IOrdersResponse {
  const orders: IOrderFromResponse[] = [];
  for (let i = 0; i < ordersCount; i++) {
    orders.push(generateOrderData(params));
  }
  return {
    Orders: orders,
    search: "",
    IsSuccess: true,
    ErrorMessage: null,
    total: ordersCount,
    page: 1,
    limit: 10,
    status: [],
    sorting: {
      sortField: sorting?.sortField || "createdOn",
      sortOrder: sorting?.sortOrder || "desc",
    },
  };
}
