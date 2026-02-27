import { faker } from "@faker-js/faker";
import { COUNTRY } from "../country";
import { DELIVERY_CONDITION, IDeliveryInfo } from "data/salesPortal/delivery-status";
import { convertToDate } from "utils/date.utils";
import { getRandomEnumValue } from "utils/enum.utils";
import moment from "moment";

export function generateDelivery(customData: Partial<IDeliveryInfo> = {}): IDeliveryInfo {
  const baseAddress = {
    country: getRandomEnumValue(COUNTRY),
    city: faker.location.city().replace(/[.'’\-–—]/g, ""),
    street: faker.location.street().replace(/[.'’\-–—]/g, ""),
    house: faker.number.int({ min: 1, max: 999 }),
    flat: faker.number.int({ min: 1, max: 9999 }),
  };

  const finalDate = moment().add(7, "days").toISOString();

  return {
    address: baseAddress,
    finalDate: convertToDate(finalDate),
    condition: DELIVERY_CONDITION.DELIVERY,
    ...customData,
  };
}
