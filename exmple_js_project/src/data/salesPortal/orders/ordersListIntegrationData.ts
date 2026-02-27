import { OrdersTableHeader } from "data/types/order.types";
import { ICase } from "data/types/core.types";

interface IOrdersListIntegrationCase extends ICase {
  ordersCount: number;
  sorting?: { sortField: OrdersTableHeader; sortOrder: "asc" | "desc" };
}

export const ordersListIntegrationData: IOrdersListIntegrationCase[] = [
  {
    title: "Sorting by Created On descending",
    ordersCount: 5,
    sorting: { sortField: "createdOn", sortOrder: "desc" },
  },
  {
    title: "Sorting by Created On ascending",
    ordersCount: 5,
    sorting: { sortField: "createdOn", sortOrder: "asc" },
  },
  {
    title: "Sorting by Price descending",
    ordersCount: 5,
    sorting: { sortField: "price", sortOrder: "desc" },
  },
  {
    title: "Sorting by Price ascending",
    ordersCount: 5,
    sorting: { sortField: "price", sortOrder: "asc" },
  },
  {
    title: "Sorting by Status descending",
    ordersCount: 5,
    sorting: { sortField: "status", sortOrder: "desc" },
  },
  {
    title: "Sorting by Status ascending",
    ordersCount: 5,
    sorting: { sortField: "status", sortOrder: "asc" },
  },
  {
    title: "Sorting by Assigned Manager descending",
    ordersCount: 5,
    sorting: { sortField: "assignedManager", sortOrder: "desc" },
  },
  {
    title: "Sorting by Assigned Manager ascending",
    ordersCount: 5,
    sorting: { sortField: "assignedManager", sortOrder: "asc" },
  },
  {
    title: "Sorting by Order Number descending",
    ordersCount: 5,
    sorting: { sortField: "_id", sortOrder: "desc" },
  },
  {
    title: "Sorting by Order Number ascending",
    ordersCount: 5,
    sorting: { sortField: "_id", sortOrder: "asc" },
  },
  {
    title: "Sorting by Email descending",
    ordersCount: 5,
    sorting: { sortField: "email", sortOrder: "desc" },
  },
  {
    title: "Sorting by Email ascending",
    ordersCount: 5,
    sorting: { sortField: "email", sortOrder: "asc" },
  },
  {
    title: "Sorting by Delivery descending",
    ordersCount: 5,
    sorting: { sortField: "delivery", sortOrder: "desc" },
  },
  {
    title: "Sorting by Delivery ascending",
    ordersCount: 5,
    sorting: { sortField: "delivery", sortOrder: "asc" },
  },
];
