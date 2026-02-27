import { IApiClient } from "api/apiClients/types";
import { apiConfig } from "config/apiConfig";
import { IRequestOptions, IResponseFields } from "data/types/core.types";
import {
  ICustomer,
  ICustomerResponse,
  ICustomerListResponse,
  ICustomersResponse,
  IGetCustomersParams,
} from "data/types/customer.types";
import { convertRequestParams } from "utils/queryParams.utils";
import { logStep } from "utils/report/logStep.utils";

export class CustomersApi {
  constructor(private apiClient: IApiClient) {}

  @logStep("CREATE /api/customers")
  async create(token: string, customer: ICustomer) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.customers,
      method: "post",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      data: customer,
    };
    return await this.apiClient.send<ICustomerResponse>(options);
  }

  @logStep("DELETE /api/customers/{id}")
  async delete(token: string, _id: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.customerById(_id),
      method: "delete",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<IResponseFields>(options);
  }

  @logStep("GET /api/customers")
  async getList(token: string, params: Partial<IGetCustomersParams>) {
    const query = convertRequestParams(params);
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: `${apiConfig.endpoints.customers}${query}`,
      method: "get",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<ICustomerListResponse>(options);
  }

  @logStep("GET /api/customers/all")
  async getAll(token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.customersAll,
      method: "get",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<ICustomersResponse>(options);
  }

  @logStep("GET /api/customers/{id}")
  async getById(token: string, _id: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.customerById(_id),
      method: "get",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<ICustomerResponse>(options);
  }

  @logStep("UPDATE /api/customers/{id}")
  async update(token: string, _id: string, customer: Partial<ICustomer>) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.customerById(_id),
      method: "put",
      headers: {
        "content-type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${token}`,
      },
      data: customer,
    };
    return await this.apiClient.send<ICustomerResponse>(options);
  }
}
