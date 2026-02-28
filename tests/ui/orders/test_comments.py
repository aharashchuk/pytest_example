"""UI tests — Add/delete comments on order details page."""

from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.orders.comment_order_test_data import (
    COMMENT_ORDER_NEGATIVE_CASES,
    COMMENT_ORDER_POSITIVE_CASES,
    CommentOrderCase,
)
from sales_portal_tests.ui.service.comments_ui_service import CommentsUIService


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestComments:
    """UI tests for adding and deleting comments on the order details page."""

    # ------------------------------------------------------------------
    # Positive: create comment
    # ------------------------------------------------------------------

    @allure.title("Add comment — positive: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", COMMENT_ORDER_POSITIVE_CASES)
    def test_add_comment_positive(
        self,
        case: CommentOrderCase,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add a valid comment; verify count increases and text is visible."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        comments_ui_service.open_order_comments(order.id)
        comments_ui_service.order_details_page.comments_tab.expect_create_disabled()
        comments_ui_service.add_comment(case.text)

        expect(comments_ui_service.order_details_page.comments_tab.comment_cards).to_have_count(1)

    @allure.title("Add comment — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", COMMENT_ORDER_NEGATIVE_CASES)
    def test_add_comment_negative(
        self,
        case: CommentOrderCase,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Fill an invalid comment text; verify error message appears and create stays disabled."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        comments_ui_service.open_order_comments(order.id)
        comments_ui_service.order_details_page.comments_tab.fill_comment(case.text)

        expect(comments_ui_service.order_details_page.comments_tab.error).to_be_visible()
        comments_ui_service.order_details_page.comments_tab.expect_create_disabled()
        expect(comments_ui_service.order_details_page.comments_tab.comment_cards).to_have_count(0)

    # ------------------------------------------------------------------
    # Smoke: multiple comments
    # ------------------------------------------------------------------

    @allure.title("Add multiple comments to same order — displayed newest-first")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_add_multiple_comments(
        self,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add 3 comments sequentially; verify newest comment is shown first."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        comments_ui_service.open_order_comments(order.id)

        comment_texts = ["First comment", "Second comment", "Third comment"]
        for i, text in enumerate(comment_texts):
            comments_ui_service.add_comment(text)
            expect(comments_ui_service.order_details_page.comments_tab.comment_cards).to_have_count(i + 1)

        expect(comments_ui_service.order_details_page.comments_tab.comment_cards).to_have_count(3)
        # newest first
        expect(comments_ui_service.order_details_page.comments_tab.comment_text.nth(0)).to_have_text(comment_texts[2])
        expect(comments_ui_service.order_details_page.comments_tab.comment_text.nth(1)).to_have_text(comment_texts[1])
        expect(comments_ui_service.order_details_page.comments_tab.comment_text.nth(2)).to_have_text(comment_texts[0])

    @allure.title("Create button disabled for empty comment")  # type: ignore[misc]
    @pytest.mark.smoke
    def test_create_button_disabled_for_empty_comment(
        self,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Create button disabled when textarea is empty; enabled when text present; disabled again when cleared."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        comments_ui_service.open_order_comments(order.id)

        tab = comments_ui_service.order_details_page.comments_tab
        tab.expect_textarea_empty()
        tab.expect_create_disabled()

        tab.fill_comment("Some text")
        tab.expect_create_enabled()

        tab.fill_comment("")
        tab.expect_create_disabled()

    # ------------------------------------------------------------------
    # Delete comments
    # ------------------------------------------------------------------

    @allure.title("Delete first comment")  # type: ignore[misc]
    @pytest.mark.regression
    def test_delete_first_comment(
        self,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add 3 comments via API; delete the first one via UI; count decreases to 2."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        orders_service.add_comment(admin_token, order.id, "Comment 1")
        orders_service.add_comment(admin_token, order.id, "Comment 2")
        orders_service.add_comment(admin_token, order.id, "Comment 3")

        comments_ui_service.open_order_comments(order.id)

        tab = comments_ui_service.order_details_page.comments_tab
        expect(tab.comment_cards).to_have_count(3)

        comments_ui_service.delete_first_comment()

        expect(tab.comment_cards).to_have_count(2)

    @allure.title("Delete last comment")  # type: ignore[misc]
    @pytest.mark.regression
    def test_delete_last_comment(
        self,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add 3 comments via API; delete the last one via UI; count decreases to 2."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        orders_service.add_comment(admin_token, order.id, "Comment 1")
        orders_service.add_comment(admin_token, order.id, "Comment 2")
        orders_service.add_comment(admin_token, order.id, "Comment 3")

        comments_ui_service.open_order_comments(order.id)

        tab = comments_ui_service.order_details_page.comments_tab
        expect(tab.comment_cards).to_have_count(3)

        comments_ui_service.delete_last_comment()

        expect(tab.comment_cards).to_have_count(2)

    @allure.title("Delete all comments one by one")  # type: ignore[misc]
    @pytest.mark.regression
    def test_delete_all_comments(
        self,
        orders_service: OrdersApiService,
        comments_ui_service: CommentsUIService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add 3 comments via API; delete all of them via UI; count reaches 0."""
        order = orders_service.create_order_in_process(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        for text in ["Comment A", "Comment B", "Comment C"]:
            orders_service.add_comment(admin_token, order.id, text)

        comments_ui_service.open_order_comments(order.id)

        tab = comments_ui_service.order_details_page.comments_tab
        expect(tab.comment_cards).to_have_count(3)

        comments_ui_service.delete_all_comments()

        expect(tab.comment_cards).to_have_count(0)
