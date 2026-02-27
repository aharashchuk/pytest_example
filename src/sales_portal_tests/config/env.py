"""Environment configuration — loads .env or .env.dev and exports typed constants."""

import json
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Determine which env file to load
# ---------------------------------------------------------------------------
_env_file = ".env.dev" if os.getenv("TEST_ENV") == "dev" else ".env"
load_dotenv(dotenv_path=_env_file, override=False)


def _require(name: str) -> str:
    """Return the value of a required environment variable or raise a clear error."""
    value = os.getenv(name)
    if not value:
        raise OSError(
            f"Required environment variable '{name}' is missing. " f"Make sure it is set in your '{_env_file}' file."
        )
    return value


# ---------------------------------------------------------------------------
# Exported constants
# ---------------------------------------------------------------------------

SALES_PORTAL_URL: str = _require("SALES_PORTAL_URL")
SALES_PORTAL_API_URL: str = _require("SALES_PORTAL_API_URL")


@dataclass
class Credentials:
    username: str
    password: str


CREDENTIALS: Credentials = Credentials(
    username=_require("USER_NAME"),
    password=_require("USER_PASSWORD"),
)

MANAGER_IDS: list[str] = json.loads(_require("MANAGER_IDS"))

# Optional — may be absent in local envs
TELEGRAM_BOT_TOKEN: str | None = os.getenv("TELEGRAM_BOT_TOKEN") or None
TELEGRAM_CHAT_ID: str | None = os.getenv("TELEGRAM_CHAT_ID") or None
