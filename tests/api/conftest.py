"""API-level conftest.py — session-scoped API wrappers/services and per-test cleanup fixture."""

from collections.abc import Generator

import pytest

from sales_portal_tests.api.api.customers_api import CustomersApi
from sales_portal_tests.api.api.notifications_api import NotificationsApi
from sales_portal_tests.api.api.orders_api import OrdersApi
from sales_portal_tests.api.api.products_api import ProductsApi
from sales_portal_tests.api.api_clients.playwright_api_client import PlaywrightApiClient
from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.login_service import LoginService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore

# ---------------------------------------------------------------------------
# Session-scoped — stateless wrappers, created once per session
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
