import { STATUS_CODES } from "data/statusCodes";
import { RESPONSE_ERRORS } from "../errors";
import { ICreateDeliveryCase } from "data/types/order.types";
import { generateDelivery } from "data/salesPortal/orders/generateDeliveryData";
import {
  IDeliveryInfo,
  DELIVERY_CONDITION,
  IDeliveryAddress,
  DELIVERY_LOCATION,
} from "data/salesPortal/delivery-status";
import { COUNTRY } from "../country";
import { getRandomEnumValue } from "utils/enum.utils";
import { faker } from "@faker-js/faker";
import _ from "lodash";
import { ICase } from "data/types/core.types";
import { ICreateDeliveryCaseUI, ICreatePickupDeliveryCaseUI } from "data/types/delivery.types";

const createAddressVariation = (overrides: Partial<IDeliveryAddress>): IDeliveryAddress => ({
  country: getRandomEnumValue(COUNTRY),
  city: "New York",
  street: "5th Avenue",
  house: 1,
  flat: 101,
  ...overrides,
});

const createDeliveryWithoutAddressField = (field: keyof IDeliveryAddress): Partial<IDeliveryInfo> => {
  const delivery = generateDelivery();
  return {
    ...delivery,
    address: _.omit(delivery.address, field),
  } as Partial<IDeliveryInfo>;
};

export const CREATE_DELIVERY_POSITIVE_CASES: ICreateDeliveryCase[] = [
  {
    title: "Successfully set delivery info with all required fields",
    deliveryData: generateDelivery(),
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    title: "Successfully set pickup condition",
    deliveryData: generateDelivery({ condition: DELIVERY_CONDITION.PICKUP }),
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    title: "Successfully update with future date",
    deliveryData: generateDelivery({ finalDate: "2025/12/31" }),
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
  {
    title: "Single character city name",
    deliveryData: generateDelivery({
      address: createAddressVariation({ city: "A" }),
    }),
    expectedStatus: STATUS_CODES.OK,
    expectedErrorMessage: null,
  },
];

const MISSING_FIELDS_CASES: ICreateDeliveryCase[] = [
  {
    title: "Missing finalDate field",
    deliveryData: _.omit(generateDelivery(), "finalDate"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Missing condition field",
    deliveryData: _.omit(generateDelivery(), "condition"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Missing address field",
    deliveryData: _.omit(generateDelivery(), "address"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Missing country in address",
    deliveryData: createDeliveryWithoutAddressField("country"),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];

const INVALID_VALUES_CASES: ICreateDeliveryCase[] = [
  {
    title: "Invalid condition value",
    deliveryData: generateDelivery({ condition: "Express" as DELIVERY_CONDITION }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
  {
    title: "Invalid date format",
    deliveryData: generateDelivery({ finalDate: "15-01-2026" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INVALID_DATE,
  },
  {
    title: "Past date",
    deliveryData: generateDelivery({ finalDate: "2024/12/31" }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.BAD_REQUEST,
  },
];

const ADDRESS_VALIDATION_CASES: ICreateDeliveryCase[] = [
  {
    title: "Negative house number",
    deliveryData: generateDelivery({ address: createAddressVariation({ house: -1 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
  {
    title: "Zero flat number",
    deliveryData: generateDelivery({ address: createAddressVariation({ flat: 0 }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
  {
    title: "Empty city",
    deliveryData: generateDelivery({ address: createAddressVariation({ city: "" }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
  {
    title: "Empty street",
    deliveryData: generateDelivery({ address: createAddressVariation({ street: "" }) }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
];

const BOUNDARY_CASES: ICreateDeliveryCase[] = [
  {
    title: "Exceeded Max length city name (>20 chars)",
    deliveryData: generateDelivery({
      address: createAddressVariation({ city: faker.string.alphanumeric({ length: 21 }) }),
    }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
  {
    title: "Exceeded Max length street name (>40 chars)",
    deliveryData: generateDelivery({
      address: createAddressVariation({ street: faker.string.alphanumeric({ length: 41 }) }),
    }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
  {
    title: "Exeeded Max house number (>999)",
    deliveryData: generateDelivery({
      address: createAddressVariation({ house: 1000 }),
    }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
];

const SPECIAL_CHARACTERS_CASES: ICreateDeliveryCase[] = [
  {
    title: "Special characters in street",
    deliveryData: generateDelivery({
      address: createAddressVariation({ street: "!@#$%^&*Street!@#$%^&*" }),
    }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
  {
    title: "Unicode characters in city",
    deliveryData: generateDelivery({
      address: createAddressVariation({ city: "北京市" }),
    }),
    expectedStatus: STATUS_CODES.BAD_REQUEST,
    expectedErrorMessage: RESPONSE_ERRORS.INCORRECT_DELIVERY,
  },
];

export const CREATE_DELIVERY_NEGATIVE_CASES: ICreateDeliveryCase[] = [
  ...MISSING_FIELDS_CASES,
  ...INVALID_VALUES_CASES,
  ...ADDRESS_VALIDATION_CASES,
  ...BOUNDARY_CASES,
  ...SPECIAL_CHARACTERS_CASES,
];

//DELIVERY UI
export const DEFAULT_SCHEDULE_FORM_CASES: ICase[] = [
  {
    title: "Default Schedule Delivery: customer fields are prefilled",
  },
];

export const CREATE_DELIVERY_POSITIVE_CASES_UI: ICreateDeliveryCaseUI[] = [
  {
    title: "Delivery + Other location",
    deliveryType: DELIVERY_CONDITION.DELIVERY,
    deliveryLocation: DELIVERY_LOCATION.OTHER,
    deliveryData: generateDelivery(),
    deliveryDateAction: async (schedulePage) => {
      await schedulePage.dateInput.click();
      return schedulePage.pickRandomAvailableDate();
    },
  },
];

export const CREATE_PICKUP_POSITIVE_CASES_UI: ICreatePickupDeliveryCaseUI[] = [
  {
    title: "Pickup: schedule with country = Canada",
    deliveryType: DELIVERY_CONDITION.PICKUP,
    country: COUNTRY.CANADA,
    deliveryDateAction: (date) => date.pickRandomAvailableDate(),
  },
  {
    title: "Pickup: schedule with country = Great Britain",
    deliveryType: DELIVERY_CONDITION.PICKUP,
    country: COUNTRY.GREAT_BRITAIN,
    deliveryDateAction: (date) => date.pickRandomAvailableDate(),
  },
];

export const EDIT_PICKUP_POSITIVE_CASES_UI: ICreatePickupDeliveryCaseUI[] = [
  {
    title: "Pickup: edit -> change country to Canada",
    deliveryType: DELIVERY_CONDITION.PICKUP,
    country: COUNTRY.CANADA,
    deliveryDateAction: (date) => date.pickRandomAvailableDate(),
  },
  {
    title: "Pickup: edit -> change country to Great Britain",
    deliveryType: DELIVERY_CONDITION.PICKUP,
    country: COUNTRY.GREAT_BRITAIN,
    deliveryDateAction: (date) => date.pickRandomAvailableDate(),
  },
];
