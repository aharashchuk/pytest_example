"""Telegram notification back-end using python-telegram-bot (sync wrapper)."""

from __future__ import annotations

import asyncio
import os

import telegram

from sales_portal_tests.utils.log_utils import log


class TelegramService:
    """Sends notifications via the Telegram Bot API.

    Implements the ``NotificationService`` Protocol through structural sub-typing —
    no explicit ``NotificationService`` import is required.

    The bot token and chat ID are read from the environment variables
    ``TELEGRAM_BOT_TOKEN`` and ``TELEGRAM_CHAT_ID`` at construction time.

    Example::

        service = TelegramService()
        service.post_notification("Test run finished: 42 passed, 0 failed.")
    """

    def __init__(self) -> None:
        self._bot_token: str = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        self._chat_id: str = os.environ.get("TELEGRAM_CHAT_ID", "")

    def post_notification(self, text: str) -> None:
        """Send *text* to the configured Telegram chat.

        Args:
            text: The message to send. HTML formatting is supported.

        Notes:
            - Errors are caught and logged to avoid failing a test run due to a
              notification delivery failure.
            - ``python-telegram-bot`` is async-native; this method runs the
              coroutine synchronously via ``asyncio.run()``.
        """
        if not self._bot_token or not self._chat_id:
            log("TelegramService: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set — skipping notification.")
            return

        async def _send() -> None:
            bot = telegram.Bot(token=self._bot_token)
            async with bot:
                await bot.send_message(chat_id=self._chat_id, text=text)

        try:
            asyncio.run(_send())
        except Exception as exc:
            log(f"TelegramService: failed to send notification — {exc}")
