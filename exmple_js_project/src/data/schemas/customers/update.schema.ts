import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { customerSchema } from "./customer.schema";

export const updateCustomerSchema = {
  type: "object",
  properties: {
    Customer: customerSchema,
    ...obligatoryFieldsSchema,
  },
  required: ["Customer", ...obligatoryRequiredFields],
};
