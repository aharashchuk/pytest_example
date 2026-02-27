import { expect } from "@playwright/test";
import { IResponse, IResponseFields } from "data/types/core.types";
import { validateJsonSchema } from "./validateSchema.utils";

export function validateResponse<T extends IResponseFields | null>(
  response: IResponse<T>,
  expected: {
    status: number;
    IsSuccess?: boolean;
    ErrorMessage?: string | null;
    schema?: object;
  },
) {
  expect.soft(response.status).toBe(expected.status);
  if ("IsSuccess" in expected) {
    expect.soft(response.body!.IsSuccess).toBe(expected.IsSuccess);
  }
  if ("ErrorMessage" in expected) {
    expect.soft(response.body!.ErrorMessage).toBe(expected.ErrorMessage);
  }
  if (expected.schema) validateJsonSchema(response.body!, expected.schema);
}
