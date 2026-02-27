import { logStep } from "utils/report/logStep.utils.js";
import { BasePage } from "../../base.page";
import { Country, ICustomerDetails } from "data/types/customer.types";
import { EditOrderCustomerModal } from "./editCustomer.modal";
import { Page } from "@playwright/test";

/**
 * Customer Details section of Order Details page.
 */
export class OrderDetailsCustomerDetails extends BasePage {
  readonly uniqueElement = this.page.locator("#customer-section");
  readonly editButton = this.page.locator("#edit-customer-pencil");
  readonly details = this.uniqueElement.locator("div.c-details > span:nth-child(2)");
  readonly editOrderCustomerModal: EditOrderCustomerModal;

  constructor(page: Page) {
    super(page);
    this.editOrderCustomerModal = new EditOrderCustomerModal(page);
  }

  @logStep("CUSTOMER: CLICK EDIT")
  async clickEdit() {
    await this.editButton.click();
    return this.editOrderCustomerModal;
  }

  @logStep("CUSTOMER: GET DATA")
  async getCustomerData(): Promise<ICustomerDetails> {
    const [email, name, country, city, street, house, flat, phone, createdOn, notes] =
      await this.details.allInnerTexts();
    return {
      email: email!,
      name: name!,
      country: country! as Country,
      city: city!,
      street: street!,
      house: +house!,
      flat: +flat!,
      phone: phone!,
      createdOn: createdOn!,
      notes: notes!,
    };
  }

  async isVisible() {
    return this.uniqueElement.isVisible();
  }
  async isEditVisible() {
    return this.editButton.isVisible();
  }
}
