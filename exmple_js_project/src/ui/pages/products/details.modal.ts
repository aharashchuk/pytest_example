import { IProductDetails } from "data/types/product.types";
import { SalesPortalPage } from "../salesPortal.page";
import { MANUFACTURERS } from "data/salesPortal/products/manufacturers";
import { logStep } from "utils/report/logStep.utils.js";

export class ProductDetailsModal extends SalesPortalPage {
  readonly uniqueElement = this.page.locator("#ProductDetailsModal");

  readonly title = this.uniqueElement.locator("h5");
  readonly closeButton = this.uniqueElement.locator("button.btn-close");
  readonly editButton = this.uniqueElement.locator("button.btn-primary");
  readonly cancelButton = this.uniqueElement.locator("button.btn-secondary");

  readonly productValue = this.uniqueElement.locator("p");

  @logStep("CLICK CLOSE BUTTON ON PRODUCT DETAILS MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  @logStep("CLICK CANCEL BUTTON ON PRODUCT DETAILS MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("CLICK EDIT BUTTON ON PRODUCT DETAILS MODAL")
  async clickEdit() {
    await this.editButton.click();
  }

  @logStep("GET PRODUCT DETAILS ON PRODUCT DETAILS MODAL")
  async getData(): Promise<IProductDetails> {
    const [name, amount, price, manufacturer, createdOn, notes] = await this.productValue.allInnerTexts();

    return {
      name: name!,
      amount: +amount!,
      price: +price!,
      manufacturer: manufacturer! as MANUFACTURERS,
      createdOn: createdOn!,
      notes: notes === "-" ? "" : notes!,
    };
  }
}
