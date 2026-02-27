import type { OrdersApiService } from "api/service/orders.service";

export interface IAssignManagerTestCase {
  title: string;
  createOrder: (ordersApiService: OrdersApiService, token: string) => Promise<{ _id: string }>;
  isSmoke?: boolean;
}

export const ASSIGN_MANAGER_ORDER_STATUS_CASES: IAssignManagerTestCase[] = [
  {
    title: "Assign manager to draft order",
    createOrder: (svc, token) => svc.createOrderAndEntities(token, 1),
    isSmoke: true,
  },
  {
    title: "Assign manager to order in processing status",
    createOrder: (svc, token) => svc.createOrderInProcess(token, 1),
  },
  {
    title: "Assign manager to partially received order",
    createOrder: (svc, token) => svc.createPartiallyReceivedOrder(token, 2),
  },
  {
    title: "Assign manager to received order",
    createOrder: (svc, token) => svc.createReceivedOrder(token, 1),
  },
  {
    title: "Assign manager to canceled order",
    createOrder: (svc, token) => svc.createCanceledOrder(token, 1),
  },
];
