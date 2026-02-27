import { orderFromResponseSchema } from "./order.schema";
import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { OrdersTableHeader } from "data/types/order.types";

export const getAllOrdersSchema = {
  type: "object",
  properties: {
    orders: {
      type: "array",
      items: orderFromResponseSchema,
    },
    total: { type: "number" },
    page: { type: "number" },
    limit: { type: "number" },
    search: { type: "string" },
    status: {
      type: "array",
      items: {
        type: "string",
        enum: Object.values(ORDER_STATUS),
      },
    },
    sorting: {
      type: "object",
      properties: {
        sortField: {
          type: "string",
          enum: [
            "orderNumber",
            "email",
            "price",
            "delivery",
            "status",
            "assignedManager",
            "createdOn",
          ] as OrdersTableHeader[],
        },
        sortOrder: {
          type: "string",
          enum: ["asc", "desc"],
        },
      },
      required: ["sortField", "sortOrder"],
      additionalProperties: false,
    },
    ...obligatoryFieldsSchema,
  },
  required: ["orders", "total", "page", "limit", "search", "status", "sorting", ...obligatoryRequiredFields],
  additionalProperties: false,
};
