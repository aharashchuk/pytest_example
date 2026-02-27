import { customerSchema } from "../customers/customer.schema";
import { deliveryInfoSchema } from "../delivery/delivery.schema";
import { ORDER_STATUS, ORDER_HISTORY_ACTIONS } from "data/salesPortal/order-status";
import { userSchema } from "../users/user.schema";

export const orderProductSchema = {
  type: "object",
  properties: {
    _id: { type: "string" },
    name: { type: "string" },
    amount: { type: "number" },
    price: { type: "number" },
    manufacturer: { type: "string" },
    notes: { type: "string" },
    received: { type: "boolean" },
  },
  required: ["_id", "name", "amount", "price", "manufacturer", "notes", "received"],
  additionalProperties: false,
};

export const commentSchema = {
  type: "object",
  properties: {
    _id: { type: "string" },
    text: { type: "string" },
    createdOn: { type: "string" },
  },
  required: ["_id", "text", "createdOn"],
  additionalProperties: false,
};

export const performerSchema = {
  type: "object",
  properties: {
    _id: { type: "string" },
    username: { type: "string" },
    firstName: { type: "string" },
    lastName: { type: "string" },
    roles: {
      type: "array",
      items: { type: "string" },
    },
    createdOn: { type: "string" },
  },
  required: ["_id", "username", "firstName", "lastName", "roles", "createdOn"],
  additionalProperties: false,
};

export const orderHistorySchema = {
  type: "object",
  properties: {
    status: {
      type: "string",
      enum: Object.values(ORDER_STATUS),
    },
    customer: { type: "string" },
    products: {
      type: "array",
      items: orderProductSchema,
    },
    total_price: { type: "number" },
    delivery: {
      anyOf: [deliveryInfoSchema, { type: "null" }],
    },
    assignedManager: { anyOf: [userSchema, { type: "null" }] },
    changedOn: { type: "string" },
    action: {
      type: "string",
      enum: Object.values(ORDER_HISTORY_ACTIONS),
    },
    performer: performerSchema,
  },
  required: [
    "status",
    "customer",
    "products",
    "total_price",
    "delivery",
    "assignedManager",
    "changedOn",
    "action",
    "performer",
  ],
  additionalProperties: false,
};

export const orderFromResponseSchema = {
  type: "object",
  properties: {
    _id: { type: "string" },
    status: {
      type: "string",
      enum: Object.values(ORDER_STATUS),
    },
    customer: customerSchema,
    products: {
      type: "array",
      items: orderProductSchema,
    },
    delivery: {
      anyOf: [deliveryInfoSchema, { type: "null" }],
    },
    total_price: { type: "number" },
    createdOn: { type: "string" },
    comments: {
      type: "array",
      items: commentSchema,
    },
    history: {
      type: "array",
      items: orderHistorySchema,
    },
    assignedManager: {
      anyOf: [userSchema, { type: "null" }],
    },
  },
  required: [
    "_id",
    "status",
    "customer",
    "products",
    "total_price",
    "createdOn",
    "comments",
    "history",
    "assignedManager",
    "delivery",
  ],
  additionalProperties: false,
};
