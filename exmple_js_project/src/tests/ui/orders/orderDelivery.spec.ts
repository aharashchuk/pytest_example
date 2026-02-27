import { expect, test } from "fixtures";
import _ from "lodash";
import { applyDeliveryCase, applyPickupCase } from "utils/orders/helpers";
import { TAGS } from "data/tags";
import { DELIVERY_CONDITION } from "data/salesPortal/delivery-status";
import {
  DEFAULT_SCHEDULE_FORM_CASES,
  CREATE_DELIVERY_POSITIVE_CASES_UI,
  CREATE_PICKUP_POSITIVE_CASES_UI,
  EDIT_PICKUP_POSITIVE_CASES_UI,
} from "data/salesPortal/orders/createDeliveryDDT";

test.describe("[Create/edit delivery]", () => {
  test.beforeEach(async ({ cleanup }) => {
    void cleanup;
  });

  test.describe("DDT - Default Schedule form", () => {
    for (const tc of DEFAULT_SCHEDULE_FORM_CASES) {
      test(
        tc.title,
        async ({ ordersApiService, ordersApi, loginApiService, orderDetailsUIService, orderDetailsPage }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderAndEntities(token, 1);
          const orderResponse = await ordersApi.getById(order._id, token);
          const customer = orderResponse.body.Order.customer;
          await orderDetailsUIService.openOrderDelivery(order._id);
          await orderDetailsUIService.openScheduleDeliveryForm();
          await expect(orderDetailsPage.scheduleDeliveryPage.title).toHaveText("Schedule Delivery");
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeDisabled();
          const scheduleDeliveryInfo = await orderDetailsPage.scheduleDeliveryPage.getScheduleDeliveryData();
          const customerComparable = _.omit(customer, ["_id", "email", "name", "phone", "createdOn", "notes"]);
          const scheduleDeliveryComparable = _.omit(scheduleDeliveryInfo, ["deliveryType", "deliveryDate", "location"]);
          expect(scheduleDeliveryComparable).toEqual(customerComparable);
        },
      );
    }
  });

  test.describe("DDT - Schedule first delivery (Delivery)", () => {
    for (const tc of CREATE_DELIVERY_POSITIVE_CASES_UI) {
      test(
        tc.title,
        { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
        async ({ ordersApiService, loginApiService, orderDetailsUIService, orderDetailsPage }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderAndEntities(token, 1);
          await orderDetailsUIService.openOrderDelivery(order._id);
          await orderDetailsUIService.openScheduleDeliveryForm();
          await expect(orderDetailsPage.scheduleDeliveryPage.title).toHaveText("Schedule Delivery");
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeDisabled();
          await applyDeliveryCase(orderDetailsPage.scheduleDeliveryPage, tc, orderDetailsUIService);
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeEnabled();
          const formInfo = await orderDetailsPage.scheduleDeliveryPage.getScheduleDeliveryData();
          const expectedForDeliveryTab = _.omit(formInfo, ["location"]);
          await orderDetailsUIService.clickSaveDelivery();
          const actual = await orderDetailsPage.deliveryTab.getData();
          expect(actual).toEqual(expectedForDeliveryTab);
        },
      );
    }
  });

  test.describe("DDT - Edit delivery (Delivery)", () => {
    for (const tc of CREATE_DELIVERY_POSITIVE_CASES_UI) {
      test(
        tc.title,
        { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
        async ({ ordersApiService, loginApiService, orderDetailsPage, orderDetailsUIService }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderAndEntities(token, 1);
          await orderDetailsUIService.openOrderDelivery(order._id);
          await orderDetailsUIService.openScheduleDeliveryForm();
          await applyDeliveryCase(orderDetailsPage.scheduleDeliveryPage, tc, orderDetailsUIService);
          await orderDetailsUIService.clickSaveDelivery();
          await orderDetailsUIService.openScheduleDeliveryForm();
          await expect(orderDetailsPage.scheduleDeliveryPage.title).toHaveText("Edit Delivery");
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeDisabled();
          await applyDeliveryCase(orderDetailsPage.scheduleDeliveryPage, tc, orderDetailsUIService);
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeEnabled();
          const formInfo = await orderDetailsPage.scheduleDeliveryPage.getScheduleDeliveryData();
          const expectedForDeliveryTab = _.omit(formInfo, ["location"]);
          await orderDetailsUIService.clickSaveDelivery();
          const actual = await orderDetailsPage.deliveryTab.getData();
          expect(actual).toEqual(expectedForDeliveryTab);
        },
      );
    }
  });

  test.describe("DDT - Schedule first delivery (Pickup)", () => {
    for (const tc of CREATE_PICKUP_POSITIVE_CASES_UI) {
      test(
        tc.title,
        { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
        async ({ ordersApiService, loginApiService, orderDetailsPage, orderDetailsUIService }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderAndEntities(token, 1);
          await orderDetailsUIService.openOrderDelivery(order._id);
          await orderDetailsUIService.openScheduleDeliveryForm();
          await expect(orderDetailsPage.scheduleDeliveryPage.title).toHaveText("Schedule Delivery");
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeDisabled();
          await applyPickupCase(orderDetailsPage.scheduleDeliveryPage, tc, orderDetailsUIService);
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeEnabled();
          const expected = await orderDetailsPage.scheduleDeliveryPage.getScheduleDeliveryData();
          expect(expected.deliveryType).toBe(DELIVERY_CONDITION.PICKUP);
          await orderDetailsUIService.clickSaveDelivery();
          const actual = await orderDetailsPage.deliveryTab.getData();
          expect(actual).toEqual(expected);
        },
      );
    }
  });

  test.describe("DDT - Edit delivery (Pickup)", () => {
    for (const tc of EDIT_PICKUP_POSITIVE_CASES_UI) {
      test(
        tc.title,
        { tag: [TAGS.REGRESSION, TAGS.UI, TAGS.ORDERS] },
        async ({ ordersApiService, loginApiService, orderDetailsPage, orderDetailsUIService }) => {
          const token = await loginApiService.loginAsAdmin();
          const order = await ordersApiService.createOrderAndEntities(token, 1);
          await orderDetailsUIService.openOrderDelivery(order._id);
          await orderDetailsUIService.openScheduleDeliveryForm();
          await applyPickupCase(orderDetailsPage.scheduleDeliveryPage, tc, orderDetailsUIService);
          await orderDetailsUIService.clickSaveDelivery();
          await orderDetailsUIService.openScheduleDeliveryForm();
          await expect(orderDetailsPage.scheduleDeliveryPage.title).toHaveText("Edit Delivery");
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeDisabled();
          await applyPickupCase(orderDetailsPage.scheduleDeliveryPage, tc, orderDetailsUIService);
          await expect(orderDetailsPage.scheduleDeliveryPage.saveButton).toBeEnabled();
          const expected = await orderDetailsPage.scheduleDeliveryPage.getScheduleDeliveryData();
          expect(expected.deliveryType).toBe(DELIVERY_CONDITION.PICKUP);
          await orderDetailsUIService.clickSaveDelivery();
          const actual = await orderDetailsPage.deliveryTab.getData();
          expect(actual).toEqual(expected);
        },
      );
    }
  });
});
