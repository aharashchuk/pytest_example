import { expect } from "@playwright/test";
import { logStep } from "utils/report/logStep.utils";
import { IOrderFromResponse, IOrderResponse } from "data/types/order.types";
import { apiConfig } from "config/apiConfig";
import { STATUS_CODES } from "data/statusCodes";
import { BaseModal } from "../base.modal";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { OrderDetailsRequestedProducts } from "./components/requested-products.component";

export class EditProductsModal extends BaseModal {
  readonly uniqueElement = this.page.locator("#edit-products-modal");
  readonly title = this.uniqueElement.getByText("Edit Products");
  readonly closeButton = this.uniqueElement.locator("button.btn-close");
  // Order Details page anchor (used to open modal with built-in waits)
  readonly orderStatusLabel = this.page.locator(
    "div:nth-child(1) > span.text-primary, div:nth-child(1) > span.text-danger",
  );

  readonly productsSection = this.uniqueElement.locator("#edit-products-section");
  readonly productRows = this.productsSection.locator("div[data-id]");
  readonly selectProductsDropdown = this.productsSection.locator(".form-select[name='Product']");
  readonly addProductButton = this.uniqueElement.locator("#add-product-btn");
  readonly cancelEditButton = this.uniqueElement.locator("#cancel-edit-products-modal-btn");
  readonly saveUpdateButton = this.uniqueElement.locator("#update-products-btn");
  readonly deleteProductButton = this.productsSection.locator('button.del-btn-modal[title="Delete"]');
  readonly totalPrice = this.uniqueElement.locator("#total-price-order-modal");

  @logStep("OPEN EDIT PRODUCTS MODAL FROM ORDER DETAILS")
  async openFromOrderDetails(
    requestedProducts: OrderDetailsRequestedProducts,
    expectedStatus: ORDER_STATUS = ORDER_STATUS.DRAFT,
  ) {
    await requestedProducts.expectLoaded();
    await expect(this.orderStatusLabel).toHaveText(expectedStatus);
    await expect(requestedProducts.editButton).toBeVisible();
    await requestedProducts.clickEdit();
    await this.waitForOpened();
  }

  @logStep("GET PRODUCTS COUNT IN EDIT PRODUCTS MODAL")
  async getProductsCount(): Promise<number> {
    return this.productRows.count();
  }

  @logStep("SELECT PRODUCT IN EDIT PRODUCTS MODAL")
  async selectProduct(index: number, productName: string) {
    const dropdown = this.selectProductsDropdown.nth(index);
    await expect(dropdown).toBeVisible();
    await dropdown.selectOption(productName);
  }

  @logStep("CLICK ADD PRODUCT BUTTON IN EDIT PRODUCTS MODAL")
  async clickAddProductButton() {
    await expect(this.addProductButton).toBeVisible();
    await this.addProductButton.click();
  }

  @logStep("DELETE PRODUCT IN EDIT PRODUCTS MODAL")
  async deleteProduct(index: number) {
    const deleteButton = this.productsSection
      .locator("div[data-id]")
      .nth(index)
      .locator('button.del-btn-modal[title="Delete"]');
    await deleteButton.click();
  }

  @logStep("CLICK SAVE BUTTON IN EDIT PRODUCTS MODAL")
  async clickSave() {
    await this.saveUpdateButton.click();
  }

  @logStep("EDIT PRODUCTS IN EDIT PRODUCTS MODAL")
  async editOrder(products: string[]): Promise<IOrderFromResponse> {
    await this.waitForOpened();
    expect(products.length).toBeGreaterThanOrEqual(1);
    expect(products.length).toBeLessThanOrEqual(5);

    const targetCount = products.length;
    const currentRowsCount = await this.getProductsCount();

    // Remove extra rows if modal currently has more
    if (currentRowsCount > targetCount) {
      for (let i = currentRowsCount - 1; i >= targetCount; i--) {
        await this.deleteProduct(i);
      }
    }

    // Add missing rows if modal currently has fewer
    for (let i = 0; i < targetCount; i++) {
      if (i >= currentRowsCount) {
        await this.clickAddProductButton();
      }
      // Select products for each row (replacement-safe)
      await this.selectProduct(i, products[i]!);
    }

    const response = await this.interceptResponse<IOrderResponse, unknown[]>(
      apiConfig.endpoints.orders,
      this.clickSave.bind(this),
    );
    expect(response.status).toBe(STATUS_CODES.OK);

    return response.body.Order;
  }

  @logStep("CLICK CANCEL BUTTON IN EDIT PRODUCTS MODAL")
  async clickCancel() {
    await this.cancelEditButton.click();
  }

  @logStep("CLICK CLOSE BUTTON IN EDIT PRODUCTS MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  @logStep("GET PRODUCTS DROPDOWN VALUES IN EDIT PRODUCTS MODAL")
  async getProductsDropdownTexts(): Promise<string[]> {
    const productsOptions = this.selectProductsDropdown.locator("option");
    return productsOptions.allTextContents();
  }

  @logStep("GET TOTAL PRICE IN EDIT PRODUCTS MODAL")
  async getTotalPrice() {
    const price = (await this.totalPrice.textContent()) || "";
    return price.replace("$", "");
  }
}
