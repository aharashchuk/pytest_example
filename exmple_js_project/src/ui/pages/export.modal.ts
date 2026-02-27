import { expect, Page, type Download } from "@playwright/test";
import { logStep } from "utils/report/logStep.utils.js";
import { BaseModal } from "./base.modal";

export type ExportFormat = "CSV" | "JSON";

const exportFormatId: Record<ExportFormat, string> = {
  CSV: "exportCsv",
  JSON: "exportJson",
};

export const productsFieldNamesMapper = {
  "Select All": "selectAll",
  Name: "product_name",
  Price: "product_price",
  Manufacturer: "product_manufacturer",
  Amount: "product_amount",
  "Created On": "product_createdOn",
  Notes: "product_notes",
} as const;

export const customersFieldNamesMapper = {
  "Select All": "selectAll",
  Email: "customer_email",
  Name: "customer_name",
  Country: "customer_country",
  City: "customer_city",
  Street: "customer_street",
  House: "customer_house",
  Flat: "customer_flat",
  Phone: "customer_phone",
  "Created On": "customer_createdOn",
} as const;

export const ordersFieldNamesMapper = {
  "Select All": "selectAll",
  Status: "status",
  "Total Price": "total_price",
  Delivery: "delivery",
  Customer: "customer",
  Products: "products",
  "Assigned Manager": "assignedManager",
  "Created On": "createdOn",
} as const;

export type OrdersCheckboxes = keyof typeof ordersFieldNamesMapper;
export type ProductsCheckboxes = keyof typeof productsFieldNamesMapper;
export type CustomersCheckboxes = keyof typeof customersFieldNamesMapper;
export type ExportFieldMapper<T extends string> = Record<T, string>;

export class ExportModal<T extends string> extends BaseModal {
  constructor(
    page: Page,
    private fieldNamesMapper: ExportFieldMapper<T>,
  ) {
    super(page);
  }

  readonly uniqueElement = this.page.locator("#exportModal");
  readonly fieldsCheckboxesContainer = this.uniqueElement.locator("#fields-checkboxes");
  readonly selectAllCheckbox = this.uniqueElement.locator("#select-all-fields");
  readonly downloadButton = this.uniqueElement.locator("#export-button");
  readonly cancelButton = this.uniqueElement.locator("button.btn-secondary");
  readonly closeButton = this.uniqueElement.locator("button.btn-close");

  private readonly formatRadio = (format: ExportFormat) => this.uniqueElement.locator(`#${exportFormatId[format]}`);

  private readonly formatLabel = (format: ExportFormat) =>
    this.uniqueElement.locator(`label[for="${exportFormatId[format]}"]`);

  readonly fieldCheckbox = (name: T) =>
    this.fieldsCheckboxesContainer.locator(`input[value="${this.fieldNamesMapper[name]}"]`);

  private readonly allFields = (): T[] => Object.keys(this.fieldNamesMapper) as T[];

  @logStep("CHECK FIELD IN EXPORT MODAL")
  async checkField(name: T, options: { shouldBeChecked: boolean } = { shouldBeChecked: true }) {
    const checkbox = this.fieldCheckbox(name);
    options.shouldBeChecked ? await checkbox.check() : await checkbox.uncheck();
  }

  @logStep("CHECK FIELDS IN BULK IN EXPORT MODAL")
  async checkFieldsBulk(names: T[], options: { shouldBeChecked: boolean } = { shouldBeChecked: true }) {
    for (const name of names) {
      await this.checkField(name, options);
    }
  }

  @logStep("SELECT EXPORT FORMAT IN EXPORT MODAL")
  async selectFormat(format: ExportFormat) {
    const radio = this.formatRadio(format);
    if ((await radio.count()) > 0) {
      await radio.check();
      return;
    }

    const label = this.formatLabel(format);
    await label.click();
  }

  @logStep("CHECK ALL FIELDS IN EXPORT MODAL")
  async checkAllFields() {
    await this.selectAllCheckbox.check();
  }

  @logStep("UNCHECK ALL FIELDS IN EXPORT MODAL")
  async uncheckAllFields() {
    // Try select-all first if present.
    if ((await this.selectAllCheckbox.count()) > 0) {
      await this.selectAllCheckbox.uncheck();
    }

    // Fallback: ensure all individual checkboxes are unchecked.
    for (const name of this.allFields()) {
      if (name === ("Select All" as unknown as T)) continue;
      await this.checkField(name, { shouldBeChecked: false });
    }
  }

  @logStep("CLICK CANCEL BUTTON IN EXPORT MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("CLOSE EXPORT MODAL")
  async close() {
    await this.closeButton.click();
  }

  @logStep("CLICK DOWNLOAD BUTTON IN EXPORT MODAL")
  async clickDownload() {
    await expect(this.downloadButton).toBeVisible();
    await this.downloadButton.click();
  }

  @logStep("DOWNLOAD FILE IN EXPORT MODAL")
  async downloadFile(): Promise<Download> {
    await expect(this.downloadButton).toBeVisible();

    const [download] = await Promise.all([this.page.waitForEvent("download"), this.downloadButton.click()]);

    return download;
  }
}

export const createOrdersExportModal = (page: Page) => new ExportModal<OrdersCheckboxes>(page, ordersFieldNamesMapper);

export const createProductsExportModal = (page: Page) =>
  new ExportModal<ProductsCheckboxes>(page, productsFieldNamesMapper);

export const createCustomersExportModal = (page: Page) =>
  new ExportModal<CustomersCheckboxes>(page, customersFieldNamesMapper);
