"""Root conftest.py — session-scoped infrastructure fixtures shared by all tests."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from playwright.sync_api import APIRequestContext, Playwright

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.api.login_api import LoginApi
from sales_portal_tests.api.api.notifications_api import NotificationsApi
from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.api_clients.playwright_api_client import PlaywrightApiClient
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.login_service import LoginService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore


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


# ---------------------------------------------------------------------------
# Session-scoped API wrappers/services (shared by both api/ and ui/ tests)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def products_api(api_client: PlaywrightApiClient) -> ProductsApi:
    """Low-level :class:`ProductsApi` wrapper backed by the shared client."""
    return ProductsApi(api_client)


@pytest.fixture(scope="session")
def customers_api(api_client: PlaywrightApiClient) -> CustomersApi:
    """Low-level :class:`CustomersApi` wrapper backed by the shared client."""
    return CustomersApi(api_client)


@pytest.fixture(scope="session")
def orders_api(api_client: PlaywrightApiClient) -> OrdersApi:
    """Low-level :class:`OrdersApi` wrapper backed by the shared client."""
    return OrdersApi(api_client)


@pytest.fixture(scope="session")
def products_service(products_api: ProductsApi) -> ProductsApiService:
    """High-level :class:`ProductsApiService` backed by the shared products API wrapper."""
    return ProductsApiService(products_api)


@pytest.fixture(scope="session")
def customers_service(customers_api: CustomersApi) -> CustomersApiService:
    """High-level :class:`CustomersApiService` backed by the shared customers API wrapper."""
    return CustomersApiService(customers_api)


@pytest.fixture(scope="session")
def orders_service(
    orders_api: OrdersApi,
    products_service: ProductsApiService,
    customers_service: CustomersApiService,
) -> OrdersApiService:
    """High-level :class:`OrdersApiService` backed by the shared order/product/customer wrappers."""
    return OrdersApiService(orders_api, products_service, customers_service)


@pytest.fixture(scope="session")
def notifications_api(api_client: PlaywrightApiClient) -> NotificationsApi:
    """Low-level :class:`NotificationsApi` wrapper backed by the shared client."""
    return NotificationsApi(api_client)


# ---------------------------------------------------------------------------
# Function-scoped — per-test teardown
# ---------------------------------------------------------------------------


@pytest.fixture
def cleanup(orders_service: OrdersApiService, login_service: LoginService) -> Generator[EntitiesStore, None, None]:
    """Yield a fresh :class:`EntitiesStore`; auto-deletes all tracked entities in teardown.

    Usage inside a test::

        def test_something(cleanup, orders_service, admin_token):
            product = products_service.create(admin_token)
            cleanup.products.add(product.id)
            # ... assertions ...
        # teardown: all tracked entities are deleted automatically
    """
    store = EntitiesStore()
    orders_service.entities_store = store
    yield store
    token = login_service.login_as_admin()
    orders_service.full_delete(token)
    store.clear()


# ---------------------------------------------------------------------------
# Allure reporting hooks
# ---------------------------------------------------------------------------


def pytest_sessionfinish(session: pytest.Session, exitstatus: int | pytest.ExitCode) -> None:
    """Pytest hook — runs once after the entire test session.

    Writes ``allure-results/environment.properties`` so the Allure report
    shows the target environment (URL, env name) on the **Environment** tab.

    Args:
        session:    The pytest session object.
        exitstatus: Integer exit code (0 = all passed).
    """
    from sales_portal_tests.config.env import SALES_PORTAL_API_URL, SALES_PORTAL_URL

    allure_dir = Path("allure-results")
    allure_dir.mkdir(exist_ok=True)
    env_name = os.getenv("TEST_ENV", "default")
    (allure_dir / "environment.properties").write_text(
        f"ENV={env_name}\n" f"UI_URL={SALES_PORTAL_URL}\n" f"API_URL={SALES_PORTAL_API_URL}\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Screenshot-on-failure hook (UI tests only)
# ---------------------------------------------------------------------------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Generator[None, None, None]:
    """Attach a screenshot to Allure whenever a UI test step fails.

    The hook checks for the ``page`` fixture inside the test's ``funcargs``
    dictionary.  If the test has access to a Playwright ``Page`` and the
    **call** phase (i.e. the test body itself, not setup/teardown) fails,
    a PNG screenshot is captured and attached to the Allure report.

    Args:
        item: The pytest test item being executed.
        call: Information about the current test phase (setup / call / teardown).
    """
    import pluggy

    outcome: pluggy.Result[pytest.TestReport] = yield  # type: ignore[assignment]
    report: pytest.TestReport = outcome.get_result()

    funcargs: dict[str, object] = getattr(item, "funcargs", {})
    if report.failed and call.when == "call" and "page" in funcargs:
        page = funcargs["page"]
        try:
            from playwright.sync_api import Page as PlaywrightPage

            if isinstance(page, PlaywrightPage):
                screenshot_bytes: bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception:
            # Never let a reporting failure break the test run
            pass
