import { COUNTRY } from "data/salesPortal/country";
import { DELIVERY_CONDITION, DELIVERY_LOCATION } from "data/salesPortal/delivery-status";
import { ICreateDeliveryCaseUI, ICreatePickupDeliveryCaseUI } from "data/types/delivery.types";
import { IOrderFromResponse } from "data/types/order.types";
import { ScheduleDeliveryPage } from "ui/pages/orders/components/delivery/scheduleDelivery.page";
import { OrderDetailsUIService } from "ui/service/orderDetails.ui-service";

export const productIdsOf = (order: IOrderFromResponse): string[] => order.products.map((p) => p._id);

export const calcTotal = (order: IOrderFromResponse): number =>
  order.products.reduce((sum: number, p) => sum + p.price, 0);

export async function applyDeliveryCase(
  page: ScheduleDeliveryPage,
  tc: ICreateDeliveryCaseUI,
  ui: OrderDetailsUIService,
) {
  await page.deliveryTypeSelect.selectOption({ label: tc.deliveryType });
  await page.locationSelect.selectOption({ label: tc.deliveryLocation });
  const addr = tc.deliveryData.address;
  if (tc.deliveryLocation === DELIVERY_LOCATION.HOME) {
    await ui.assertDeliveryHomeLocks();
    await page.pickDateIfNeeded(tc.deliveryDateAction);
    return;
  }
  if (addr?.country) await page.countryField.selectOption({ label: addr.country });
  if (addr?.city !== undefined) await page.cityInput.fill(String(addr.city));
  if (addr?.street !== undefined) await page.streetInput.fill(String(addr.street));
  if (addr?.house !== undefined) await page.houseInput.fill(String(addr.house));
  if (addr?.flat !== undefined) await page.flatInput.fill(String(addr.flat));
  await page.pickDateIfNeeded(tc.deliveryDateAction);
}

export async function applyPickupCase(
  page: ScheduleDeliveryPage,
  tc: ICreatePickupDeliveryCaseUI,
  ui: OrderDetailsUIService,
) {
  await page.deliveryTypeSelect.selectOption({ label: DELIVERY_CONDITION.PICKUP });
  await ui.assertPickupLocks();
  await page.countryField.selectOption({ label: tc.country as COUNTRY });
  await page.pickDateIfNeeded(tc.deliveryDateAction);
}
