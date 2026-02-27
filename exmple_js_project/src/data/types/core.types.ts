import { STATUS_CODES } from "data/statusCodes";

export interface ID {
  _id: string;
}

export interface IResponseFields {
  IsSuccess: boolean;
  ErrorMessage: string | null;
}

export interface IRequestOptions {
  baseURL: string;
  url: string;
  method: "get" | "post" | "put" | "delete" | "patch";
  data?: object;
  headers?: Record<string, string>;
}

export interface IResponse<T extends object | null> {
  status: number;
  headers: Record<string, string>;
  body: T;
}

export interface ICreatedOn {
  createdOn: string;
}

export type SortOrder = "asc" | "desc";

export interface ICase {
  title: string;
}
export interface ICaseApi extends ICase {
  _id?: string;
  expectedStatus: STATUS_CODES;
  expectedErrorMessage: string | null;
  isSuccess?: boolean;
}
