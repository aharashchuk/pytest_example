import { faker } from "@faker-js/faker";
import { ICustomer, ICustomerFromResponse } from "data/types/customer.types";
import { getRandomEnumValue } from "utils/enum.utils";
import { ObjectId } from "bson";
import { COUNTRY } from "../country";

function onlyLetters(input: string, max: number) {
  const cleaned = input
    .replace(/[^A-Za-z ]+/g, " ")
    .replace(/\s{2,}/g, " ")
    .trim();
  return cleaned.slice(0, max) || "John";
}

function alphaNumSpace(input: string, max: number) {
  const cleaned = input
    .replace(/[^A-Za-z0-9 ]+/g, " ")
    .replace(/\s{2,}/g, " ")
    .trim();
  return cleaned.slice(0, max) || "Main";
}

function validEmail() {
  return faker.internet.email().replace(/\s+/g, "");
}

function validPhone() {
  // '+' and 10-15 digits to match strict validator without precision issues
  const digits = faker.string.numeric({ length: 15, allowLeadingZeros: true });
  return "+" + digits;
}

function validNotes(max = 250) {
  return faker.string.alphanumeric({ length: Math.min(30, max) });
}

export function generateCustomerData(params?: Partial<ICustomer>): ICustomer {
  const nameRaw = `${faker.person.firstName()} ${faker.person.lastName()}`;
  const cityRaw = faker.location.city();
  const streetRaw = `${faker.location.street()} ${faker.number.int({ min: 1, max: 99 })}`;

  const data: ICustomer = {
    email: validEmail(),
    name: onlyLetters(nameRaw, 40),
    country: getRandomEnumValue(COUNTRY),
    city: onlyLetters(cityRaw, 20),
    street: alphaNumSpace(streetRaw, 40),
    house: faker.number.int({ min: 1, max: 999 }),
    flat: faker.number.int({ min: 1, max: 9999 }),
    phone: validPhone(),
    notes: validNotes(250),
  };

  return { ...data, ...params };
}

export function generateCustomerResponseData(params?: Partial<ICustomer>): ICustomerFromResponse {
  const initial = generateCustomerData(params);
  return {
    _id: new ObjectId().toHexString(),
    email: initial.email,
    name: initial.name,
    country: initial.country,
    city: initial.city,
    street: initial.street,
    house: initial.house,
    flat: initial.flat,
    phone: initial.phone,
    createdOn: new Date().toISOString(),
    notes: initial.notes!,
  };
}
