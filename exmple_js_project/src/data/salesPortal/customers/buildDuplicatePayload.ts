import { ICustomer } from "data/types/customer.types";
import { generateCustomerData } from "./generateCustomerData";

export function buildDuplicatePayload(original: ICustomer): ICustomer {
  return generateCustomerData({ email: original.email });
}
