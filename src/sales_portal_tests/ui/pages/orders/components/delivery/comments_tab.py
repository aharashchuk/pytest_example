"""CommentsTab — order details comments tabpanel."""

from __future__ import annotations

from playwright.sync_api import Locator, expect

from sales_portal_tests.ui.pages.sales_portal_page import SalesPortalPage
from sales_portal_tests.utils.report.allure_step import step


class CommentsTab(SalesPortalPage):
    @property
    def tab(self) -> Locator:
        return self.page.locator('#comments[role="tabpanel"]')

    @property
    def unique_element(self) -> Locator:
        return self.tab.locator("h4", has_text="Comments")

    @property
    def textarea(self) -> Locator:
        return self.tab.locator("#textareaComments")

    @property
    def error(self) -> Locator:
        return self.tab.locator("#error-textareaComments")

    @property
    def create_button(self) -> Locator:
        return self.tab.locator("#create-comment-btn")

    @property
    def comment_cards(self) -> Locator:
        return self.tab.locator("div.shadow-sm.rounded.mx-3.my-3.p-3.border")

    @property
    def comment_text(self) -> Locator:
        return self.comment_cards.locator("p.m-0")

    def get_delete_button(self, card: Locator) -> Locator:
        return card.locator('button[name="delete-comment"][title="Delete"]')

    @step("CREATE BUTTON IS DISABLED")
    def expect_create_disabled(self) -> None:
        expect(self.create_button).to_be_disabled()

    @step("CREATE BUTTON IS ENABLED")
    def expect_create_enabled(self) -> None:
        expect(self.create_button).to_be_enabled()

    @step("TEXT AREA IS EMPTY")
    def expect_textarea_empty(self) -> None:
        expect(self.textarea).to_have_value("")

    @step("FILL TEXT IN COMMENT")
    def fill_comment(self, text: str) -> None:
        self.textarea.fill(text)

    @step("CLICK CREATE BUTTON")
    def click_create(self) -> None:
        self.create_button.click()
