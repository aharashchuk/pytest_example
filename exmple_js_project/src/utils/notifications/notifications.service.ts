export class NotificationService {
  constructor(private service: INotificationService) {}

  async postNotification(notification: string) {
    await this.service.postNotification(notification);
  }
}

export interface INotificationService {
  postNotification(text: string): Promise<void>;
}
