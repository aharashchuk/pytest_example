import { DELIVERY_CONDITION } from "data/salesPortal/delivery-status";

export const deliveryAddressSchema = {
  type: "object",
  properties: {
    country: { type: "string" },
    city: { type: "string" },
    street: { type: "string" },
    house: { type: "number" },
    flat: { type: "number" },
  },
  required: ["country", "city", "street", "house", "flat"],
  additionalProperties: false,
};

export const deliveryInfoSchema = {
  type: "object",
  properties: {
    address: deliveryAddressSchema,
    finalDate: { type: "string" },
    condition: {
      type: "string",
      enum: Object.values(DELIVERY_CONDITION),
    },
  },
  required: ["address", "condition", "finalDate"],
  additionalProperties: false,
};
