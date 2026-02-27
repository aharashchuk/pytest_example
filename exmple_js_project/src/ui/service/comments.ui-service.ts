import { expect, Page } from "@playwright/test";
import { OrderDetailsPage } from "ui/pages/orders/order-details.page";
import { logStep } from "utils/report/logStep.utils.js";

export class CommentsUIService {
  orderDetailsPage: OrderDetailsPage;

  constructor(private page: Page) {
    this.orderDetailsPage = new OrderDetailsPage(page);
  }

  @logStep("NAVIGATE TO ORDER COMMENTS")
  async openOrderComments(orderId: string) {
    await this.orderDetailsPage.openByOrderId(orderId);
    await this.orderDetailsPage.waitForOpened();
    await this.orderDetailsPage.openCommentsTab();
    await this.orderDetailsPage.commentsTab.waitForOpened();
  }

  @logStep("ADD COMMENT")
  async addComment(text: string) {
    const commentsTab = this.orderDetailsPage.commentsTab;
    const before = await commentsTab.commentCards.count();

    await commentsTab.fillComment(text);
    await commentsTab.expectCreateEnabled();
    await commentsTab.clickCreate();

    await expect(commentsTab.commentCards).toHaveCount(before + 1);
    await expect(commentsTab.commentText.first()).toHaveText(text);
    await commentsTab.expectTextareaEmpty();
    await commentsTab.expectCreateDisabled();
  }

  @logStep("DELETE FIRST COMMENT")
  async deleteFirstComment() {
    const commentsTab = this.orderDetailsPage.commentsTab;
    const before = await commentsTab.commentCards.count();

    await commentsTab.getDeleteButton(commentsTab.commentCards.first()).click();

    await expect(commentsTab.commentCards).toHaveCount(before - 1);
  }

  @logStep("DELETE LAST COMMENT")
  async deleteLastComment() {
    const commentsTab = this.orderDetailsPage.commentsTab;
    const before = await commentsTab.commentCards.count();

    await commentsTab.getDeleteButton(commentsTab.commentCards.last()).click();

    await expect(commentsTab.commentCards).toHaveCount(before - 1);
  }

  @logStep("DELETE ALL COMMENTS")
  async deleteAllComments() {
    const commentsTab = this.orderDetailsPage.commentsTab;

    while ((await commentsTab.commentCards.count()) > 0) {
      const before = await commentsTab.commentCards.count();
      await commentsTab.getDeleteButton(commentsTab.commentCards.first()).click();
      await expect(commentsTab.commentCards).toHaveCount(before - 1);
    }
  }

  @logStep("DELETE COMMENTS BY TEXT")
  async deleteCommentsByText(text: string) {
    const commentsTab = this.orderDetailsPage.commentsTab;

    let card = commentsTab.commentCards
      .filter({
        has: commentsTab.commentText.filter({ hasText: text }),
      })
      .first();

    while (await card.count()) {
      const before = await commentsTab.commentCards.count();
      await commentsTab.getDeleteButton(card).click();
      await expect(commentsTab.commentCards).toHaveCount(before - 1);

      card = commentsTab.commentCards
        .filter({
          has: commentsTab.commentText.filter({ hasText: text }),
        })
        .first();
    }
  }
}
