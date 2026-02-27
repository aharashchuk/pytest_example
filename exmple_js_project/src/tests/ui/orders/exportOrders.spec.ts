import { test, expect } from "fixtures";
import { parseDownloadedExport } from "utils/files/exportFile.utils";
import { TAGS } from "data/tags";
import { TIMEOUT_50_S } from "data/salesPortal/constants";
import type { ExportedFile } from "utils/files/exportFile.utils";
import { ORDER_STATUS } from "data/salesPortal/order-status";

test.describe("[UI][Orders][Export]", () => {
  let token = "";

  test.beforeAll(async ({ loginApiService }) => {
    token = await loginApiService.loginAsAdmin();
  });

  test.beforeEach(async ({ cleanup }) => {
    void cleanup;
  });

  test.afterEach(async ({ ordersApiService }, testInfo) => {
    testInfo.setTimeout(testInfo.timeout + TIMEOUT_50_S);
    await ordersApiService.fullDelete(token);
  });

  const asCsv = (exported: ExportedFile) => {
    if (exported.format !== "csv") {
      throw new Error(`Expected CSV export, got: ${exported.format}`);
    }
    return exported.data;
  };

  test(
    "JSON => all options selected",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersListPage }, testInfo) => {
      await ordersApiService.createOrderAndEntities(token, 1);
      await ordersApiService.createOrderInProcess(token, 1);
      await ordersApiService.createPartiallyReceivedOrder(token, 1);
      await ordersApiService.createReceivedOrder(token, 1);
      await ordersApiService.createCanceledOrder(token, 1);

      await ordersListPage.open("#/orders");
      await ordersListPage.waitForOpened();

      await ordersListPage.openExportModal();
      await ordersListPage.exportModal.selectFormat("JSON");
      await ordersListPage.exportModal.checkAllFields();

      const download = await ordersListPage.exportModal.downloadFile();
      const exported = await parseDownloadedExport(download, testInfo);

      expect(exported.format).toBe("json");
      expect(Array.isArray(exported.data)).toBe(true);

      const arr = exported.data as unknown[];
      expect(arr.length).toBeGreaterThan(0);
      expect(typeof arr[0]).toBe("object");
      expect(arr[0]).not.toBeNull();
    },
  );

  test(
    "CSV => 1 option selected",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersListPage }, testInfo) => {
      await ordersApiService.createOrderAndEntities(token, 1);
      await ordersApiService.createOrderInProcess(token, 1);
      await ordersApiService.createPartiallyReceivedOrder(token, 1);
      await ordersApiService.createReceivedOrder(token, 1);
      await ordersApiService.createCanceledOrder(token, 1);

      await ordersListPage.open("#/orders");
      await ordersListPage.waitForOpened();

      await ordersListPage.openExportModal();
      await ordersListPage.exportModal.selectFormat("CSV");
      await ordersListPage.exportModal.uncheckAllFields();
      await ordersListPage.exportModal.checkFieldsBulk(["Status"]);

      const download = await ordersListPage.exportModal.downloadFile();
      const exported = await parseDownloadedExport(download, testInfo);

      expect(exported.format).toBe("csv");

      const csv = asCsv(exported);
      expect(csv.length).toBeGreaterThanOrEqual(3);

      const allowedStatuses = new Set(Object.values(ORDER_STATUS));
      const exportedStatuses = csv.map((record) => record["Status"]).filter(Boolean);
      expect(exportedStatuses.length).toBeGreaterThan(0);
      for (const status of exportedStatuses) {
        expect(allowedStatuses.has(status as ORDER_STATUS)).toBe(true);
      }
    },
  );

  test(
    "CSV => default pre-selected",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersListPage }, testInfo) => {
      await ordersApiService.createOrderAndEntities(token, 1);
      await ordersApiService.createOrderInProcess(token, 1);
      await ordersApiService.createPartiallyReceivedOrder(token, 1);
      await ordersApiService.createReceivedOrder(token, 1);
      await ordersApiService.createCanceledOrder(token, 1);

      await ordersListPage.open("#/orders");
      await ordersListPage.waitForOpened();

      await ordersListPage.openExportModal();
      // don't touch format (default is expected to be CSV)
      await ordersListPage.exportModal.uncheckAllFields();
      await ordersListPage.exportModal.checkFieldsBulk(["Status", "Total Price", "Customer", "Products", "Created On"]);

      const download = await ordersListPage.exportModal.downloadFile();
      const exported = await parseDownloadedExport(download, testInfo);

      expect(exported.format).toBe("csv");

      const csv = asCsv(exported);
      expect(csv.length).toBeGreaterThanOrEqual(3);

      // Minimal header validation based on real export columns
      const requiredColumns = ["Status", "Total Price", "Created On"];
      for (const column of requiredColumns) {
        expect(Object.prototype.hasOwnProperty.call(csv[0] ?? {}, column)).toBe(true);
      }

      const allowedStatuses = new Set(Object.values(ORDER_STATUS));
      const fileStatuses = csv.map((record) => record["Status"]).filter(Boolean);
      for (const status of fileStatuses) {
        expect(allowedStatuses.has(status as ORDER_STATUS)).toBe(true);
      }
    },
  );

  test(
    "W/o selected options in checkboxes",
    { tag: [TAGS.UI, TAGS.ORDERS, TAGS.REGRESSION] },
    async ({ ordersApiService, ordersListPage }) => {
      await ordersApiService.createOrderAndEntities(token, 1);

      await ordersListPage.open("#/orders");
      await ordersListPage.waitForOpened();

      await ordersListPage.openExportModal();
      await ordersListPage.exportModal.selectFormat("CSV");
      await ordersListPage.exportModal.uncheckAllFields();
      await expect(ordersListPage.exportModal.downloadButton).toBeVisible();
      await expect(ordersListPage.exportModal.downloadButton).toBeDisabled();
    },
  );
});
