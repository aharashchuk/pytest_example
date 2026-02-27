import { SalesPortalPage } from "./salesPortal.page";
import { logStep } from "utils/report/logStep.utils";

export class NavBar extends SalesPortalPage {
  readonly navbarContainer = this.page.locator(".navbar");
  readonly uniqueElement = this.navbarContainer;
  readonly homeButton = this.navbarContainer.locator("[name='home']");
  readonly productsButton = this.navbarContainer.locator("[name='products']");
  readonly customersButton = this.navbarContainer.locator("[name='customers']");
  readonly ordersButton = this.navbarContainer.locator("[name='orders']");

  @logStep("NAVBAR: CLICK ON NAVIGATION BUTTON")
  async clickOnNavButton(buttonName: "Home" | "Products" | "Customers" | "Orders") {
    if (buttonName === "Home") {
      await this.homeButton.click();
    }
    if (buttonName === "Products") {
      await this.productsButton.click();
    }
    if (buttonName === "Customers") {
      await this.customersButton.click();
    }
    if (buttonName === "Orders") {
      await this.ordersButton.click();
    }
  }
}
