import { ID, IResponseFields, ICreatedOn } from "./core.types";

export enum ROLES {
  ADMIN = "ADMIN",
  USER = "USER",
}
//assignedManager, performer of the order
export interface IUser extends ID, ICreatedOn, IResponseFields {
  username: string;
  firstName: string;
  lastName: string;
  roles: ROLES[];
}
export type IUserFromResponse = IUser;

export type IAssignedManager = IUserFromResponse;

export interface ICreateUserPayload {
  username: string;
  password: string;
  firstName: string;
  lastName: string;
}
