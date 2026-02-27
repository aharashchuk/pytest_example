export const obligatoryFieldsSchema = {
  IsSuccess: { type: "boolean" },
  ErrorMessage: {
    type: ["string", "null"],
  },
};

export const obligatoryRequiredFields = ["IsSuccess", "ErrorMessage"];
