import { INotificationService } from "./notifications.service";
import TelegramBot from "node-telegram-bot-api";

export class TelegramService implements INotificationService {
  private bot: TelegramBot;
  private botToken: string;
  private chatId: string;

  constructor() {
    this.botToken = `${process.env.TELEGRAM_BOT_TOKEN}`;
    this.chatId = `${process.env.TELEGRAM_CHAT_ID}`;
    this.bot = new TelegramBot(this.botToken, { polling: false });
  }

  async postNotification(text: string): Promise<void> {
    try {
      await this.bot.sendMessage(this.chatId, text);
    } catch (e) {
      console.error(JSON.stringify(e, null, " "));
    }
  }
}
