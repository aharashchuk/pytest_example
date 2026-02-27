import { expect, Page } from "@playwright/test";
import { apiConfig } from "config/apiConfig";
import { generateProductData } from "data/salesPortal/products/generateProductData";
import { STATUS_CODES } from "data/statusCodes";
import { IProduct, IProductResponse } from "data/types/product.types";
import { AddNewProductPage, ProductsListPage } from "ui/pages/products";
import _ from "lodash";
import { logStep } from "utils/report/logStep.utils.js";

export class AddNewProductUIService {
  addNewProductPage: AddNewProductPage;
  productsListPage: ProductsListPage;

  constructor(private page: Page) {
    this.addNewProductPage = new AddNewProductPage(page);
    this.productsListPage = new ProductsListPage(page);
  }

  @logStep("OPEN ADD NEW PRODUCT PAGE")
  async open() {
    await this.addNewProductPage.open("products/add");
    await this.addNewProductPage.waitForOpened();
  }

  @logStep("CREATE NEW PRODUCT")
  async create(productData?: Partial<IProduct>) {
    const data = generateProductData(productData);
    await this.addNewProductPage.fillForm(data);
    const response = await this.addNewProductPage.interceptResponse<IProductResponse, unknown[]>(
      apiConfig.endpoints.products,
      this.addNewProductPage.clickSave.bind(this.addNewProductPage),
    );
    expect(response.status).toBe(STATUS_CODES.CREATED);
    expect(_.omit(response.body.Product, "_id", "createdOn")).toEqual(data);

    await this.productsListPage.waitForOpened();
    return response.body.Product;
  }
}
