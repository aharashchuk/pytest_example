import { expect, Locator } from "@playwright/test";
import { ORDER_HISTORY_ACTIONS, ORDER_STATUS } from "data/salesPortal/order-status";
import {
  HistoryEventRow,
  HistoryChanges,
  DeliveryHistoryAction,
  DeliveryHistoryField,
  StatusHistoryAction,
  OrderStatusChange,
  ManagerHistoryAction,
  ManagerField,
} from "data/types/delivery.types";
import { logStep } from "utils/report/logStep.utils";
import { SalesPortalPage } from "ui/pages/salesPortal.page";

export class OrderHistoryTab extends SalesPortalPage {
  readonly tab = this.page.locator('#history.tab-pane.active.show[role="tabpanel"]');
  readonly title = this.tab.locator("h4", { hasText: "Order History" });
  readonly body = this.tab.locator("#history-body");

  readonly uniqueElement = this.tab;
  // top headers
  readonly topHeaderRow = this.tab.locator(":scope > div.his-header.py-3.fs-5");
  readonly headers = this.topHeaderRow.locator("span.his-col.fw-bold");

  // accordion headers
  readonly eventRows = this.body.locator(".accordion-header.his-header");

  public rowByActionAndDate(action: ORDER_HISTORY_ACTIONS, dateTime: string): Locator {
    return this.eventRows.filter({ hasText: action }).filter({ hasText: dateTime }).first();
  }

  @logStep("GET INFO FOR SPECIFIC ACTION")
  async getRowInfoByDateAndAction(action: ORDER_HISTORY_ACTIONS, dateTime: string): Promise<HistoryEventRow> {
    const row = this.rowByActionAndDate(action, dateTime);
    await expect(row).toBeVisible();
    const [, performedBy = "", dt = ""] = await row.locator("span.his-col").allInnerTexts();
    return { action, performedBy, dateTime: dt };
  }

  // Accordion controls
  private panel(row: Locator) {
    return row.locator("xpath=following-sibling::div[contains(@class,'accordion-collapse')]").first();
  }
  public async setExpanded(row: Locator, open: boolean) {
    const btn = row.locator("button.accordion-button.his-action");
    const panel = this.panel(row);
    await expect(btn).toBeVisible();
    const className = (await btn.getAttribute("class")) ?? "";
    const isOpen = !className.includes("collapsed");
    if (isOpen !== open) {
      await btn.click();
    }
    if (open) {
      await expect(btn).not.toHaveClass(/collapsed/);
      await expect(panel).toBeVisible();
    } else {
      await expect(btn).toHaveClass(/collapsed/);
      await expect(panel).toBeHidden();
    }
  }

  // Read changes
  private async readHistoryChanges(details: Locator): Promise<HistoryChanges<string>> {
    const rows = details.locator("div.d-flex.justify-content-around");
    const count = await rows.count();
    const previous: Record<string, string> = {};
    const updated: Record<string, string> = {};
    for (let i = 0; i < count; i++) {
      const cols = rows.nth(i).locator("span.his-col");
      if ((await cols.count()) < 3) continue;
      const field = await cols.nth(0).innerText();
      const prev = await cols.nth(1).innerText();
      const upd = await cols.nth(2).innerText();
      if (!field) continue;
      if (prev === "Previous" && upd === "Updated") continue;
      previous[field] = prev;
      updated[field] = upd;
    }
    return { previous, updated };
  }

  @logStep("GET ALL INFO FOR SPECIFIC ACTION")
  public async getHistoryChangesByDate(
    action: ORDER_HISTORY_ACTIONS,
    dateTime: string,
  ): Promise<HistoryChanges<string>> {
    const row = this.rowByActionAndDate(action, dateTime);
    await expect(row).toBeVisible();

    await this.setExpanded(row, true);

    const details = this.panel(row);
    await expect(details).toBeVisible();

    return this.readHistoryChanges(details);
  }

  @logStep("GET ALL INFO FOR DELIVERY ACTION")
  public async getDeliveryChangesByDate(
    action: DeliveryHistoryAction,
    dateTime: string,
  ): Promise<HistoryChanges<DeliveryHistoryField>> {
    const changes = await this.getHistoryChangesByDate(action, dateTime);
    return changes as HistoryChanges<DeliveryHistoryField>;
  }

  @logStep("GET STATUS FOR SPECIFIC ACTION")
  public async getStatusByDate(action: StatusHistoryAction, dateTime: string): Promise<OrderStatusChange> {
    const changes = await this.getHistoryChangesByDate(action, dateTime);
    return {
      previous: (changes.previous["Status"] ?? ORDER_STATUS.EMPTY) as ORDER_STATUS,
      updated: (changes.updated["Status"] ?? ORDER_STATUS.EMPTY) as ORDER_STATUS,
    };
  }

  @logStep("GET ALL INFO FOR MANAGER ACTION")
  public async getManagerChangesByDate(
    action: ManagerHistoryAction,
    dateTime: string,
  ): Promise<HistoryChanges<ManagerField>> {
    const changes = await this.getHistoryChangesByDate(action, dateTime);
    return changes as HistoryChanges<ManagerField>;
  }
}
