import { obligatoryRequiredFields, obligatoryFieldsSchema } from "../core.schema";

export const loginSchema = {
  type: "object",
  properties: {
    ...obligatoryFieldsSchema,
  },
  required: [...obligatoryRequiredFields],
};
