import { IApiClient } from "api/apiClients/types";
import { apiConfig } from "config/apiConfig";
import { IDeliveryInfo } from "data/salesPortal/delivery-status";
import { ORDER_STATUS } from "data/salesPortal/order-status";
import { IRequestOptions } from "data/types/core.types";
import {
  IGetAllOrdersQuery,
  IOrderCreateBody,
  IOrderResponse,
  IOrdersResponse,
  IOrderUpdateBody,
} from "data/types/order.types";
import { convertRequestParams } from "utils/queryParams.utils";
import { logStep } from "utils/report/logStep.utils";

export class OrdersApi {
  constructor(private apiClient: IApiClient) {}

  @logStep("CREATE /api/orders")
  async create(token: string, payload: IOrderCreateBody) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orders,
      method: "post",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      data: payload,
    };
    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("GET /api/orders/{id}")
  async getById(_id: string, token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderById(_id),
      method: "get",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("CREATE /api/orders/{orderId}/delivery")
  async addDelivery(token: string, orderId: string, deliveryData: IDeliveryInfo) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderDelivery(orderId),
      method: "post",
      data: deliveryData,
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("UPDATE /api/orders/{id}/status")
  async updateStatus(_id: string, status: ORDER_STATUS, token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderStatus(_id),
      method: "put",
      data: { status: status },
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("CREATE /api/orders/{id}/receive")
  async receiveProducts(_id: string, productsId: string[], token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderReceive(_id),
      method: "post",
      data: { products: productsId },
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("DELETE /api/orders/{id}")
  async delete(token: string, _id: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderById(_id),
      method: "delete",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<null>(options);
  }

  @logStep("CREATE /api/orders/{id}/comments")
  async addComment(token: string, orderId: string, comment: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderComments(orderId),
      method: "post",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      data: { comment: comment },
    };
    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("DELETE /api/orders/{id}/comments/{commentId}")
  async deleteComment(token: string, orderId: string, commentId: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderCommentById(orderId, commentId),
      method: "delete",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<null>(options);
  }

  @logStep("UPDATE /api/orders/{id}")
  async update(token: string, _id: string, payload: IOrderUpdateBody) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderById(_id),
      method: "put",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      data: payload,
    };
    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("PUT /api/orders/{orderId}/assign-manager/{managerId}")
  async assingManager(token: string, orderId?: string, managerId?: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderAssignManager(orderId, managerId),
      method: "put",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("PUT /api/orders/{orderId}/unassign-manager")
  async unassingManager(token: string, orderId?: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.orderUnassignManager(orderId),
      method: "put",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };
    return await this.apiClient.send<IOrderResponse>(options);
  }

  @logStep("GET /api/orders")
  async getAll(token: string, params?: IGetAllOrdersQuery) {
    const query = params ? convertRequestParams(params) : "";

    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: `${apiConfig.endpoints.orders}${query}`,
      method: "get",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<IOrdersResponse>(options);
  }
}
