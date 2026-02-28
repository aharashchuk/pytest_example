"""CI helper script — send a test-run summary notification to Telegram.

Usage (in a CI step, after Allure report generation)::

    python scripts/notify_telegram.py --report-url https://your.pages.url/report --passed 42 --failed 0 --skipped 3

All arguments except ``--report-url`` are optional; when omitted the
corresponding field is simply absent from the message.

Environment variables consumed by :class:`TelegramService`:
    TELEGRAM_BOT_TOKEN  — Telegram Bot API token.
    TELEGRAM_CHAT_ID    — Target chat / channel ID.

If either variable is unset the script exits cleanly with a warning so that
missing notification credentials never fail a CI pipeline.
"""

from __future__ import annotations

import argparse
import os
import sys

# Make sure the package is importable when the script is run from the repo root
# even without ``pip install -e .``.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from sales_portal_tests.utils.notifications.telegram_service import TelegramService


def _build_message(
    report_url: str | None,
    passed: int | None,
    failed: int | None,
    skipped: int | None,
    env: str | None,
) -> str:
    """Compose the notification text from the provided run statistics.

    Args:
        report_url: Public URL of the Allure report (or ``None``).
        passed:     Number of passing tests (or ``None`` if unknown).
        failed:     Number of failing tests (or ``None`` if unknown).
        skipped:    Number of skipped tests (or ``None`` if unknown).
        env:        Environment name, e.g. ``"default"``, ``"dev"`` (or ``None``).

    Returns:
        A formatted multi-line string ready to send as a Telegram message.
    """
    emoji = "✅" if not failed else "❌"
    lines: list[str] = [f"{emoji} <b>Test run finished</b>"]

    if env:
        lines.append(f"🌐 Environment: <code>{env}</code>")

    stats: list[str] = []
    if passed is not None:
        stats.append(f"✅ {passed} passed")
    if failed is not None:
        stats.append(f"❌ {failed} failed")
    if skipped is not None:
        stats.append(f"⏭ {skipped} skipped")

    if stats:
        lines.append("  |  ".join(stats))

    if report_url:
        lines.append(f'📊 <a href="{report_url}">View Allure Report</a>')

    return "\n".join(lines)


def main() -> None:
    """Parse CLI arguments, build the notification message, and send it."""
    parser = argparse.ArgumentParser(
        description="Send a Telegram notification with test-run results.",
    )
    parser.add_argument(
        "--report-url",
        default=None,
        help="Public URL of the published Allure report.",
    )
    parser.add_argument(
        "--passed",
        type=int,
        default=None,
        help="Number of passing tests.",
    )
    parser.add_argument(
        "--failed",
        type=int,
        default=None,
        help="Number of failing tests.",
    )
    parser.add_argument(
        "--skipped",
        type=int,
        default=None,
        help="Number of skipped tests.",
    )
    parser.add_argument(
        "--env",
        default=os.getenv("TEST_ENV", "default"),
        help="Environment name (defaults to the TEST_ENV env-var or 'default').",
    )

    args = parser.parse_args()

    message = _build_message(
        report_url=args.report_url,
        passed=args.passed,
        failed=args.failed,
        skipped=args.skipped,
        env=args.env,
    )

    service = TelegramService()
    service.post_notification(message)


if __name__ == "__main__":
    main()
