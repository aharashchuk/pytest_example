import { obligatoryFieldsSchema, obligatoryRequiredFields } from "../core.schema";
import { productSchema } from "./product.schema";

export const getAllProductsSchema = {
  type: "object",
  properties: {
    Products: {
      type: "array",
      items: productSchema,
    },
    ...obligatoryFieldsSchema,
  },
  required: ["Products", ...obligatoryRequiredFields],
};
