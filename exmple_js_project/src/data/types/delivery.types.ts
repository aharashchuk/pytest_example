import { DELIVERY_CONDITION, DELIVERY_LOCATION, IDeliveryInfo } from "data/salesPortal/delivery-status";
import { ORDER_HISTORY_ACTIONS, ORDER_STATUS } from "data/salesPortal/order-status";
import { ICase } from "./core.types";
import { ScheduleDeliveryPage } from "ui/pages/orders/components/delivery/scheduleDelivery.page";
import { COUNTRY } from "data/salesPortal/country";

export type DeliveryInfo = {
  deliveryType: string;
  deliveryDate: string;
  country: string;
  city: string;
  street: string;
  house: number;
  flat: number;
};

export type HistoryEventRow = {
  action: string;
  performedBy: string;
  dateTime: string;
};

export const DELIVERY_HISTORY_FIELDS = [
  "Delivery Type",
  "Delivery Date",
  "Country",
  "City",
  "Street",
  "House",
  "Flat",
] as const;

export type DeliveryHistoryField = (typeof DELIVERY_HISTORY_FIELDS)[number];

export type StatusField = "Status";
export type ManagerField = "Assigned Manager";

export const STATUS_ACTIONS = [
  ORDER_HISTORY_ACTIONS.CREATED,
  ORDER_HISTORY_ACTIONS.REOPENED,
  ORDER_HISTORY_ACTIONS.CANCELED,
  ORDER_HISTORY_ACTIONS.PROCESSED,
] as const;
export type StatusHistoryAction = (typeof STATUS_ACTIONS)[number];

export const DELIVERY_ACTIONS = [
  ORDER_HISTORY_ACTIONS.DELIVERY_EDITED,
  ORDER_HISTORY_ACTIONS.DELIVERY_SCHEDULED,
] as const;
export type DeliveryHistoryAction = (typeof DELIVERY_ACTIONS)[number];

export const MANAGER_ACTIONS = [
  ORDER_HISTORY_ACTIONS.MANAGER_ASSIGNED,
  ORDER_HISTORY_ACTIONS.MANAGER_UNASSIGNED,
] as const;
export type ManagerHistoryAction = (typeof MANAGER_ACTIONS)[number];

export type HistoryChanges<K extends string = string> = {
  previous: Partial<Record<K, string>>;
  updated: Partial<Record<K, string>>;
};

export type OrderStatusChange = {
  previous: ORDER_STATUS;
  updated: ORDER_STATUS;
};

export interface ICreateDeliveryCaseUI extends ICase {
  deliveryType: DELIVERY_CONDITION.DELIVERY;
  deliveryLocation: DELIVERY_LOCATION;
  deliveryData: Partial<IDeliveryInfo>;
  deliveryDateAction: DeliveryDateAction;
}

export interface ICreatePickupDeliveryCaseUI extends ICase {
  deliveryType: DELIVERY_CONDITION.PICKUP;
  country: COUNTRY;
  deliveryDateAction: DeliveryDateAction;
}

export type DeliveryDateAction = (page: ScheduleDeliveryPage) => Promise<Date>;
