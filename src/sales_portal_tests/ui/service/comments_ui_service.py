"""CommentsUIService — add, delete and navigate to order comments."""

from __future__ import annotations

from playwright.sync_api import Page, expect

from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.utils.report.allure_step import step


class CommentsUIService:
    """High-level flows for the comments tab on the order details page.

    Wraps :class:`OrderDetailsPage` and its
    :attr:`~sales_portal_tests.ui.pages.orders.order_details_page.OrderDetailsPage.comments_tab`
    component.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.order_details_page = OrderDetailsPage(page)

    @step("NAVIGATE TO ORDER COMMENTS TAB")
    def open_order_comments(self, order_id: str) -> None:
        """Open the order details page for *order_id* and switch to comments.

        Args:
            order_id: MongoDB ``_id`` of the order.
        """
        self.order_details_page.open_by_order_id(order_id)
        self.order_details_page.wait_for_opened()
        self.order_details_page.open_comments_tab()
        self.order_details_page.comments_tab.wait_for_opened()

    @step("ADD COMMENT")
    def add_comment(self, text: str) -> None:
        """Fill the comment textarea with *text*, submit and verify it was added.

        Asserts that:
        - the comment count increases by one,
        - the new comment text is at the top of the list,
        - the textarea is cleared after submission,
        - the create button returns to disabled state.

        Args:
            text: Comment body to submit.
        """
        comments_tab = self.order_details_page.comments_tab
        before = comments_tab.comment_cards.count()

        comments_tab.fill_comment(text)
        comments_tab.expect_create_enabled()
        comments_tab.click_create()

        expect(comments_tab.comment_cards).to_have_count(before + 1)
        expect(comments_tab.comment_text.first).to_have_text(text)
        comments_tab.expect_textarea_empty()
        comments_tab.expect_create_disabled()

    @step("DELETE FIRST COMMENT")
    def delete_first_comment(self) -> None:
        """Delete the first (topmost) comment card and verify the count decreases."""
        comments_tab = self.order_details_page.comments_tab
        before = comments_tab.comment_cards.count()

        comments_tab.get_delete_button(comments_tab.comment_cards.first).click()

        expect(comments_tab.comment_cards).to_have_count(before - 1)

    @step("DELETE LAST COMMENT")
    def delete_last_comment(self) -> None:
        """Delete the last (bottommost) comment card and verify the count decreases."""
        comments_tab = self.order_details_page.comments_tab
        before = comments_tab.comment_cards.count()

        comments_tab.get_delete_button(comments_tab.comment_cards.last).click()

        expect(comments_tab.comment_cards).to_have_count(before - 1)

    @step("DELETE ALL COMMENTS")
    def delete_all_comments(self) -> None:
        """Delete every comment card one by one until none remain."""
        comments_tab = self.order_details_page.comments_tab

        while comments_tab.comment_cards.count() > 0:
            before = comments_tab.comment_cards.count()
            comments_tab.get_delete_button(comments_tab.comment_cards.first).click()
            expect(comments_tab.comment_cards).to_have_count(before - 1)

    @step("DELETE COMMENTS BY TEXT")
    def delete_comments_by_text(self, text: str) -> None:
        """Delete all comment cards whose body matches *text*.

        Args:
            text: Exact comment body to match for deletion.
        """
        comments_tab = self.order_details_page.comments_tab

        matching_card = comments_tab.comment_cards.filter(has=comments_tab.comment_text.filter(has_text=text)).first

        while matching_card.count() > 0:
            before = comments_tab.comment_cards.count()
            comments_tab.get_delete_button(matching_card).click()
            expect(comments_tab.comment_cards).to_have_count(before - 1)

            matching_card = comments_tab.comment_cards.filter(has=comments_tab.comment_text.filter(has_text=text)).first
