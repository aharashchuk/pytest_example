import { Page } from "@playwright/test";
import { apiConfig } from "config/apiConfig";
import { STATUS_CODES } from "data/statusCodes";
import { IProductResponse, IProductsResponse, IProductsSortedResponse } from "data/types/product.types";
import { IResponseMetrics } from "data/types/metrics.types";
import { IOrdersResponse, IOrderResponse } from "data/types/order.types";
import { ICustomersResponse } from "data/types/customer.types";
import { IResponseFields } from "data/types/core.types";

export class Mock {
  constructor(private page: Page) {}

  async routeRequest(url: string | RegExp | ((url: URL) => boolean), body: IResponseFields, statusCode: STATUS_CODES) {
    await this.page.route(url, async (route) => {
      await route.fulfill({
        status: statusCode,
        contentType: "application/json",
        body: JSON.stringify(body),
      });
    });
  }

  async productsPage(body: IProductsSortedResponse, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(/\/api\/products(\?.*)?$/, body, statusCode);
  }

  async productDetailsModal(body: IProductResponse, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.productById(body.Product._id), body, statusCode);
  }

  async metricsHomePage(body: IResponseMetrics, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.metrics, body, statusCode);
  }

  async ordersPage(body: IOrdersResponse, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(/\/api\/orders\?.*$/, body, statusCode);
  }

  async orderDetailsModal(body: IOrderResponse, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.orderById(body.Order._id), body, statusCode);
  }

  async createOrderModal(body: IOrderResponse | IResponseFields, statusCode: STATUS_CODES = STATUS_CODES.CREATED) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.orders, body, statusCode);
  }

  async getCustomersAll(body: ICustomersResponse | IResponseFields, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.customersAll, body, statusCode);
  }

  async getProductsAll(body: IProductsResponse | IResponseFields, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.productsAll, body, statusCode);
  }

  async orderById(body: IOrderResponse | IResponseFields, orderId: string, statusCode: STATUS_CODES = STATUS_CODES.OK) {
    await this.routeRequest(apiConfig.baseURL + apiConfig.endpoints.orderById(orderId), body, statusCode);
  }
}
