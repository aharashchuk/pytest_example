import { expect, Page } from "@playwright/test";
import { apiConfig } from "config/apiConfig";
import { generateCustomerData } from "data/salesPortal/customers/generateCustomerData";
import { STATUS_CODES } from "data/statusCodes";
import { ICustomer, ICustomerResponse } from "data/types/customer.types";
import { AddNewCustomerPage, CustomersListPage } from "ui/pages/customers";
import _ from "lodash";
import { logStep } from "utils/report/logStep.utils.js";

export class AddNewCustomerUIService {
  addNewCustomerPage: AddNewCustomerPage;
  customersListPage: CustomersListPage;

  constructor(private page: Page) {
    this.addNewCustomerPage = new AddNewCustomerPage(page);
    this.customersListPage = new CustomersListPage(page);
  }

  @logStep("OPEN ADD NEW CUSTOMER PAGE")
  async open() {
    await this.addNewCustomerPage.open("customers/add");
    await this.addNewCustomerPage.waitForOpened();
  }

  @logStep("CREATE NEW CUSTOMER")
  async create(customerData?: Partial<ICustomer>) {
    const data = generateCustomerData(customerData);
    await this.addNewCustomerPage.fillForm(data);
    const response = await this.addNewCustomerPage.interceptResponse<ICustomerResponse, unknown[]>(
      apiConfig.endpoints.customers,
      this.addNewCustomerPage.clickSave.bind(this.addNewCustomerPage),
    );
    expect(response.status).toBe(STATUS_CODES.CREATED);
    expect(_.omit(response.body.Customer, "_id", "createdOn")).toEqual(data);

    await this.customersListPage.waitForOpened();
    return response.body.Customer;
  }
}
