import { ICreatedOn } from "./core.types";
import { ID, IResponseFields } from "./core.types";
import { ICaseApi } from "./core.types";
import { NOTIFICATIONS_TYPES } from "data/salesPortal/notifications";

export interface INotification extends ID {
  userId: ID;
  type: NOTIFICATIONS_TYPES;
  orderId: ID;
  message: string;
  read: boolean;
  createdAt: ICreatedOn;
  expiresAt: ICreatedOn;
  updatedAt: ICreatedOn;
}

export interface INotificationsResponse extends IResponseFields {
  Notifications: INotification[];
}

export interface ICreateNotificationCase extends ICaseApi {
  id?: ID["_id"];
}
