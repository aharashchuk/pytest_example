import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { productSchema } from "./product.schema";

export const createProductSchema = {
  type: "object",
  properties: {
    Product: productSchema,
    ...obligatoryFieldsSchema,
  },
  required: ["Product", ...obligatoryRequiredFields],
};
