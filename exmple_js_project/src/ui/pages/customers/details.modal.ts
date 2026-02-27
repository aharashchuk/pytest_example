import { ICustomerDetails } from "data/types/customer.types";
import { SalesPortalPage } from "../salesPortal.page";
import { COUNTRY } from "data/salesPortal/country";
import { logStep } from "utils/report/logStep.utils.js";

export class CustomerDetailsModal extends SalesPortalPage {
  readonly uniqueElement = this.page.locator("#CustomerDetailsModal");

  readonly title = this.uniqueElement.locator("h5");
  readonly closeButton = this.uniqueElement.locator("button.btn-close");
  readonly editButton = this.uniqueElement.locator("button.btn-primary");
  readonly cancelButton = this.uniqueElement.locator("button.btn-secondary");

  readonly productValue = this.uniqueElement.locator("p");

  @logStep("CLOSE CUSTOMER DETAILS MODAL")
  async clickClose() {
    await this.closeButton.click();
  }

  @logStep("CANCEL CUSTOMER DETAILS MODAL")
  async clickCancel() {
    await this.cancelButton.click();
  }

  @logStep("EDIT CUSTOMER DETAILS MODAL")
  async clickEdit() {
    await this.editButton.click();
  }

  @logStep("GET CUSTOMER DETAILS")
  async getData(): Promise<ICustomerDetails> {
    const [email, name, country, city, street, house, flat, phone, createdOn, notes] =
      await this.productValue.allInnerTexts();

    return {
      email: email!,
      name: name!,
      country: country! as COUNTRY,
      city: city!,
      street: street!,
      house: +house!,
      flat: +flat!,
      phone: phone!,
      createdOn: createdOn!,
      notes: notes === "-" ? "" : notes!,
    };
  }
}
