import { COUNTRY } from "./country";

export enum DELIVERY_CONDITION {
  DELIVERY = "Delivery",
  PICKUP = "Pickup",
}

export interface IDeliveryAddress {
  country: COUNTRY;
  city: string;
  street: string;
  house: number;
  flat: number;
}

export interface IDeliveryInfo {
  address: IDeliveryAddress;
  condition: DELIVERY_CONDITION;
  finalDate: string;
}

export enum DELIVERY_LOCATION {
  HOME = "Home",
  OTHER = "Other",
}
