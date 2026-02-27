"""Confirmation modal assertion helper — reusable UI assertion for modal dialogs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest_check as check

if TYPE_CHECKING:
    from playwright.sync_api import Locator

from sales_portal_tests.data.sales_portal.notifications import ModalCopy


@dataclass
class ConfirmationModal:
    """Locator bundle for a confirmation modal dialog."""

    title: Locator
    confirmation_message: Locator
    confirm_button: Locator


def assert_confirmation_modal(modal: ConfirmationModal, copy: ModalCopy) -> None:
    """Assert that a confirmation modal displays the expected *copy*.

    Uses soft assertions so all three fields are checked even if one fails.

    Args:
        modal:  Locators for the modal's title, body message, and action button.
        copy:   Expected text content from a ``ModalCopy`` data object.
    """
    check.equal(modal.title.inner_text(), copy.title, f"Modal title should be {copy.title!r}")
    check.equal(
        modal.confirmation_message.inner_text(),
        copy.body,
        f"Modal body should be {copy.body!r}",
    )
    check.equal(
        modal.confirm_button.inner_text(),
        copy.action_button,
        f"Modal confirm button should be {copy.action_button!r}",
    )
