import { faker } from "@faker-js/faker";
import { IProduct, IProductFromResponse, IOrderProductFromResponse } from "data/types/product.types";
import { getRandomEnumValue } from "utils/enum.utils";
import { MANUFACTURERS } from "./manufacturers";
import { ObjectId } from "bson";
import _ from "lodash";

export function generateProductData(params?: Partial<IProduct>): IProduct {
  return {
    name: faker.commerce.product() + faker.number.int({ min: 1, max: 100000 }),
    manufacturer: getRandomEnumValue(MANUFACTURERS),
    price: faker.number.int({ min: 1, max: 99999 }),
    amount: faker.number.int({ min: 0, max: 999 }),
    notes: faker.string.alphanumeric({ length: 250 }),
    ...params,
  };
}
export function generateProductResponseData(params?: Partial<IProduct>): IProductFromResponse {
  const initial = generateProductData(params);
  return {
    _id: new ObjectId().toHexString(),
    name: initial.name,
    amount: initial.amount,
    price: initial.price,
    manufacturer: initial.manufacturer,
    createdOn: new Date().toISOString(),
    notes: initial.notes!,
  };
}

export function generateIOrderProductFromResponse(
  params?: Partial<IOrderProductFromResponse>,
): IOrderProductFromResponse {
  const initial = _.omit(generateProductResponseData(params), "createdOn");
  return {
    ...initial,
    received: params?.received || false,
  };
}
