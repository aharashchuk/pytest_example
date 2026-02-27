import { expect, Locator } from "@playwright/test";
import { logStep } from "utils/report/logStep.utils";
import { SalesPortalPage } from "ui/pages/salesPortal.page";

export class CommentsTab extends SalesPortalPage {
  readonly tab = this.page.locator('#comments[role="tabpanel"]');
  readonly uniqueElement = this.tab.locator("h4", { hasText: "Comments" });
  // form
  readonly textarea = this.tab.locator("#textareaComments");
  readonly error = this.tab.locator("#error-textareaComments");
  readonly createButton = this.tab.locator("#create-comment-btn");
  // cards
  readonly commentCards = this.tab.locator("div.shadow-sm.rounded.mx-3.my-3.p-3.border");
  readonly commentText = this.commentCards.locator("p.m-0");

  private cardText(card: Locator) {
    return card.locator("p.m-0");
  }

  getDeleteButton(card: Locator) {
    return card.locator('button[name="delete-comment"][title="Delete"]');
  }

  @logStep("CREATE BUTTON IS DISABLED")
  async expectCreateDisabled() {
    await expect(this.createButton).toBeDisabled();
  }

  @logStep("CREATE BUTTON IS ENABLED")
  async expectCreateEnabled() {
    await expect(this.createButton).toBeEnabled();
  }

  @logStep("TEXT AREA IS EMPTY")
  async expectTextareaEmpty() {
    await expect(this.textarea).toHaveValue("");
  }

  @logStep("FILL TEXT IN COMMENT")
  async fillComment(text: string) {
    await this.textarea.fill(text);
  }

  @logStep("CLICK CREATE BUTTON")
  async clickCreate() {
    await this.createButton.click();
  }
}
