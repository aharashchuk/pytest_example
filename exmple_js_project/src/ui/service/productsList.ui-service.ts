import { expect, Page } from "@playwright/test";
import { IProductDetails } from "data/types/product.types";
import { AddNewProductPage } from "ui/pages/products/addNewProduct.page";
import { EditProductPage } from "ui/pages/products/editProduct.page";
import { ProductsListPage } from "ui/pages/products/productsList.page";
import { convertToFullDateAndTime } from "utils/date.utils";
import _ from "lodash";
import { logStep } from "utils/report/logStep.utils.js";

export class ProductsListUIService {
  productsListPage: ProductsListPage;
  addNewProductPage: AddNewProductPage;
  editProductPage: EditProductPage;

  constructor(private page: Page) {
    this.productsListPage = new ProductsListPage(page);
    this.addNewProductPage = new AddNewProductPage(page);
    this.editProductPage = new EditProductPage(page);
  }

  @logStep("OPEN ADD NEW PRODUCT PAGE")
  async openAddNewProductPage() {
    await this.productsListPage.clickAddNewProduct();
    await this.addNewProductPage.waitForOpened();
  }

  @logStep("OPEN PRODUCT DETAILS MODAL")
  async openDetailsModal(productName: string) {
    await this.productsListPage.detailsButton(productName).click();
    await this.productsListPage.detailsModal.waitForOpened();
  }

  @logStep("OPEN DELETE PRODUCT MODAL")
  async openDeleteModal(productName: string) {
    await this.productsListPage.clickAction(productName, "delete");
    await this.productsListPage.deleteModal.waitForOpened();
  }

  @logStep("DELETE PRODUCT")
  async deleteProduct(productName: string) {
    await this.productsListPage.clickAction(productName, "delete");
    await this.productsListPage.deleteModal.waitForOpened();
    await this.productsListPage.deleteModal.clickConfirm();
    await this.productsListPage.deleteModal.waitForClosed();
  }

  @logStep("EDIT PRODUCT")
  async editProduct(productName: string) {
    await this.productsListPage.clickAction(productName, "edit");
    await this.productsListPage.deleteModal.waitForOpened();
    await this.productsListPage.deleteModal.clickConfirm();
    await this.productsListPage.deleteModal.waitForClosed();
  }

  @logStep("SEARCH PRODUCT")
  async search(text: string) {
    await this.productsListPage.fillSearchInput(text);
    await this.productsListPage.clickSearch();
    await this.productsListPage.waitForOpened();
  }

  @logStep("OPEN PRODUCTS LIST PAGE")
  async open() {
    await this.productsListPage.open("products");
    await this.productsListPage.waitForOpened();
  }

  assertDetailsData(actual: IProductDetails, expected: IProductDetails) {
    expect(actual).toEqual({
      ..._.omit(expected, ["_id"]),
      createdOn: convertToFullDateAndTime(expected.createdOn),
    });
  }

  @logStep("CHECK PRODUCT EXISTS IN TABLE")
  async assertProductIsVisibleInTable(productName: string, isVisible = true) {
    await expect(this.productsListPage.tableRowByName(productName)).toBeVisible({ visible: isVisible });
  }
}
