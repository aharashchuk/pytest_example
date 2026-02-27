import { IProductInTable, ProductsTableHeader } from "data/types/product.types";
import { SalesPortalPage } from "../salesPortal.page";
import { MANUFACTURERS } from "data/salesPortal/products/manufacturers";
import { ProductDetailsModal } from "./details.modal";
import { ConfirmationModal } from "../confirmation.modal";
import { logStep } from "utils/report/logStep.utils.js";
import { ExportModal, productsFieldNamesMapper } from "../export.modal";
import { NavBar } from "../navbar.component";

export class ProductsListPage extends SalesPortalPage {
  readonly detailsModal = new ProductDetailsModal(this.page);
  readonly deleteModal = new ConfirmationModal(this.page);
  readonly exportModal = new ExportModal(this.page, productsFieldNamesMapper);
  readonly navBar = new NavBar(this.page);
  readonly productsPageTitle = this.page.locator("h2.fw-bold");
  readonly addNewProductButton = this.page.locator('[name="add-button"]');
  readonly tableRow = this.page.locator("tbody tr");
  readonly tableRowByName = (productName: string) =>
    this.page.locator("table tbody tr", { has: this.page.locator("td", { hasText: productName }) });
  readonly tableRowByIndex = (index: number) => this.page.locator("table tbody tr").nth(index);
  readonly nameCell = (productName: string) => this.tableRowByName(productName).locator("td").nth(0);
  readonly priceCell = (productName: string) => this.tableRowByName(productName).locator("td").nth(1);
  readonly manufacturerCell = (productName: string) => this.tableRowByName(productName).locator("td").nth(2);
  readonly createdOnCell = (nameOrIndex: string | number) =>
    typeof nameOrIndex === "string"
      ? this.tableRowByName(nameOrIndex).locator("td").nth(3)
      : this.tableRowByIndex(nameOrIndex).locator("td").nth(3);
  readonly tableHeader = this.page.locator("thead th div[current]");
  readonly tableHeaderNamed = (name: ProductsTableHeader) => this.tableHeader.filter({ hasText: name });

  readonly tableHeaderArrow = (name: ProductsTableHeader, { direction }: { direction: "asc" | "desc" }) =>
    this.page
      .locator("thead th", { has: this.page.locator("div[current]", { hasText: name }) })
      .locator(`i.${direction === "asc" ? "bi-arrow-down" : "bi-arrow-up"}`);

  readonly editButton = (productName: string) => this.tableRowByName(productName).getByTitle("Edit");
  readonly detailsButton = (productName: string) => this.tableRowByName(productName).getByTitle("Details");
  readonly deleteButton = (productName: string) => this.tableRowByName(productName).getByTitle("Delete");

  readonly searchInput = this.page.locator("#search");
  readonly searchButton = this.page.locator("#search-products");

  readonly uniqueElement = this.addNewProductButton;

  @logStep("CLICK ADD NEW PRODUCT")
  async clickAddNewProduct() {
    await this.addNewProductButton.click();
  }

  @logStep("GET PRODUCT DATA")
  async getProductData(productName: string): Promise<IProductInTable> {
    const [name, price, manufacturer, createdOn] = await this.tableRowByName(productName).locator("td").allInnerTexts();
    return {
      name: name!,
      price: +price!.replace("$", ""),
      manufacturer: manufacturer! as MANUFACTURERS,
      createdOn: createdOn!,
    };
  }

  @logStep("GET PRODUCTS DATA IN TABLE")
  async getTableData(): Promise<IProductInTable[]> {
    const data: IProductInTable[] = [];

    const rows = await this.tableRow.all();
    for (const row of rows) {
      const [name, price, manufacturer, createdOn] = await row.locator("td").allInnerTexts();
      data.push({
        name: name!,
        price: +price!.replace("$", ""),
        manufacturer: manufacturer! as MANUFACTURERS,
        createdOn: createdOn!,
      });
    }
    return data;
  }

  @logStep("CLICK ACTION BUTTON ON PRODUCTS LIST PAGE")
  async clickAction(productName: string, button: "edit" | "delete" | "details") {
    if (button === "edit") await this.editButton(productName).click();
    if (button === "delete") await this.deleteButton(productName).click();
    if (button === "details") await this.detailsButton(productName).click();
  }

  @logStep("CLICK TABLE HEADER ON PRODUCTS LIST PAGE")
  async clickTableHeader(name: ProductsTableHeader) {
    await this.tableHeaderNamed(name).click();
  }

  @logStep("FILL SEARCH INPUT ON PRODUCTS LIST PAGE")
  async fillSearchInput(text: string) {
    await this.searchInput.fill(text);
  }

  @logStep("CLICK SEARCH BUTTON ON PRODUCTS LIST PAGE")
  async clickSearch() {
    await this.searchButton.click();
  }

  @logStep("OPEN EXPORT MODAL ON PRODUCTS LIST PAGE")
  async openExportModal() {
    const exportButton = this.page.locator('button[name="export-button"]');
    await exportButton.click();
    await this.exportModal.checkFieldsBulk(["Name", "Price", "Manufacturer", "Amount", "Created On", "Notes"]);
  }
}
