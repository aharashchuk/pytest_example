import { IApiClient } from "api/apiClients/types";
import { apiConfig } from "config/apiConfig";
import { IRequestOptions } from "data/types/core.types";
import { INotificationsResponse } from "data/types/notifications.types";
import { logStep } from "utils/report/logStep.utils";

export class NotificationsApi {
  constructor(private apiClient: IApiClient) {}

  @logStep("GET /api/notifications")
  async getUsersNotifications(token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.notifications,
      method: "get",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<INotificationsResponse>(options);
  }

  @logStep("PATCH /api/notifications/{id}")
  async markAsRead(_id: string, token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.notificationAsRead(_id),
      method: "patch",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<INotificationsResponse>(options);
  }

  @logStep("PATCH /api/notifications/mark-all-read")
  async markAllAsRead(_id: string, token: string) {
    const options: IRequestOptions = {
      baseURL: apiConfig.baseURL,
      url: apiConfig.endpoints.notificationAsRead(_id),
      method: "patch",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    };

    return await this.apiClient.send<INotificationsResponse>(options);
  }
}
