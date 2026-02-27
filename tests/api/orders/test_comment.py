"""API tests — POST/GET/DELETE /api/orders/:id/comments (Order Comments)."""

from __future__ import annotations

import allure
import pytest

from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.data.sales_portal.orders.comment_order_test_data import (
    COMMENT_ORDER_NEGATIVE_CASES,
    COMMENT_ORDER_POSITIVE_CASES,
    DELETE_COMMENT_NEGATIVE_CASES,
    DELETE_COMMENT_POSITIVE_CASES,
    CommentOrderCase,
)
from sales_portal_tests.data.schemas.orders.schemas import GET_ORDER_SCHEMA
from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Orders")
@pytest.mark.api
@pytest.mark.orders
class TestOrderComments:
    """Tests for POST/GET/DELETE /api/orders/:id/comments."""

    # ------------------------------------------------------------------
    # Add comment — positive DDT
    # ------------------------------------------------------------------

    @allure.title("Add comment — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", COMMENT_ORDER_POSITIVE_CASES)
    def test_add_comment_positive(
        self,
        case: CommentOrderCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add a valid comment to an order; verify the response and that comment appears."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        response = orders_api.add_comment(admin_token, order.id, case.text)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
            schema=GET_ORDER_SCHEMA,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        comments = body["Order"].get("comments", [])
        assert any(
            c["text"] == case.text for c in comments
        ), f"Comment {case.text!r} not found in order comments: {comments}"

    # ------------------------------------------------------------------
    # Add comment — negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT add comment — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", COMMENT_ORDER_NEGATIVE_CASES)
    def test_add_comment_negative(
        self,
        case: CommentOrderCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to add an invalid comment; expect an error response."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        response = orders_api.add_comment(admin_token, order.id, case.text)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )

    # ------------------------------------------------------------------
    # Get comments
    # ------------------------------------------------------------------

    @allure.title("Get comments — returns previously added comments via GET order")  # type: ignore[misc]
    @pytest.mark.regression
    def test_get_comments(
        self,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add a comment and then verify it appears in the GET order response (comments are embedded in the order)."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        comment_text = "Test comment for get"
        orders_api.add_comment(admin_token, order.id, comment_text)

        # Comments are embedded in the order — fetch the order to read them
        response = orders_api.get_by_id(order.id, admin_token)

        validate_response(
            response,
            status=StatusCodes.OK,
            is_success=True,
            error_message=None,
        )

        body = response.body
        assert isinstance(body, dict), f"Expected dict body, got {type(body)}"
        comments = body["Order"].get("comments", [])
        assert any(
            c["text"] == comment_text for c in comments
        ), f"Comment {comment_text!r} not found in order comments: {comments}"

    # ------------------------------------------------------------------
    # Delete comment — positive DDT
    # ------------------------------------------------------------------

    @allure.title("Delete comment — positive: {case}")  # type: ignore[misc]
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", DELETE_COMMENT_POSITIVE_CASES)
    def test_delete_comment_positive(
        self,
        case: CommentOrderCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Add a comment, delete it, and verify the response status."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        # Add comment first
        add_response = orders_api.add_comment(admin_token, order.id, case.text)
        body = add_response.body
        assert isinstance(body, dict)
        comments = body["Order"].get("comments", [])
        assert comments, "Expected at least one comment after adding"
        comment_id = comments[-1]["_id"]

        delete_response = orders_api.delete_comment(admin_token, order.id, comment_id)

        validate_response(
            delete_response,
            status=case.expected_status,
            error_message=case.expected_error_message,
        )

    # ------------------------------------------------------------------
    # Delete comment — negative DDT
    # ------------------------------------------------------------------

    @allure.title("Should NOT delete comment — negative: {case}")  # type: ignore[misc]
    @pytest.mark.regression
    @pytest.mark.parametrize("case", DELETE_COMMENT_NEGATIVE_CASES)
    def test_delete_comment_negative(
        self,
        case: CommentOrderCase,
        orders_api: OrdersApi,
        orders_service: OrdersApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        """Attempt to delete a comment with an invalid/non-existing ID; expect an error."""
        order = orders_service.create_order_and_entities(admin_token, num_products=1)
        cleanup.orders.add(order.id)

        comment_id = case.comment_id if case.comment_id is not None else ""

        response = orders_api.delete_comment(admin_token, order.id, comment_id)

        validate_response(
            response,
            status=case.expected_status,
            is_success=case.is_success,
            error_message=case.expected_error_message,
        )
