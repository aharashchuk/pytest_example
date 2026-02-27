"""DDT cases for order comments (POST/DELETE /api/orders/:id/comments)."""

from __future__ import annotations

import pytest
from bson import ObjectId
from faker import Faker

from sales_portal_tests.data.models.core import CaseApi
from sales_portal_tests.data.sales_portal.errors import ResponseErrors
from sales_portal_tests.data.status_codes import StatusCodes

_faker = Faker()


class CommentOrderCase(CaseApi):
    text: str
    comment_id: str | None

    def __init__(
        self,
        title: str,
        text: str,
        expected_status: StatusCodes,
        expected_error_message: str | None,
        is_success: bool = True,
        comment_id: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            expected_status=expected_status,
            expected_error_message=expected_error_message,
            is_success=is_success,
        )
        self.text = text
        self.comment_id = comment_id


COMMENT_ORDER_POSITIVE_CASES = [
    pytest.param(
        CommentOrderCase(
            title="Add 1-char comment",
            text=_faker.pystr(min_chars=1, max_chars=1),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="comment-1-char",
    ),
    pytest.param(
        CommentOrderCase(
            title="Add 250-char comment",
            text=_faker.pystr(min_chars=250, max_chars=250),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="comment-250-chars",
    ),
    pytest.param(
        CommentOrderCase(
            title="Add regular sentence with punctuation",
            text=_faker.sentence(nb_words=7),
            expected_status=StatusCodes.OK,
            expected_error_message=None,
        ),
        id="comment-sentence",
    ),
]

COMMENT_ORDER_NEGATIVE_CASES = [
    pytest.param(
        CommentOrderCase(
            title="Empty comment is rejected",
            text="",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="comment-empty",
    ),
    pytest.param(
        CommentOrderCase(
            title="Too long comment (251) is rejected",
            text=_faker.pystr(min_chars=251, max_chars=251),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message=ResponseErrors.BAD_REQUEST,
            is_success=False,
        ),
        id="comment-251-chars",
    ),
    pytest.param(
        CommentOrderCase(
            title="Comment with '<' is accepted",
            text="Please check < invalid tag",
            expected_status=StatusCodes.OK,
            expected_error_message=None,
            is_success=True,
        ),
        id="comment-less-than",
    ),
    pytest.param(
        CommentOrderCase(
            title="Comment with '>' is accepted",
            text="Ensure > threshold before ship",
            expected_status=StatusCodes.OK,
            expected_error_message=None,
            is_success=True,
        ),
        id="comment-greater-than",
    ),
]

DELETE_COMMENT_POSITIVE_CASES = [
    pytest.param(
        CommentOrderCase(
            title="Delete existing comment",
            text=_faker.sentence(nb_words=5),
            expected_status=StatusCodes.DELETED,
            expected_error_message=None,
        ),
        id="delete-existing-comment",
    ),
]

DELETE_COMMENT_NEGATIVE_CASES = [
    pytest.param(
        CommentOrderCase(
            title="Non-existing commentId rejected",
            text="",
            comment_id=str(ObjectId()),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Comment was not found",
            is_success=False,
        ),
        id="non-existing-comment-id",
    ),
    pytest.param(
        CommentOrderCase(
            title="Invalid ID format rejected",
            text="",
            comment_id="invalid-comment-id",
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Comment was not found",
            is_success=False,
        ),
        id="invalid-comment-id-format",
    ),
    pytest.param(
        CommentOrderCase(
            title="Empty comment ID is rejected",
            text="",
            comment_id=str(ObjectId()),
            expected_status=StatusCodes.BAD_REQUEST,
            expected_error_message="Comment was not found",
            is_success=False,
        ),
        id="empty-comment-id",
    ),
]
