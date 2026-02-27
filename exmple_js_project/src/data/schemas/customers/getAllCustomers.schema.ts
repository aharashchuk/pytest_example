import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { customerSchema } from "./customer.schema";

export const getAllCustomersSchema = {
  type: "object",
  properties: {
    Customers: {
      type: "array",
      items: customerSchema,
    },
    ...obligatoryFieldsSchema,
  },
  required: ["Customers", ...obligatoryRequiredFields],
};
