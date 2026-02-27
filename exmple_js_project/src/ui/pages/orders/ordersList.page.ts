import { SalesPortalPage } from "../salesPortal.page";
import { logStep } from "utils/report/logStep.utils.js";
import { IOrderInTable, OrdersTableHeader } from "data/types/order.types";
import { CreateOrderModal } from "./createOrderModal.page";
import { ExportModal, ordersFieldNamesMapper } from "../export.modal";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { NavBar } from "../navbar.component";

export class OrdersListPage extends SalesPortalPage {
  private readonly headerText = (name: OrdersTableHeader): string => {
    const map: Record<OrdersTableHeader, string> = {
      _id: "Order Number",
      email: "Email",
      price: "Price",
      delivery: "Delivery",
      status: "Status",
      assignedManager: "Assigned Manager",
      createdOn: "Created On",
    };
    return map[name];
  };

  readonly createOrderModal = new CreateOrderModal(this.page);
  readonly navBar = new NavBar(this.page);
  readonly exportModal = new ExportModal(this.page, ordersFieldNamesMapper);
  readonly title = this.page.locator("h2.fw-bold");
  readonly createOrderButton = this.page.locator('[name="add-button"]');
  readonly tableRow = this.page.locator("tbody tr");
  readonly tableRowByName = (orderNumber: string) =>
    this.page.locator("table tbody tr", { has: this.page.locator("td", { hasText: orderNumber }) });
  readonly tableRowByIndex = (index: number) => this.page.locator("table tbody tr").nth(index);
  readonly orderNumberCell = (orderNumber: string) => this.tableRowByName(orderNumber).locator("td").nth(0);
  readonly emailCell = (orderNumber: string) => this.tableRowByName(orderNumber).locator("td").nth(1);
  readonly priceCell = (orderNumber: string) => this.tableRowByName(orderNumber).locator("td").nth(2);
  readonly deliveryCell = (orderNumber: string) => this.tableRowByName(orderNumber).locator("td").nth(2);
  readonly statusCell = (orderNumber: string) => this.tableRowByName(orderNumber).locator("td").nth(2);
  readonly assignedManagerCell = (orderNumber: string) => this.tableRowByName(orderNumber).locator("td").nth(2);
  readonly createdOnCell = (nameOrIndex: string | number) =>
    typeof nameOrIndex === "string"
      ? this.tableRowByName(nameOrIndex).locator("td").nth(3)
      : this.tableRowByIndex(nameOrIndex).locator("td").nth(3);
  readonly tableHeader = this.page.locator('thead th div[onclick*="sortOrdersInTable"]');
  readonly tableHeaderNamed = (name: OrdersTableHeader) => this.tableHeader.filter({ hasText: this.headerText(name) });
  readonly tableHeaderArrow = (name: OrdersTableHeader, { direction }: { direction: "asc" | "desc" }) =>
    this.page
      .locator("thead th", { has: this.page.locator("div", { hasText: this.headerText(name) }) })
      .locator(`i.${direction === "asc" ? "bi-arrow-down" : "bi-arrow-up"}`);

  readonly detailsButton = (orderNumber: string) =>
    this.tableRowByName(orderNumber).getByTitle("Details", { exact: true });
  readonly reopenButton = (orderNumber: string) => this.tableRowByName(orderNumber).getByTitle("Reopen");
  readonly uniqueElement = this.createOrderButton;
  readonly searchInput = this.page.locator("#search");
  readonly searchButton = this.page.locator("#search-orders");
  readonly exportButton = this.page.locator("#export");

  @logStep("CLICK ADD NEW ORDER BUTTON")
  async clickCreateOrderButton() {
    await this.createOrderButton.click();
    return this.createOrderModal;
  }

  @logStep("GET ORDER'S DATA BY ORDER NUMBER")
  async getOrderData(orderNumber: string): Promise<IOrderInTable> {
    const [orderId, email, price, delivery, status, assignedManager, createdOn] = await this.tableRowByName(orderNumber)
      .locator("td")
      .allInnerTexts();
    return {
      orderId: orderId!,
      email: email!,
      price: +price!.replace("$", ""),
      delivery: delivery!,
      status: status! as ORDER_STATUS,
      assignedManager: assignedManager!,
      createdOn: createdOn!,
    };
  }

  @logStep("GET ALL ORDERS' DATA IN TABLE")
  async getTableData(): Promise<IOrderInTable[]> {
    const data: IOrderInTable[] = [];

    const rows = await this.tableRow.all();
    for (const row of rows) {
      const [orderId, email, price, delivery, status, assignedManager, createdOn] = await row
        .locator("td")
        .allInnerTexts();
      data.push({
        orderId: orderId!,
        email: email!,
        price: +price!.replace("$", ""),
        delivery: delivery!,
        status: status! as ORDER_STATUS,
        assignedManager: assignedManager!,
        createdOn: createdOn!,
      });
    }
    return data;
  }

  @logStep("CLICK ACTION BUTTON ON ORDERS LIST PAGE")
  async clickAction(orderNumber: string, button: "details" | "reopen") {
    if (button === "details") await this.detailsButton(orderNumber).click();
    if (button === "reopen") await this.reopenButton(orderNumber).click();
  }

  @logStep("CLICK TABLE HEADER ON ORDERS LIST PAGE")
  async clickTableHeader(name: OrdersTableHeader) {
    await this.tableHeaderNamed(name).click();
  }

  @logStep("FILL SEARCH INPUT ON ORDERS LIST PAGE")
  async fillSearchInput(text: string) {
    await this.searchInput.fill(text);
  }

  @logStep("CLICK SEARCH BUTTON ON ORDERS LIST PAGE")
  async clickSearch() {
    await this.searchButton.click();
  }

  @logStep("OPEN EXPORT MODAL ON ORDERS LIST PAGE")
  async openExportModal() {
    await this.exportButton.click();
    await this.exportModal.waitForOpened();
  }

  @logStep("SORT ORDERS TABLE")
  async sortBy(header: OrdersTableHeader, direction: "asc" | "desc") {
    const arrow = this.tableHeaderArrow(header, { direction });
    do {
      await this.clickTableHeader(header);
      await this.waitForSpinners();
    } while (!(await arrow.isVisible()));
  }

  @logStep("GET ORDERS TABLE AS RECORDS")
  async getTableAsRecords(): Promise<Array<Record<string, string>>> {
    const headerCells = await this.page.locator("table thead th").all();
    const headers = await Promise.all(headerCells.map(async (cell) => (await cell.innerText()).trim()));

    const rows = await this.page.locator("table tbody tr").all();
    const data: Array<Record<string, string>> = [];

    for (const row of rows) {
      const values = await row.locator("td").allInnerTexts();
      const record: Record<string, string> = {};

      for (let i = 0; i < Math.min(headers.length, values.length); i++) {
        const header = headers[i];
        if (!header) continue;
        record[header] = values[i]?.trim() ?? "";
      }

      data.push(record);
    }

    return data;
  }
}
