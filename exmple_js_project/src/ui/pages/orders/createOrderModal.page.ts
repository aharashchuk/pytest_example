import { expect } from "@playwright/test";
import { logStep } from "utils/report/logStep.utils";
import { IOrderFromResponse, IOrderResponse } from "data/types/order.types";
import { apiConfig } from "config/apiConfig";
import { STATUS_CODES } from "data/statusCodes";
import { BaseModal } from "../base.modal";

export class CreateOrderModal extends BaseModal {
  readonly uniqueElement = this.page.locator("#add-order-modal");
  readonly title = this.uniqueElement.getByText("Create Order");
  readonly closeButton = this.uniqueElement.locator("button.btn-close");
  readonly selectCustomersDropdown = this.uniqueElement.locator("#inputCustomerOrder");
  readonly productsSection = this.uniqueElement.locator("#products-section");
  readonly selectProductsDropdown = this.productsSection.locator(".form-select[name='Product']");
  readonly addProductButton = this.uniqueElement.locator("#add-product-btn");
  readonly createButton = this.uniqueElement.locator("#create-order-btn");
  readonly cancelButton = this.uniqueElement.locator("#cancel-order-modal-btn");
  readonly totalPrice = this.uniqueElement.locator("#total-price-order-modal");

  @logStep("SELECT CUSTOMER IN CREATE ORDER MODAL")
  async selectCustomer(customerName: string) {
    await this.selectCustomersDropdown.selectOption(customerName);
  }

  @logStep("SELECT PRODUCT IN CREATE ORDER MODAL")
  async selectProduct(index: number, productName: string) {
    const dropdown = this.selectProductsDropdown.nth(index);
    await expect(dropdown).toBeVisible();
    await dropdown.selectOption(productName);
  }

  @logStep("CLICK ADD PRODUCT BUTTON IN CREATE ORDER MODAL")
  async clickAddProductButton() {
    await expect(this.addProductButton).toBeVisible();
    await this.addProductButton.click();
  }

  @logStep("DELETE PRODUCT IN CREATE ORDER MODAL")
  async deleteProduct(index: number) {
    const deleteButton = this.productsSection
      .locator("div[data-id]")
      .nth(index)
      .locator('button.del-btn-modal[title="Delete"]');
    await deleteButton.click();
  }

  @logStep("GET TOTAL PRICE IN CREATE ORDER MODAL")
  async getTotalPrice() {
    const price = (await this.totalPrice.textContent()) || "";
    return price.replace("$", "");
  }

  @logStep("CLICK CREATE BUTTON IN CREATE ORDER MODAL")
  async clickCreate() {
    await this.createButton.click();
  }

  @logStep("CREATE ORDER IN CREATE ORDER MODAL")
  async createOrder(customerName: string, products: string[]): Promise<IOrderFromResponse> {
    await this.waitForOpened();
    expect(products.length).toBeGreaterThanOrEqual(1);
    expect(products.length).toBeLessThanOrEqual(5);
    await this.selectCustomer(customerName);
    await this.selectProduct(0, products[0]!);
    for (let i = 1; i < products.length; i++) {
      await this.clickAddProductButton();
      await this.selectProduct(i, products[i]!);
    }
    const response = await this.interceptResponse<IOrderResponse, unknown[]>(
      apiConfig.endpoints.orders,
      this.clickCreate.bind(this),
    );
    expect(response.status).toBe(STATUS_CODES.CREATED);

    return response.body.Order;
  }

  @logStep("CLICK CANCEL BUTTON IN CREATE ORDER MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("CLICK CLOSE BUTTON IN CREATE ORDER MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  @logStep("GET CUSTOMERS DROPDOWN VALUES IN CREATE ORDER MODAL")
  async getCustomersDropdownTexts(): Promise<string[]> {
    const customersOptions = this.selectCustomersDropdown.locator("option");
    return customersOptions.allTextContents();
  }

  @logStep("GET PRODUCTS DROPDOWN VALUES IN CREATE ORDER MODAL")
  async getProductsDropdownTexts(): Promise<string[]> {
    const productsOptions = this.selectProductsDropdown.locator("option");
    return productsOptions.allTextContents();
  }
}
