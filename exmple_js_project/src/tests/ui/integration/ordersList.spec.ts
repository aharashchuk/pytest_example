import { TAGS } from "data/tags";
import { test, expect } from "fixtures";
import { generateOrdersResponseData } from "data/salesPortal/orders/generateOrderData";
import { ordersListIntegrationData } from "data/salesPortal/orders/ordersListIntegrationData";
import { apiConfig } from "config/apiConfig";
import { SortOrder } from "data/types/core.types";
import { IOrderInTable } from "data/types/order.types";

test.describe("[Integration][Orders][Table Sorting]", () => {
  const directions = ["asc", "desc"] as SortOrder[];
  for (const { title, ordersCount, sorting } of ordersListIntegrationData) {
    test(
      title,
      { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION, TAGS.INTEGRATION] },
      async ({ mock, ordersListPage }) => {
        const header = sorting!.sortField;
        const direction = sorting!.sortOrder;
        const orders = generateOrdersResponseData(ordersCount, sorting);

        await mock.ordersPage({
          ...orders,
          sorting: {
            sortField: header!,
            sortOrder: directions.find((el) => el !== direction)!,
          },
        });

        await ordersListPage.open("#/orders");
        await ordersListPage.waitForOpened();

        await mock.ordersPage({
          ...orders,
          sorting: {
            sortField: header!,
            sortOrder: direction,
          },
        });

        await ordersListPage.expectRequest(
          "GET",
          apiConfig.endpoints.orders,
          {
            sortField: header,
            sortOrder: direction,
          },
          ordersListPage.sortBy.bind(ordersListPage),
          header,
          direction,
        );

        await ordersListPage.waitForOpened();
        await expect(ordersListPage.tableHeaderArrow(header, { direction })).toBeVisible();
        const ordersList = orders.Orders;
        const tableData = (await ordersListPage.getTableData()) as IOrderInTable[];
        expect.soft(tableData.length).toBe(ordersList.length);
        tableData.forEach((order, i) => {
          const expectedId = ordersList[i]?._id;
          expect(order.orderId).toEqual(expectedId);
        });
      },
    );
  }
});
