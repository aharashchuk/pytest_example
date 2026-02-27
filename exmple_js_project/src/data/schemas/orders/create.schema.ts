import { orderFromResponseSchema } from "./order.schema";
import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";

export const createOrderSchema = {
  type: "object",
  properties: {
    Order: orderFromResponseSchema,
    ...obligatoryFieldsSchema,
  },
  required: ["Order", ...obligatoryRequiredFields],
  additionalProperties: false,
};
