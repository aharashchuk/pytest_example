"""Root conftest.py — session-scoped infrastructure fixtures shared by all tests."""

from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from sales_portal_tests.api.api.login_api import LoginApi
from sales_portal_tests.api.api_clients.playwright_api_client import PlaywrightApiClient
from sales_portal_tests.api.service.login_service import LoginService


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Create a single Playwright APIRequestContext for the entire test session."""
    context = playwright.request.new_context()
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def api_client(api_request_context: APIRequestContext) -> PlaywrightApiClient:
    """Return a :class:`PlaywrightApiClient` backed by the session-scoped request context."""
    return PlaywrightApiClient(api_request_context)


@pytest.fixture(scope="session")
def login_api(api_client: PlaywrightApiClient) -> LoginApi:
    """Return a :class:`LoginApi` wrapper backed by the shared API client."""
    return LoginApi(api_client)


@pytest.fixture(scope="session")
def login_service(login_api: LoginApi) -> LoginService:
    """Return a :class:`LoginService` backed by the shared :class:`LoginApi`."""
    return LoginService(login_api)


@pytest.fixture(scope="session")
def admin_token(login_service: LoginService) -> str:
    """Authenticate once as admin and cache the bearer token for the whole session."""
    return str(login_service.login_as_admin())
