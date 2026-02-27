import { Page } from "@playwright/test";
import { HomeModuleButton, HomePage } from "ui/pages/home.page";
import { ProductsListPage } from "ui/pages/products/productsList.page";
import { CustomersListPage } from "ui/pages/customers/customersList.page";
import { OrdersListPage } from "ui/pages/orders/ordersList.page";
import { logStep } from "utils/report/logStep.utils.js";

export class HomeUIService {
  homePage: HomePage;
  productsListPage: ProductsListPage;
  customersListPage: CustomersListPage;
  ordersListPage: OrdersListPage;

  constructor(private page: Page) {
    this.homePage = new HomePage(page);
    this.productsListPage = new ProductsListPage(page);
    this.customersListPage = new CustomersListPage(page);
    this.ordersListPage = new OrdersListPage(page);
  }

  public async open() {
    await this.homePage.open("#/home");
  }

  @logStep("OPEN ${moduleName} MODULE ON HOME PAGE")
  async openModule(moduleName: HomeModuleButton) {
    await this.homePage.clickOnViewModule(moduleName);

    if (moduleName === "Products") {
      await this.productsListPage.waitForOpened();
    }

    if (moduleName === "Customers") {
      await this.customersListPage.waitForOpened();
    }

    if (moduleName === "Orders") {
      await this.ordersListPage.waitForOpened();
    }
  }
}
