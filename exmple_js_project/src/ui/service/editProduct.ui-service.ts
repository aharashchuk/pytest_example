import { expect, Page } from "@playwright/test";
import { generateProductData } from "data/salesPortal/products/generateProductData";
import { STATUS_CODES } from "data/statusCodes";
import { IProductResponse } from "data/types/product.types";
import { EditProductPage, ProductsListPage } from "ui/pages/products";
import { apiConfig } from "config/apiConfig";
import _ from "lodash";
import { logStep } from "utils/report/logStep.utils.js";

export class EditProductUIService {
  editProductPage: EditProductPage;
  productsListPage: ProductsListPage;

  constructor(private page: Page) {
    this.editProductPage = new EditProductPage(page);
    this.productsListPage = new ProductsListPage(page);
  }

  @logStep("OPEN EDIT PRODUCT PAGE")
  async open(id: string) {
    await this.editProductPage.open(`products/${id}/edit`);
    await this.editProductPage.waitForOpened();
  }

  @logStep("EDIT PRODUCT")
  async edit(id: string) {
    const data = generateProductData();
    await this.editProductPage.fillForm(data);
    const response = await this.editProductPage.interceptResponse<IProductResponse, unknown[]>(
      apiConfig.endpoints.productById(id),
      this.editProductPage.clickSave.bind(this.editProductPage),
    );
    expect(response.status).toBe(STATUS_CODES.OK);
    expect(_.omit(response.body.Product, "_id", "createdOn")).toEqual(data);

    await this.productsListPage.waitForOpened();
    return response.body.Product;
  }
}
