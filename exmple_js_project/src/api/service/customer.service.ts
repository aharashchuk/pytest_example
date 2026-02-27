import { CustomersApi } from "api/api/customers.api";
import { generateCustomerData } from "data/salesPortal/customers/generateCustomerData";
import { getListCustomersSchema } from "data/schemas/customers/getList.schema";
import { STATUS_CODES } from "data/statusCodes";
import {
  ICustomer,
  ICustomerFromResponse,
  ICustomerListResponse,
  IGetCustomersParams,
} from "data/types/customer.types";
import { validateResponse } from "utils/validation/validateResponse.utils";
import { logStep } from "utils/report/logStep.utils.js";

export class CustomersApiService {
  constructor(private customerApi: CustomersApi) {}

  @logStep("CREATE CUSTOMER - API")
  async create(token: string, customerData?: ICustomer) {
    const data = generateCustomerData(customerData);
    const response = await this.customerApi.create(token, data);
    validateResponse(response, {
      status: STATUS_CODES.CREATED,
      IsSuccess: true,
      ErrorMessage: null,
    });

    return response.body.Customer;
  }

  @logStep("DELETE CUSTOMER - API")
  async delete(token: string, id: string) {
    const response = await this.customerApi.delete(token, id);
    validateResponse(response, {
      status: STATUS_CODES.DELETED,
    });
  }

  @logStep("GET CUSTOMER BY ID - API")
  async getById(token: string, id: string): Promise<ICustomerFromResponse> {
    const response = await this.customerApi.getById(token, id);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });

    return response.body.Customer;
  }

  @logStep("GET ALL CUSTOMERS - API")
  async getAll(token: string): Promise<ICustomerFromResponse[]> {
    const response = await this.customerApi.getAll(token);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });

    return response.body.Customers;
  }

  @logStep("GET LIST OF CUSTOMERS - API")
  async getList(token: string, params: IGetCustomersParams): Promise<ICustomerListResponse> {
    const response = await this.customerApi.getList(token, params);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
      schema: getListCustomersSchema,
    });

    return response.body;
  }

  @logStep("UPDATE CUSTOMER - API")
  async update(token: string, id: string, customerData: Partial<ICustomer>): Promise<ICustomerFromResponse> {
    const response = await this.customerApi.update(token, id, customerData);
    validateResponse(response, {
      status: STATUS_CODES.OK,
      IsSuccess: true,
      ErrorMessage: null,
    });

    return response.body.Customer;
  }
}
