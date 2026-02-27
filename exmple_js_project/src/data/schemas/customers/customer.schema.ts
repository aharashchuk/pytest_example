import { obligatoryRequiredFields } from "../core.schema";
import { COUNTRY } from "data/salesPortal/country";

export const customerSchema = {
  type: "object",
  properties: {
    email: { type: "string" },
    name: { type: "string" },
    country: { type: "string", enum: Object.values(COUNTRY) },
    city: { type: "string" },
    street: { type: "string" },
    house: { type: "number" },
    flat: { type: "number" },
    phone: { type: "string" },
    createdOn: { type: "string" },
    notes: { type: "string" },
    _id: { type: "string" },
  },
  required: ["email", "name", "country", "city", "street", "house", "flat", "phone", "createdOn", "_id"],
};

export const createCustomerSchema = {
  type: "object",
  properties: {
    Customer: customerSchema,
    ...obligatoryRequiredFields,
  },
  required: ["Customer", ...obligatoryRequiredFields],
};
