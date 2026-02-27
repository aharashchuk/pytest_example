import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { ROLES } from "data/types/user.types";

export const userSchema = {
  type: "object",
  properties: {
    _id: { type: "string" },
    username: { type: "string" },
    firstName: { type: "string" },
    lastName: { type: "string" },
    roles: {
      type: "array",
      items: {
        type: "string",
        enum: Object.values(ROLES),
      },
    },
    createdOn: { type: "string" },
  },
  required: ["_id", "username", "firstName", "lastName", "roles", "createdOn"],
  additionalProperties: false,
};

export const getUserSchema = {
  type: "object",
  properties: {
    User: userSchema,
    ...obligatoryFieldsSchema,
  },
  required: ["User", ...obligatoryRequiredFields],
  additionalProperties: false,
};

export const getAllUsersSchema = {
  type: "object",
  properties: {
    Users: {
      type: "array",
      items: userSchema,
    },
    ...obligatoryFieldsSchema,
  },
  required: ["Users", ...obligatoryRequiredFields],
  additionalProperties: false,
};
