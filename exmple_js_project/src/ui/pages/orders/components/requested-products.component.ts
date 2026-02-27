import { expect, Locator, Page } from "@playwright/test";
import { logStep } from "utils/report/logStep.utils.js";
import { TIMEOUT_10_S, TIMEOUT_15_S } from "data/salesPortal/constants";
import { BasePage } from "../../base.page";

/**
 * Requested Products section of Order Details page, including receiving flow.
 */
export class OrderDetailsRequestedProducts extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  // Rely on frontend to render `#products-section`; `uniqueElement` is the component marker.
  readonly uniqueElement = this.page.locator("#products-section").first();

  readonly accordionRoot = this.page.locator("#products-accordion-section");

  readonly editButton = this.page.locator("#edit-products-pencil");

  // Receiving controls
  readonly startReceivingButton = this.uniqueElement.locator("#start-receiving-products, #start-receiving").first();
  // Be flexible across FE variants
  readonly saveReceivingButton = this.uniqueElement
    .locator("#save-received-products, #save-receiving, button#save-received-products")
    .first();
  readonly cancelReceivingButton = this.uniqueElement.locator("#cancel-receiving").first();
  readonly selectAllCheckbox = this.uniqueElement.locator("#selectAll");
  readonly productCheckboxes = this.page.locator('input[name="product"]');

  // Per-product helpers
  productItemByIndex(index: number) {
    return this.accordionRoot.locator(`#heading${index}`).first();
  }

  productCheckboxByIndex(index: number) {
    return this.page.locator(`#check${index}`);
  }

  productCheckboxById(productId: string) {
    return this.page.locator(`input[name="product"][value="${productId}"]`).first();
  }

  productItemByName(name: string) {
    // Product name itself is stable (not localized). Different UI modes render different wrappers,
    // so anchor on the product button text.
    return this.uniqueElement.locator("button", { hasText: name }).first();
  }

  receivedLabelWithin(item: Locator) {
    return item.locator(".received-label");
  }

  @logStep("PRODUCTS: CLICK EDIT")
  async clickEdit() {
    await this.editButton.click();
  }

  @logStep("PRODUCTS: START RECEIVING")
  async startReceiving() {
    await this.startReceivingButton.click();
  }

  @logStep("PRODUCTS: SAVE RECEIVING")
  async saveReceiving() {
    await expect(this.saveReceivingButton).toBeEnabled({ timeout: TIMEOUT_10_S });
    await this.saveReceivingButton.click();
  }

  @logStep("PRODUCTS: CANCEL RECEIVING")
  async cancelReceiving() {
    await this.cancelReceivingButton.click();
  }

  @logStep("PRODUCTS: SELECT ALL")
  async selectAll() {
    await this.selectAllCheckbox.click();
  }

  @logStep("PRODUCTS: TOGGLE PRODUCT BY INDEX")
  async toggleProductByIndex(index: number) {
    const cb = this.productCheckboxByIndex(index);
    await cb.click();
  }

  @logStep("PRODUCTS: TOGGLE PRODUCT BY ID")
  async toggleProductById(productId: string) {
    await this.productCheckboxById(productId).click();
  }

  @logStep("PRODUCTS: EXPECT LOADED")
  async expectLoaded() {
    await expect(this.uniqueElement).toBeVisible();
    // Not all UI states render the accordion (e.g. after fully received).
    if (await this.accordionRoot.first().isVisible()) {
      await expect(this.accordionRoot.first()).toBeVisible();
    }
  }

  @logStep("PRODUCTS: IS PRODUCT RECEIVED BY NAME")
  async isProductReceivedByName(name: string): Promise<boolean> {
    const item = this.productItemByName(name);
    await expect(item).toBeVisible();

    // In "Received" view-mode the UI usually shows a badge/label, not a checkbox.
    const row = item.locator("xpath=ancestor::*[self::div or self::li][1]");

    // In view-mode the UI shows a badge/label.
    const receivedLabel = row.locator(".received-label").first();
    if (await receivedLabel.isVisible()) return true;

    // In receiving-mode, the state is represented by a checkbox.
    const checkbox = row.locator('input[type="checkbox"]').first();
    if (await checkbox.isVisible()) return checkbox.isChecked();

    return false;
  }

  @logStep("PRODUCTS: IS PRODUCT RECEIVED (ID-FIRST)")
  async isProductReceived(productId: string, nameFallback?: string): Promise<boolean> {
    const checkbox = this.productCheckboxById(productId);
    if ((await checkbox.count()) > 0) {
      // Prefer structural UI signal over checkbox state (some FE modes render "Received" label
      // while checkbox can be absent/hidden/out-of-sync).
      const row = checkbox.locator("xpath=ancestor::*[self::div or self::li or self::tr][1]");
      const receivedLabel = row.locator(".received-label").first();
      if (await receivedLabel.isVisible()) return true;
      return checkbox.isChecked();
    }

    if (nameFallback) {
      return this.isProductReceivedByName(nameFallback);
    }

    return false;
  }

  async isEditVisible() {
    return this.editButton.isVisible();
  }
  async isStartReceivingVisible() {
    return this.startReceivingButton.isVisible();
  }
  async isSaveReceivingVisible() {
    return this.saveReceivingButton.isVisible();
  }
  async isCancelReceivingVisible() {
    return this.cancelReceivingButton.isVisible();
  }

  @logStep("PRODUCTS: WAIT FOR RECEIVING CONTROLS")
  async waitForReceivingControls(timeoutMs: number = TIMEOUT_15_S) {
    await expect(this.cancelReceivingButton).toBeVisible({ timeout: timeoutMs });
    await expect(this.saveReceivingButton).toBeVisible({ timeout: timeoutMs });
  }

  @logStep("PRODUCTS: WAIT FOR RECEIVING READY")
  async waitForStartReceiving(timeoutMs: number = TIMEOUT_15_S) {
    const startLocator = this.uniqueElement.locator("#start-receiving-products, #start-receiving").first();
    await startLocator.waitFor({ state: "visible", timeout: timeoutMs });
  }

  async waitForSaveCancel(timeoutMs: number = TIMEOUT_15_S) {
    const save = this.uniqueElement
      .locator("#save-received-products, #save-receiving, button#save-received-products")
      .first();
    const cancel = this.uniqueElement.locator("#cancel-receiving").first();
    await Promise.all([
      save.waitFor({ state: "visible", timeout: timeoutMs }),
      cancel.waitFor({ state: "visible", timeout: timeoutMs }),
    ]);
  }

  async waitForReceivingReady(timeoutMs: number = TIMEOUT_15_S) {
    const startPromise = this.uniqueElement
      .locator("#start-receiving-products, #start-receiving")
      .first()
      .waitFor({ state: "visible", timeout: timeoutMs });

    const save = this.uniqueElement
      .locator("#save-received-products, #save-receiving, button#save-received-products")
      .first();
    const cancel = this.uniqueElement.locator("#cancel-receiving").first();
    const saveCancelPromise = Promise.all([
      save.waitFor({ state: "visible", timeout: timeoutMs }),
      cancel.waitFor({ state: "visible", timeout: timeoutMs }),
    ]);

    try {
      // Resolve when either start becomes visible OR both save+cancel become visible
      // `Promise.any` returns on first fulfilled promise; if all reject, it throws.
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore - `Promise.any` is supported in runtime
      await Promise.any([startPromise, saveCancelPromise]);
    } catch {
      throw new Error("Receiving controls not ready within timeout");
    }
  }
}
