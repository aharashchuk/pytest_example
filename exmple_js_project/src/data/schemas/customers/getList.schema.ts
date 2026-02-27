import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { customerSchema } from "./customer.schema";

export const getListCustomersSchema = {
  type: "object",
  properties: {
    Customers: {
      type: "array",
      items: customerSchema,
    },
    total: { type: "number" },
    page: { type: "number" },
    limit: { type: "number" },
    search: { type: "string" },
    country: { type: "array" },
    sorting: { type: "object" },
    ...obligatoryFieldsSchema,
  },
  required: ["Customers", ...obligatoryRequiredFields],
};
