"""UI conftest.py — authenticated browser context, page/service fixtures, cleanup."""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pytest
from playwright.sync_api import Page

from sales_portal_tests.api.service.login_service import LoginService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.config.env import SALES_PORTAL_URL
from sales_portal_tests.mock.mock import Mock
from sales_portal_tests.ui.pages.customers.add_new_customer_page import AddNewCustomerPage
from sales_portal_tests.ui.pages.customers.customers_list_page import CustomersListPage
from sales_portal_tests.ui.pages.home_page import HomePage
from sales_portal_tests.ui.pages.login.login_page import LoginPage
from sales_portal_tests.ui.pages.navbar_component import NavBar
from sales_portal_tests.ui.pages.orders.order_details_page import OrderDetailsPage
from sales_portal_tests.ui.pages.orders.orders_list_page import OrdersListPage
from sales_portal_tests.ui.pages.products.add_new_product_page import AddNewProductPage
from sales_portal_tests.ui.pages.products.edit_product_page import EditProductPage
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage
from sales_portal_tests.ui.service.add_new_customer_ui_service import AddNewCustomerUIService
from sales_portal_tests.ui.service.add_new_product_ui_service import AddNewProductUIService
from sales_portal_tests.ui.service.assign_manager_ui_service import AssignManagerUIService
from sales_portal_tests.ui.service.comments_ui_service import CommentsUIService
from sales_portal_tests.ui.service.customers_list_ui_service import CustomersListUIService
from sales_portal_tests.ui.service.edit_product_ui_service import EditProductUIService
from sales_portal_tests.ui.service.home_ui_service import HomeUIService
from sales_portal_tests.ui.service.login_ui_service import LoginUIService
from sales_portal_tests.ui.service.order_details_ui_service import OrderDetailsUIService
from sales_portal_tests.ui.service.products_list_ui_service import ProductsListUIService

# ---------------------------------------------------------------------------
# Auth state
# ---------------------------------------------------------------------------

_AUTH_STATE_PATH = Path("src/.auth/user.json")


@pytest.fixture(scope="session")
def storage_state_path(browser_type_launch_args: dict[str, Any], admin_token: str) -> str:
    """Perform a real UI login once per session and persist the storage state.

    The stored cookies/localStorage are reused by every browser context in
    the session so each test starts already authenticated.

    Args:
        browser_type_launch_args: Launch kwargs forwarded from pytest-playwright.
        admin_token: Bearer token obtained from the API login (session-scoped).

    Returns:
        Path to the saved ``storage_state`` JSON file.
    """
    from playwright.sync_api import sync_playwright

    url = urlparse(SALES_PORTAL_URL)
    hostname = url.hostname or "localhost"

    with sync_playwright() as p:
        browser = p.chromium.launch(**browser_type_launch_args)
        ctx = browser.new_context()
        ctx.add_cookies(
            [
                {
                    "name": "Authorization",
                    "value": admin_token,
                    "domain": hostname,
                    "path": "/",
                }
            ]
        )
        _AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        ctx.storage_state(path=str(_AUTH_STATE_PATH))
        ctx.close()
        browser.close()

    return str(_AUTH_STATE_PATH)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any], storage_state_path: str) -> dict[str, Any]:
    """Override pytest-playwright's built-in fixture to inject auth state and viewport.

    Args:
        browser_context_args: Base context kwargs from pytest-playwright.
        storage_state_path: Path to the saved auth storage state file.

    Returns:
        Updated context kwargs dict with ``storage_state`` and ``viewport`` set.
    """
    return {
        **browser_context_args,
        "storage_state": storage_state_path,
        "viewport": {"width": 1920, "height": 1080},
    }


# ---------------------------------------------------------------------------
# Page-object fixtures (function-scoped — each test gets fresh instances)
# ---------------------------------------------------------------------------


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Fresh :class:`LoginPage` bound to the current test's *page*."""
    return LoginPage(page)


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """Fresh :class:`HomePage` bound to the current test's *page*."""
    return HomePage(page)


@pytest.fixture
def navbar(page: Page) -> NavBar:
    """Fresh :class:`NavBar` component bound to the current test's *page*."""
    return NavBar(page)


@pytest.fixture
def products_list_page(page: Page) -> ProductsListPage:
    """Fresh :class:`ProductsListPage` bound to the current test's *page*."""
    return ProductsListPage(page)


@pytest.fixture
def add_new_product_page(page: Page) -> AddNewProductPage:
    """Fresh :class:`AddNewProductPage` bound to the current test's *page*."""
    return AddNewProductPage(page)


@pytest.fixture
def edit_product_page(page: Page) -> EditProductPage:
    """Fresh :class:`EditProductPage` bound to the current test's *page*."""
    return EditProductPage(page)


@pytest.fixture
def customers_list_page(page: Page) -> CustomersListPage:
    """Fresh :class:`CustomersListPage` bound to the current test's *page*."""
    return CustomersListPage(page)


@pytest.fixture
def add_new_customer_page(page: Page) -> AddNewCustomerPage:
    """Fresh :class:`AddNewCustomerPage` bound to the current test's *page*."""
    return AddNewCustomerPage(page)


@pytest.fixture
def orders_list_page(page: Page) -> OrdersListPage:
    """Fresh :class:`OrdersListPage` bound to the current test's *page*."""
    return OrdersListPage(page)


@pytest.fixture
def order_details_page(page: Page) -> OrderDetailsPage:
    """Fresh :class:`OrderDetailsPage` bound to the current test's *page*."""
    return OrderDetailsPage(page)


# ---------------------------------------------------------------------------
# UI service fixtures (function-scoped)
# ---------------------------------------------------------------------------


@pytest.fixture
def login_ui_service(page: Page) -> LoginUIService:
    """Fresh :class:`LoginUIService` for performing end-to-end login flows."""
    return LoginUIService(page)


@pytest.fixture
def home_ui_service(page: Page) -> HomeUIService:
    """Fresh :class:`HomeUIService` for home-page navigation and metric checks."""
    return HomeUIService(page)


@pytest.fixture
def add_new_product_ui_service(page: Page) -> AddNewProductUIService:
    """Fresh :class:`AddNewProductUIService` for creating products via the UI."""
    return AddNewProductUIService(page)


@pytest.fixture
def edit_product_ui_service(page: Page) -> EditProductUIService:
    """Fresh :class:`EditProductUIService` for editing products via the UI."""
    return EditProductUIService(page)


@pytest.fixture
def products_list_ui_service(page: Page) -> ProductsListUIService:
    """Fresh :class:`ProductsListUIService` for searching/deleting products via the UI."""
    return ProductsListUIService(page)


@pytest.fixture
def add_new_customer_ui_service(page: Page) -> AddNewCustomerUIService:
    """Fresh :class:`AddNewCustomerUIService` for creating customers via the UI."""
    return AddNewCustomerUIService(page)


@pytest.fixture
def customers_list_ui_service(page: Page) -> CustomersListUIService:
    """Fresh :class:`CustomersListUIService` for searching/deleting customers via the UI."""
    return CustomersListUIService(page)


@pytest.fixture
def order_details_ui_service(page: Page) -> OrderDetailsUIService:
    """Fresh :class:`OrderDetailsUIService` for order-details flows via the UI."""
    return OrderDetailsUIService(page)


@pytest.fixture
def assign_manager_ui_service(page: Page) -> AssignManagerUIService:
    """Fresh :class:`AssignManagerUIService` for manager assignment flows via the UI."""
    return AssignManagerUIService(page)


@pytest.fixture
def comments_ui_service(page: Page) -> CommentsUIService:
    """Fresh :class:`CommentsUIService` for comment add/delete flows via the UI."""
    return CommentsUIService(page)


@pytest.fixture
def mock(page: Page) -> Mock:
    """Fresh :class:`Mock` helper for network interception in integration tests."""
    return Mock(page)


# ---------------------------------------------------------------------------
# Per-test cleanup (function-scoped)
# ---------------------------------------------------------------------------


@pytest.fixture
def cleanup(orders_service: OrdersApiService, login_service: LoginService) -> Generator[EntitiesStore, None, None]:
    """Yield a fresh :class:`EntitiesStore`; auto-delete all tracked entities in teardown.

    Mirrors the API-level cleanup fixture so UI tests can provision data via
    API services and still get deterministic cleanup.

    Usage inside a test::

        def test_something(cleanup, orders_service, admin_token):
            order = orders_service.create_order_and_entities(admin_token)
            cleanup.orders.add(order.id)
            # ... assertions ...
        # teardown: all tracked orders/customers/products are deleted automatically

    Note:
        ``orders_service`` and ``login_service`` are inherited from
        ``tests/conftest.py`` and ``tests/api/conftest.py`` automatically — no
        explicit import is required here.
    """
    store = EntitiesStore()
    orders_service.entities_store = store
    yield store
    token = login_service.login_as_admin()
    orders_service.full_delete(token)
    store.clear()
