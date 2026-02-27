import { ICustomer } from "data/types/customer.types";
import { SalesPortalPage } from "../salesPortal.page";
import { logStep } from "utils/report/logStep.utils.js";

export class AddNewCustomerPage extends SalesPortalPage {
  readonly title = this.page.locator("h2.page-title-text");
  readonly email = this.page.locator("#inputEmail");
  readonly nameInput = this.page.locator("#inputName");
  readonly countrySelect = this.page.locator("#inputCountry");
  readonly cityInput = this.page.locator("#inputCity");
  readonly streetInput = this.page.locator("#inputStreet");
  readonly houseInput = this.page.locator("#inputHouse");
  readonly flatInput = this.page.locator("#inputFlat");
  readonly phoneInput = this.page.locator("#inputPhone");
  readonly notesInput = this.page.locator("#textareaNotes");
  readonly saveButton = this.page.locator("#save-new-customer");

  readonly uniqueElement = this.title;

  @logStep("FILL NEW CUSTOMER FORM")
  async fillForm(customerData: Partial<ICustomer>) {
    if (customerData.name) await this.nameInput.fill(customerData.name);
    if (customerData.email) await this.email.fill(customerData.email);
    if (customerData.country) await this.countrySelect.selectOption(customerData.country);
    if (customerData.city) await this.cityInput.fill(customerData.city);
    if (customerData.street) await this.streetInput.fill(customerData.street);
    if (customerData.house) await this.houseInput.fill(customerData.house.toString());
    if (customerData.flat) await this.flatInput.fill(customerData.flat.toString());
    if (customerData.phone) await this.phoneInput.fill(customerData.phone.toString());
    if (customerData.notes) await this.notesInput.fill(customerData.notes);
  }

  @logStep("SAVE NEW CUSTOMER")
  async clickSave() {
    await this.saveButton.click();
  }
}
