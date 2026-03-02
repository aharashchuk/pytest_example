# Framework Improvements — Step-by-Step Implementation Plan

> **Purpose:** This document contains atomic, LLM-executable implementation tasks.
> Each step specifies the exact files to create/modify, the code to write, and the
> acceptance criteria so that an AI coding agent can implement them sequentially
> with no ambiguity.

---

## Table of Contents

1. [STEP 1 — Extract Shared `_auth_headers` Helper](#step-1--extract-shared-_auth_headers-helper)
2. [STEP 2 — Extract Duplicated `_delivery_info_model` Helper](#step-2--extract-duplicated-_delivery_info_model-helper)
3. [STEP 3 — Introduce `TokenProvider` to Prevent Token Expiry](#step-3--introduce-tokenprovider-to-prevent-token-expiry)
4. [STEP 4 — Make Cleanup Fault-Tolerant](#step-4--make-cleanup-fault-tolerant)
5. [STEP 5 — Decouple `EntitiesStore` from `OrdersApiService`](#step-5--decouple-entitiesstore-from-ordersapiservice)
6. [STEP 6 — Introduce `JsonResponse` Type Alias for Stronger Typing](#step-6--introduce-jsonresponse-type-alias-for-stronger-typing)
7. [STEP 7 — Add HTTP-Level Retry Logic to `PlaywrightApiClient`](#step-7--add-http-level-retry-logic-to-playwrightapiclient)
8. [STEP 8 — Add Faker Seed Control for Reproducibility](#step-8--add-faker-seed-control-for-reproducibility)
9. [STEP 9 — Remove Hard Assert from `CreateOrderModal.create_order`](#step-9--remove-hard-assert-from-createordermodalcreate_order)
10. [STEP 10 — Add Integration Tests `conftest.py`](#step-10--add-integration-tests-conftestpy)
11. [STEP 11 — Remove Unused `Tags` Enum or Wire It In](#step-11--remove-unused-tags-enum-or-wire-it-in)
12. [STEP 12 — Add Parallel Execution Safety CI Smoke Target](#step-12--add-parallel-execution-safety-ci-smoke-target)

---

## STEP 1 — Extract Shared `_auth_headers` Helper

### Problem

The identical `_JSON_AUTH_HEADERS` constant and `_auth_headers(token)` function are
copy-pasted across **four** files:

- `src/sales_portal_tests/api/api/products_api.py` (lines 11–14)
- `src/sales_portal_tests/api/api/customers_api.py` (lines 11–14)
- `src/sales_portal_tests/api/api/orders_api.py` (lines 13–16)
- `src/sales_portal_tests/api/api/notifications_api.py` (lines 10–13)

Any change to auth header construction (e.g., adding `Accept`, supporting API keys)
requires updating all four copies.

### Files to Create

#### `src/sales_portal_tests/api/api/headers.py`

```python
"""Shared HTTP header helpers for API endpoint wrappers."""

from __future__ import annotations

_JSON_CONTENT_TYPE: dict[str, str] = {"Content-Type": "application/json"}


def auth_headers(token: str) -> dict[str, str]:
    """Return JSON content-type headers with a Bearer authorization token.

    Args:
        token: Bearer auth token string.

    Returns:
        A dict containing ``Content-Type`` and ``Authorization`` headers.
    """
    return {**_JSON_CONTENT_TYPE, "Authorization": f"Bearer {token}"}
```

### Files to Modify

In **each** of these four files, perform two changes:

1. **Remove** the module-level `_JSON_AUTH_HEADERS` constant and `_auth_headers` function.
2. **Replace** the import: add `from sales_portal_tests.api.api.headers import auth_headers`.
3. **Replace** every call from `_auth_headers(token)` → `auth_headers(token)`.

#### `src/sales_portal_tests/api/api/products_api.py`

- Delete lines 11–14 (`_JSON_AUTH_HEADERS` and `_auth_headers`).
- Add import: `from sales_portal_tests.api.api.headers import auth_headers`
- Replace all occurrences of `_auth_headers(token)` with `auth_headers(token)`.

#### `src/sales_portal_tests/api/api/customers_api.py`

- Same changes as above.

#### `src/sales_portal_tests/api/api/orders_api.py`

- Same changes as above.

#### `src/sales_portal_tests/api/api/notifications_api.py`

- Same changes as above.

### Acceptance Criteria

- [ ] `ruff check src/sales_portal_tests/api/api/` passes with no errors.
- [ ] `mypy --strict src/sales_portal_tests/api/api/` passes.
- [ ] `grep -r "_auth_headers\|_JSON_AUTH_HEADERS" src/sales_portal_tests/api/api/` returns **zero** matches (only `headers.py` has the logic now).
- [ ] All existing API tests still pass: `pytest tests/api/ -x --timeout=60`.

---

## STEP 2 — Extract Duplicated `_delivery_info_model` Helper

### Problem

The private function `_delivery_info_model()` is duplicated identically in two files:

- `src/sales_portal_tests/api/service/orders_service.py` (lines 20–33)
- `src/sales_portal_tests/api/facades/orders_facade_service.py` (lines 17–31)

Both convert the `generate_delivery()` dataclass result to a `DeliveryInfoModel` Pydantic
model. The only trivial difference is that the facade wraps `condition` in
`DeliveryCondition(...)` while the service does not — this should be unified.

### Files to Create

#### `src/sales_portal_tests/data/sales_portal/orders/delivery_helpers.py`

```python
"""Delivery data conversion helper — shared by services and facades."""

from __future__ import annotations

from sales_portal_tests.data.models.delivery import DeliveryAddressModel, DeliveryInfoModel
from sales_portal_tests.data.sales_portal.orders.generate_delivery_data import generate_delivery


def build_delivery_info_model() -> DeliveryInfoModel:
    """Generate random delivery data and return it as a Pydantic ``DeliveryInfoModel``.

    Converts the dataclass returned by :func:`generate_delivery` into the Pydantic
    model expected by the orders API.

    Returns:
        A :class:`DeliveryInfoModel` with random address and condition data.
    """
    info = generate_delivery()
    return DeliveryInfoModel(
        address=DeliveryAddressModel(
            country=str(info.address.country.value),
            city=info.address.city,
            street=info.address.street,
            house=info.address.house,
            flat=info.address.flat,
        ),
        condition=info.condition,
        finalDate=info.final_date,
    )
```

### Files to Modify

#### `src/sales_portal_tests/api/service/orders_service.py`

1. **Delete** the `_delivery_info_model()` function (lines 20–33) and its imports
   (`DeliveryAddressModel`, `DeliveryInfoModel`, `generate_delivery`) that become unused.
2. **Add** import: `from sales_portal_tests.data.sales_portal.orders.delivery_helpers import build_delivery_info_model`.
3. **Replace** every call `_delivery_info_model()` → `build_delivery_info_model()`.

#### `src/sales_portal_tests/api/facades/orders_facade_service.py`

1. **Delete** the `_delivery_info_model()` function (lines 17–31) and its now-unused
   imports (`DeliveryAddressModel`, `DeliveryInfoModel`, `DeliveryCondition`, `generate_delivery`).
2. **Add** import: `from sales_portal_tests.data.sales_portal.orders.delivery_helpers import build_delivery_info_model`.
3. **Replace** every call `_delivery_info_model()` → `build_delivery_info_model()`.

### Acceptance Criteria

- [ ] `grep -r "_delivery_info_model" src/` returns **zero** matches.
- [ ] `ruff check src/` and `mypy --strict src/` pass.
- [ ] Existing tests that exercise delivery creation still pass.

---

## STEP 3 — Introduce `TokenProvider` to Prevent Token Expiry

### Problem

The `admin_token` fixture in `tests/conftest.py` (line 57) is `scope="session"` and
returns a plain `str`. If the server's JWT expires mid-session (common TTL: 30–60 min),
every subsequent test silently fails with 401.

### Files to Create

#### `src/sales_portal_tests/api/service/token_provider.py`

```python
"""TokenProvider — TTL-aware bearer token cache with automatic refresh."""

from __future__ import annotations

import time

from sales_portal_tests.api.service.login_service import LoginService
from sales_portal_tests.utils.log_utils import log


class TokenProvider:
    """Provides a cached bearer token that automatically refreshes before expiry.

    Args:
        login_service: The :class:`LoginService` used to obtain tokens.
        ttl_seconds: Token time-to-live in seconds.  The token is refreshed
                     when at least this many seconds have elapsed since the
                     last login.  Defaults to 25 minutes (1500 s), providing a
                     safety margin for a typical 30-minute server TTL.
    """

    def __init__(self, login_service: LoginService, ttl_seconds: int = 1500) -> None:
        self._login_service = login_service
        self._ttl = ttl_seconds
        self._token: str = ""
        self._obtained_at: float = 0.0

    def get_token(self) -> str:
        """Return a valid bearer token, refreshing transparently if expired.

        Returns:
            A non-empty bearer token string.
        """
        if self._is_expired():
            log("Token expired or missing — refreshing…")
            self._token = self._login_service.login_as_admin()
            self._obtained_at = time.monotonic()
        return self._token

    def _is_expired(self) -> bool:
        """Check whether the current token should be considered expired."""
        if not self._token:
            return True
        return (time.monotonic() - self._obtained_at) >= self._ttl
```

### Files to Modify

#### `tests/conftest.py`

1. **Add import:**

   ```python
   from sales_portal_tests.api.service.token_provider import TokenProvider
   ```

2. **Add a new session-scoped fixture** right after the existing `login_service` fixture:

   ```python
   @pytest.fixture(scope="session")
   def token_provider(login_service: LoginService) -> TokenProvider:
       """Session-scoped :class:`TokenProvider` with automatic refresh."""
       return TokenProvider(login_service)
   ```

3. **Modify the `admin_token` fixture** to delegate to `TokenProvider`:

   Change from:

   ```python
   @pytest.fixture(scope="session")
   def admin_token(login_service: LoginService) -> str:
       """Authenticate once as admin and cache the bearer token for the whole session."""
       return str(login_service.login_as_admin())
   ```

   To:

   ```python
   @pytest.fixture
   def admin_token(token_provider: TokenProvider) -> str:
       """Return a valid admin bearer token, refreshing automatically if expired."""
       return token_provider.get_token()
   ```

   **Note:** The scope changes from `session` to `function` so that each test
   gets a fresh call to `get_token()` (which returns the cached value instantly
   if still valid).

4. **Update the `cleanup` fixture** to use `token_provider` instead of `login_service`
   for obtaining the teardown token:

   Change from:

   ```python
   @pytest.fixture
   def cleanup(orders_service: OrdersApiService, login_service: LoginService) -> Generator[EntitiesStore, None, None]:
       store = EntitiesStore()
       orders_service.entities_store = store
       yield store
       token = login_service.login_as_admin()
       orders_service.full_delete(token)
       store.clear()
   ```

   To:

   ```python
   @pytest.fixture
   def cleanup(orders_service: OrdersApiService, token_provider: TokenProvider) -> Generator[EntitiesStore, None, None]:
       store = EntitiesStore()
       orders_service.entities_store = store
       yield store
       token = token_provider.get_token()
       orders_service.full_delete(token)
       store.clear()
   ```

### Acceptance Criteria

- [ ] `mypy --strict src/sales_portal_tests/api/service/token_provider.py` passes.
- [ ] `admin_token` fixture is now function-scoped (verify with `pytest --fixtures tests/`).
- [ ] A session longer than 30 minutes no longer produces 401 failures.
- [ ] All existing tests pass: `pytest tests/ -x --timeout=120`.

---

## STEP 4 — Make Cleanup Fault-Tolerant

### Problem

In `src/sales_portal_tests/api/service/orders_service.py`, the `full_delete()` method
(lines 318–330) iterates entities and deletes them sequentially. If any single delete
throws (e.g., entity already deleted, server 500), the remaining entities **leak** — they
are never cleaned up.

### Files to Modify

#### `src/sales_portal_tests/api/service/orders_service.py`

Replace the `full_delete` method body. Change from:

```python
@step("FULL DELETE ORDERS AND ENTITIES - API")
def full_delete(self, token: str) -> None:
    """Delete all entities tracked in :attr:`entities_store`.

    Deletes orders first, then customers, then products to respect
    referential constraints.

    Args:
        token: Bearer auth token.
    """
    for order_id in list(self.entities_store.orders):
        self.delete(token, order_id)
    for customer_id in list(self.entities_store.customers):
        self._customers_service.delete(token, customer_id)
    for product_id in list(self.entities_store.products):
        self._products_service.delete(token, product_id)
```

To:

```python
@step("FULL DELETE ORDERS AND ENTITIES - API")
def full_delete(self, token: str) -> None:
    """Delete all entities tracked in :attr:`entities_store`.

    Deletes orders first, then customers, then products to respect
    referential constraints.  Individual delete failures are logged
    and suppressed so that remaining entities are still cleaned up.

    Args:
        token: Bearer auth token.
    """
    for order_id in list(self.entities_store.orders):
        try:
            self.delete(token, order_id)
        except Exception as exc:
            log(f"[Cleanup] Failed to delete order {order_id}: {exc}")
    for customer_id in list(self.entities_store.customers):
        try:
            self._customers_service.delete(token, customer_id)
        except Exception as exc:
            log(f"[Cleanup] Failed to delete customer {customer_id}: {exc}")
    for product_id in list(self.entities_store.products):
        try:
            self._products_service.delete(token, product_id)
        except Exception as exc:
            log(f"[Cleanup] Failed to delete product {product_id}: {exc}")
```

Also add the missing import at the top of the file if not already present:

```python
from sales_portal_tests.utils.log_utils import log
```

### Acceptance Criteria

- [ ] `ruff check src/sales_portal_tests/api/service/orders_service.py` passes.
- [ ] `mypy --strict src/sales_portal_tests/api/service/orders_service.py` passes.
- [ ] When a delete call raises, cleanup continues and remaining entities are deleted.
- [ ] All existing tests pass.

---

## STEP 5 — Decouple `EntitiesStore` from `OrdersApiService`

### Problem

The `cleanup` fixture in `tests/conftest.py` (line 120) mutates the **session-scoped**
`OrdersApiService` by overwriting its `entities_store` attribute:

```python
orders_service.entities_store = store
```

Under parallel execution (`pytest-xdist`), multiple workers sharing the session object
will race on this mutable field, causing cross-test entity tracking corruption.

### Solution

Create a standalone `CleanupService` that accepts the store and all sub-services.
Remove `entities_store` from `OrdersApiService` entirely.

### Files to Create

#### `src/sales_portal_tests/api/service/cleanup_service.py`

```python
"""CleanupService — fault-tolerant entity cleanup for test teardown."""

from __future__ import annotations

from sales_portal_tests.api.service.customers_service import CustomersApiService
from sales_portal_tests.api.service.orders_service import OrdersApiService
from sales_portal_tests.api.service.products_service import ProductsApiService
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore
from sales_portal_tests.utils.log_utils import log
from sales_portal_tests.utils.report.allure_step import step


class CleanupService:
    """Deletes all entities tracked in an :class:`EntitiesStore`.

    Entity deletion order respects referential constraints:
    orders → customers → products.  Individual failures are logged and
    suppressed so remaining entities are still cleaned up.

    Args:
        orders_service: Service for deleting orders.
        customers_service: Service for deleting customers.
        products_service: Service for deleting products.
    """

    def __init__(
        self,
        orders_service: OrdersApiService,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
    ) -> None:
        self._orders_service = orders_service
        self._customers_service = customers_service
        self._products_service = products_service

    @step("CLEANUP: DELETE ALL TRACKED ENTITIES")
    def delete_all(self, token: str, store: EntitiesStore) -> None:
        """Delete every entity tracked in *store*, then clear the store.

        Args:
            token: Bearer auth token.
            store: The :class:`EntitiesStore` whose entity IDs should be deleted.
        """
        for order_id in list(store.orders):
            try:
                self._orders_service.delete(token, order_id)
            except Exception as exc:
                log(f"[Cleanup] Failed to delete order {order_id}: {exc}")

        for customer_id in list(store.customers):
            try:
                self._customers_service.delete(token, customer_id)
            except Exception as exc:
                log(f"[Cleanup] Failed to delete customer {customer_id}: {exc}")

        for product_id in list(store.products):
            try:
                self._products_service.delete(token, product_id)
            except Exception as exc:
                log(f"[Cleanup] Failed to delete product {product_id}: {exc}")

        store.clear()
```

### Files to Modify

#### `src/sales_portal_tests/api/service/orders_service.py`

1. **Remove** the `entities_store` parameter from `__init__` and the `self.entities_store`
   attribute entirely.

   Change the `__init__` from:

   ```python
   def __init__(
       self,
       orders_api: OrdersApi,
       products_service: ProductsApiService,
       customers_service: CustomersApiService,
       entities_store: EntitiesStore | None = None,
   ) -> None:
       self._orders_api = orders_api
       self._products_service = products_service
       self._customers_service = customers_service
       self.entities_store: EntitiesStore = entities_store if entities_store is not None else EntitiesStore()
   ```

   To:

   ```python
   def __init__(
       self,
       orders_api: OrdersApi,
       products_service: ProductsApiService,
       customers_service: CustomersApiService,
   ) -> None:
       self._orders_api = orders_api
       self._products_service = products_service
       self._customers_service = customers_service
   ```

2. **Remove** the `full_delete` method entirely (it now lives in `CleanupService`).

3. **Remove** the `EntitiesStore` import if it becomes unused.

4. **Update `create_order_and_entities`** and similar methods that reference
   `self.entities_store` — these methods should **return** the created IDs and let the
   test register them via the `cleanup` fixture instead:

   Change `create_order_and_entities` from:

   ```python
   @step("CREATE ORDER AND ENTITIES - API")
   def create_order_and_entities(self, token: str, num_products: int) -> OrderFromResponse:
       customer = self._customers_service.create(token)
       self.entities_store.customers.add(customer.id)
       product_ids: list[str] = []
       for _ in range(num_products):
           product = self._products_service.create(token)
           product_ids.append(product.id)
       self.entities_store.products.update(product_ids)
       order = self.create(token, customer.id, product_ids)
       self.entities_store.orders.add(order.id)
       return order
   ```

   To:

   ```python
   @step("CREATE ORDER AND ENTITIES - API")
   def create_order_and_entities(self, token: str, num_products: int) -> OrderFromResponse:
       """Create a customer, *num_products* products, and an order linking them.

       **Caller** is responsible for registering the returned entity IDs in
       the ``cleanup`` fixture's :class:`EntitiesStore`.

       Args:
           token: Bearer auth token.
           num_products: Number of products to create and attach to the order.
       """
       customer = self._customers_service.create(token)
       product_ids: list[str] = []
       for _ in range(num_products):
           product = self._products_service.create(token)
           product_ids.append(product.id)
       order = self.create(token, customer.id, product_ids)
       return order
   ```

   Apply the same pattern to `create_order_with_delivery`, `create_order_in_process`,
   `create_canceled_order`, `create_partially_received_order`, `create_received_order`,
   and `create_order_in_status` — remove all `self.entities_store.*` calls.

#### `tests/conftest.py`

1. **Add imports:**

   ```python
   from sales_portal_tests.api.service.cleanup_service import CleanupService
   ```

2. **Add a new session-scoped fixture:**

   ```python
   @pytest.fixture(scope="session")
   def cleanup_service(
       orders_service: OrdersApiService,
       customers_service: CustomersApiService,
       products_service: ProductsApiService,
   ) -> CleanupService:
       """Session-scoped :class:`CleanupService` for teardown."""
       return CleanupService(orders_service, customers_service, products_service)
   ```

3. **Rewrite the `cleanup` fixture:**

   Change from:

   ```python
   @pytest.fixture
   def cleanup(orders_service: OrdersApiService, login_service: LoginService) -> Generator[EntitiesStore, None, None]:
       store = EntitiesStore()
       orders_service.entities_store = store
       yield store
       token = login_service.login_as_admin()
       orders_service.full_delete(token)
       store.clear()
   ```

   To:

   ```python
   @pytest.fixture
   def cleanup(
       cleanup_service: CleanupService,
       token_provider: TokenProvider,
   ) -> Generator[EntitiesStore, None, None]:
       """Yield a fresh :class:`EntitiesStore`; auto-deletes all tracked entities in teardown."""
       store = EntitiesStore()
       yield store
       token = token_provider.get_token()
       cleanup_service.delete_all(token, store)
   ```

#### All test files that call `orders_service.create_order_and_entities()`

Tests that previously relied on `OrdersApiService` auto-registering IDs into the store
must now register them manually. For example, in `tests/ui/orders/test_order_delivery.py`:

Change from:

```python
order = orders_service.create_order_and_entities(admin_token, num_products=1)
cleanup.orders.add(order.id)
```

To:

```python
order = orders_service.create_order_and_entities(admin_token, num_products=1)
cleanup.orders.add(order.id)
# Also register the customer and product IDs created inside the helper:
cleanup.customers.add(order.customer.id)
for p in order.products:
    cleanup.products.add(p.id)
```

> **Note:** Since `OrderFromResponse` already includes the nested `customer.id` and
> `products[*].id`, the test has the information it needs. A convenience method can be
> added to `EntitiesStore` to simplify this (see below).

#### `src/sales_portal_tests/api/service/stores/entities_store.py`

Add a convenience method:

```python
def track_order(self, order: OrderFromResponse) -> None:
    """Register an order and all its nested entity IDs for cleanup.

    Args:
        order: The :class:`OrderFromResponse` whose IDs should be tracked.
    """
    self.orders.add(order.id)
    if order.customer and order.customer.id:
        self.customers.add(order.customer.id)
    for product in order.products:
        if product.id:
            self.products.add(product.id)
```

This allows tests to write:

```python
order = orders_service.create_order_and_entities(admin_token, num_products=2)
cleanup.track_order(order)
```

### Acceptance Criteria

- [ ] `OrdersApiService` no longer has an `entities_store` attribute.
- [ ] `grep -r "entities_store" src/sales_portal_tests/api/service/orders_service.py` returns zero matches.
- [ ] `CleanupService` exists and has fault-tolerant deletion.
- [ ] `cleanup` fixture no longer mutates session-scoped objects.
- [ ] `ruff check src/ tests/` and `mypy --strict src/ tests/` pass.
- [ ] All existing API and UI tests pass.

---

## STEP 6 — Introduce `JsonResponse` Type Alias for Stronger Typing

### Problem

`Response[object | None]` is used everywhere, forcing downstream code to write
`assert isinstance(body, dict)` before accessing dict keys. The generic parameter
provides no practical value.

### Files to Modify

#### `src/sales_portal_tests/data/models/core.py`

Add the following type alias after the `Response` class definition:

```python
from typing import Any

# Convenient alias for the common case: an API response with a JSON dict body.
JsonResponse = Response[dict[str, Any]]
```

#### All API wrapper files (`products_api.py`, `customers_api.py`, `orders_api.py`, `notifications_api.py`, `login_api.py`)

Change return types from `Response[object | None]` to `JsonResponse` for methods
that always return JSON. For example, in `products_api.py`:

Change:

```python
def create(self, product: Product, token: str) -> Response[object | None]:
```

To:

```python
def create(self, product: Product, token: str) -> JsonResponse:
```

**Exception:** The `delete` methods that return 204 (no body) should remain
`Response[object | None]` since the body is `None`.

#### All service files that assert `isinstance(body, dict)`

Remove the `assert isinstance(body, dict)` lines since the type is now guaranteed
by the return type. For example, in `products_service.py`:

Change:

```python
body = response.body
assert isinstance(body, dict), f"Expected dict response body, got {type(body)}"
return ProductFromResponse.from_api(body["Product"])
```

To:

```python
return ProductFromResponse.from_api(response.body["Product"])
```

### Acceptance Criteria

- [ ] `JsonResponse` is defined in `data/models/core.py`.
- [ ] `grep -rn "assert isinstance(body, dict)" src/` returns zero matches (for methods
      that now return `JsonResponse`).
- [ ] `mypy --strict src/` passes.
- [ ] All existing tests pass.

---

## STEP 7 — Add HTTP-Level Retry Logic to `PlaywrightApiClient`

### Problem

`PlaywrightApiClient.send()` does not handle transient server errors (502, 503, 504)
or connection resets. A single flaky network response fails the test immediately.
While `pytest-rerunfailures` retries the entire test, HTTP-level retry is cheaper.

### Files to Modify

#### `src/sales_portal_tests/api/api_clients/playwright_api_client.py`

1. **Add** a module-level constant for retryable status codes:

   ```python
   import time

   _RETRYABLE_STATUSES: frozenset[int] = frozenset({502, 503, 504})
   _MAX_RETRIES: int = 2
   _RETRY_DELAY_SECONDS: float = 1.0
   ```

2. **Modify the `send` method** to add retry logic around the `fetch` call:

   Change from:

   ```python
   with allure.step(step_title):
       fetch_kwargs = self._build_fetch_kwargs(options)
       raw: APIResponse = self._api_context.fetch(options.url, **fetch_kwargs)
       response = self._transform_response(raw)

       self._attach_request(options)
       self._attach_response(response)

       return response
   ```

   To:

   ```python
   with allure.step(step_title):
       fetch_kwargs = self._build_fetch_kwargs(options)

       last_response: Response[object | None] | None = None
       for attempt in range(_MAX_RETRIES + 1):
           raw: APIResponse = self._api_context.fetch(options.url, **fetch_kwargs)
           last_response = self._transform_response(raw)
           if last_response.status not in _RETRYABLE_STATUSES:
               break
           if attempt < _MAX_RETRIES:
               log(
                   f"[Retry] {options.method} {options.url} returned "
                   f"{last_response.status}, attempt {attempt + 1}/{_MAX_RETRIES}"
               )
               time.sleep(_RETRY_DELAY_SECONDS)

       assert last_response is not None
       self._attach_request(options)
       self._attach_response(last_response)

       return last_response
   ```

3. **Add import** at top of file:
   ```python
   import time
   from sales_portal_tests.utils.log_utils import log
   ```

### Acceptance Criteria

- [ ] `mypy --strict src/sales_portal_tests/api/api_clients/playwright_api_client.py` passes.
- [ ] A 502 response is retried up to 2 times before being returned.
- [ ] A 200 response is returned immediately without retries.
- [ ] All existing tests pass.

---

## STEP 8 — Add Faker Seed Control for Reproducibility

### Problem

DDT case tables in `src/sales_portal_tests/data/sales_portal/*/` use Faker at module
import time. The generated data is non-deterministic — you cannot reproduce a specific
failure.

### Files to Create

#### `src/sales_portal_tests/data/seed.py`

```python
"""Faker seed configuration for reproducible test data generation.

Set the ``FAKER_SEED`` environment variable to fix the seed.
When unset, a random seed is used and logged so you can reproduce later.

Usage (in any module that uses Faker)::

    from sales_portal_tests.data.seed import faker_instance

    name = faker_instance.name()
"""

from __future__ import annotations

import os
import random

from faker import Faker

_env_seed = os.getenv("FAKER_SEED")
FAKER_SEED: int = int(_env_seed) if _env_seed else random.randint(0, 2**31 - 1)

faker_instance: Faker = Faker()
Faker.seed(FAKER_SEED)

print(f"[test-data] Faker seed: {FAKER_SEED}  (reproduce with FAKER_SEED={FAKER_SEED})")
```

### Files to Modify

All files that create their own `Faker()` instance should import from the shared seed
module instead. Search for them:

```bash
grep -rn "from faker import Faker\|Faker()" src/sales_portal_tests/data/
```

In each file found, replace:

```python
from faker import Faker
_faker = Faker()
```

With:

```python
from sales_portal_tests.data.seed import faker_instance as _faker
```

### Acceptance Criteria

- [ ] Running tests prints `[test-data] Faker seed: <N>` once at startup.
- [ ] Setting `FAKER_SEED=42` produces the same DDT case data every run.
- [ ] `grep -rn "Faker()" src/sales_portal_tests/data/` returns only `seed.py`.
- [ ] `ruff check src/` and `mypy --strict src/` pass.
- [ ] All tests pass.

---

## STEP 9 — Remove Hard Assert from `CreateOrderModal.create_order`

### Problem

`src/sales_portal_tests/ui/pages/orders/create_order_modal.py` line 100 has:

```python
assert response.status == StatusCodes.CREATED, f"Expected {StatusCodes.CREATED}, got {response.status}"
```

This is a **hard assert inside framework code** (a Page Object). If it fails, the error
traces to the PO instead of the test, confusing debugging.

### Files to Modify

#### `src/sales_portal_tests/ui/pages/orders/create_order_modal.py`

Replace the hard assert with a soft check using `pytest_check`, consistent with the
framework's validation patterns:

Change from:

```python
    response: Response[dict[str, object]] = self.intercept_response(
        api_config.ORDERS,
        self.click_create,
    )
    assert response.status == StatusCodes.CREATED, f"Expected {StatusCodes.CREATED}, got {response.status}"
    order_data = response.body.get("Order", {})
    return OrderFromResponse.model_validate(order_data)
```

To:

```python
    response: Response[dict[str, object]] = self.intercept_response(
        api_config.ORDERS,
        self.click_create,
    )
    check.equal(
        response.status,
        StatusCodes.CREATED,
        f"Create order: expected HTTP {StatusCodes.CREATED}, got {response.status}",
    )
    order_data = response.body.get("Order", {})
    return OrderFromResponse.model_validate(order_data)
```

Add the import at the top:

```python
import pytest_check as check
```

### Acceptance Criteria

- [ ] No `assert` statements remain in `create_order_modal.py` other than any inside
      dataclass/model methods.
- [ ] `ruff check` and `mypy --strict` pass.
- [ ] UI order creation tests still pass.

---

## STEP 10 — Add Integration Tests `conftest.py`

### Problem

`tests/ui/integration/` has no `conftest.py`. Integration tests (mock-based) share the
same configuration as real UI tests with no isolation enforcement.

### Files to Create

#### `tests/ui/integration/conftest.py`

```python
"""Integration test conftest — auto-applies the ``integration`` marker."""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Automatically add the ``integration`` marker to all tests in this directory.

    This ensures integration tests are always selectable via
    ``pytest -m integration`` even if a developer forgets the decorator.
    """
    for item in items:
        if "integration" not in [m.name for m in item.iter_markers()]:
            item.add_marker(pytest.mark.integration)
```

### Acceptance Criteria

- [ ] Running `pytest tests/ui/integration/ --collect-only` shows every test has
      the `integration` marker.
- [ ] Running `pytest -m "not integration"` excludes all integration tests.
- [ ] File passes `ruff check` and `mypy --strict`.

---

## STEP 11 — Remove Unused `Tags` Enum or Wire It In

### Problem

`src/sales_portal_tests/data/tags.py` defines a `Tags(StrEnum)` with values like
`SMOKE = "smoke"`, `API = "api"`, etc. But no test file imports or uses it — tests
use `@pytest.mark.smoke` directly as string markers.

### Decision: Remove It

The `Tags` enum adds no runtime value since pytest markers are strings. It's dead code.

### Files to Delete

- `src/sales_portal_tests/data/tags.py`

### Files to Modify

#### `src/sales_portal_tests/data/__init__.py`

If this file imports or re-exports `Tags`, remove that import.

### Acceptance Criteria

- [ ] `grep -rn "from sales_portal_tests.data.tags\|from sales_portal_tests.data import tags" src/ tests/`
      returns zero matches.
- [ ] `ruff check src/ tests/` passes.
- [ ] All tests pass.

---

## STEP 12 — Add Parallel Execution Safety CI Smoke Target

### Problem

`test-api-parallel` exists in the `Makefile` but parallel execution has not been validated
against the mutable state issues (now fixed by Steps 3–5). A CI-specific target should
exist to gate parallel safety.

### Files to Modify

#### `Makefile`

Add a new target after `test-api-parallel`:

```makefile
test-parallel-smoke: ## Run a subset of API tests in parallel to validate xdist safety
	pytest tests/api/products/ tests/api/customers/ -m smoke -n 4 --alluredir=allure-results --timeout=60
```

### Acceptance Criteria

- [ ] `make test-parallel-smoke` runs tests across 4 workers without cleanup conflicts.
- [ ] No entity leaks after parallel run (verify DB or check cleanup logs).

---

---

## STEP 13 — Add Code Coverage Reporting

### Problem

There is no visibility into which source code paths are exercised by tests.
`pytest-cov` is absent from dependencies; no coverage targets or thresholds are defined.

### Files to Modify

#### `requirements.txt`

Append:
```
pytest-cov>=6.0
```

#### `pyproject.toml`

Add a `[tool.coverage.run]` section:
```toml
[tool.coverage.run]
source = ["src/sales_portal_tests"]
omit = ["*/__init__.py"]
branch = true

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 50
```

#### `Makefile`

Add a new target:
```makefile
coverage: ## Generate HTML coverage report
	pytest tests/ --cov=src/sales_portal_tests --cov-report=term-missing --cov-report=html:coverage-report
	@echo "Report: coverage-report/index.html"
```

#### `.github/workflows/tests.yml`

After the "Run UI tests" step, add:
```yaml
- name: Upload coverage report
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: coverage-report/
```

### Acceptance Criteria

- [ ] `make coverage` runs without error and produces `coverage-report/index.html`.
- [ ] Coverage percentage is printed in terminal output.
- [ ] `ruff check` and `mypy --strict` pass.

---

## STEP 14 — Add Docker Compose Application Startup to CI

### Problem

`.github/workflows/tests.yml` assumes the application is pre-deployed. There is no
self-contained CI run — tests fail on fresh environments with "Connection refused".

### Files to Modify

#### `.github/workflows/tests.yml`

**Insert before "Run API tests":**
```yaml
- name: Start application stack
  working-directory: sales-portal
  run: docker compose up -d --wait
  timeout-minutes: 3

- name: Wait for backend health
  run: |
    for i in $(seq 1 30); do
      curl -sf http://localhost:8686/api/docs && break
      echo "Waiting for backend... attempt $i"
      sleep 2
    done
```

**Set default env vars** (place under the `env:` key of the job, or as step env):
```yaml
env:
  SALES_PORTAL_URL: http://localhost:8585
  SALES_PORTAL_API_URL: http://localhost:8686
  USER_NAME: admin@example.com
  USER_PASSWORD: admin123
```
These are the `docker-compose.yml` defaults for the local stack. They should be
overridden by GitHub Secrets for production environments.

**Insert as final step with `if: always()`:**
```yaml
- name: Stop application stack
  if: always()
  working-directory: sales-portal
  run: docker compose down -v
```

### Acceptance Criteria

- [ ] Triggering CI on a branch with no pre-deployed environment runs tests successfully.
- [ ] Docker containers appear in the CI log under "Start application stack".
- [ ] "Connection refused" errors are gone.

---

## STEP 15 — Expand Integration Test Coverage for Products and Customers

### Problem

Only 3 integration test files exist, all for order creation.
Products and Customers have no mocked UI integration tests.

### Files to Create

- `tests/ui/integration/test_products_list.py`
- `tests/ui/integration/test_customers_list.py`

### Files to Modify

#### `src/sales_portal_tests/mock/mock.py`

Add helpers for missing endpoints:
```python
def get_products_list(self, body: dict[str, object], status_code: int = StatusCodes.OK) -> None:
    """Mock GET /api/products response."""
    self.route_request(re.compile(r"/api/products(\?.*)?$"), body, status_code)

def get_customers_list(self, body: dict[str, object], status_code: int = StatusCodes.OK) -> None:
    """Mock GET /api/customers response."""
    self.route_request(re.compile(r"/api/customers(\?.*)?$"), body, status_code)
```

Add the `import re` at the top if not already present.

#### `tests/ui/integration/test_products_list.py`

```python
"""Integration tests — Products list page against mocked backend."""

from __future__ import annotations

import pytest
import allure

from sales_portal_tests.mock.mock import Mock
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage


@allure.suite("UI")
@allure.sub_suite("Integration / Products")
@pytest.mark.integration
@pytest.mark.ui
class TestProductsListIntegration:

    def test_products_list_shows_empty_state(
        self,
        mock: Mock,
        products_list_page: ProductsListPage,
    ) -> None:
        mock.get_products_list({"Products": [], "IsSuccess": True})
        products_list_page.open()
        products_list_page.wait_for_opened()
        # Assert empty-state element is visible (adjust locator to match the app)
        products_list_page.expect_empty_state()

    def test_products_list_shows_items(
        self,
        mock: Mock,
        products_list_page: ProductsListPage,
    ) -> None:
        mock.get_products_list({
            "Products": [
                {"_id": "aaa", "title": "Widget A", "price": 9.99, "notes": ""},
                {"_id": "bbb", "title": "Widget B", "price": 19.99, "notes": ""},
            ],
            "IsSuccess": True,
        })
        products_list_page.open()
        products_list_page.wait_for_opened()
        products_list_page.expect_row_count(2)

    def test_products_list_shows_error_toast_on_server_error(
        self,
        mock: Mock,
        products_list_page: ProductsListPage,
    ) -> None:
        mock.get_products_list(
            {"IsSuccess": False, "ErrorMessage": "Internal Server Error"},
            status_code=500,
        )
        products_list_page.open()
        products_list_page.wait_for_opened()
        products_list_page.expect_error_toast()
```

> **Note:** `expect_empty_state()`, `expect_row_count()`, and `expect_error_toast()` are new
> methods to add to `ProductsListPage`. Add them using Playwright `expect()` assertions
> against existing locators in the page.

#### `tests/ui/integration/test_customers_list.py`

Follow the exact same pattern as `test_products_list.py`, replacing the `mock` call with
`mock.get_customers_list(...)` and the page object with `CustomersListPage`.

### Acceptance Criteria

- [ ] `pytest tests/ui/integration/ -v` collects 9+ tests (3 existing + 6 new).
- [ ] All new tests pass when a mock response is supplied.
- [ ] `ruff check` and `mypy --strict` pass.

---

## STEP 16 — Make Pydantic Response Model Fields Explicitly Required

### Problem

Response models use `default=""` and `default_factory=list` for fields that should always
be present in the API response. Missing fields silently produce empty strings/lists
instead of raising a `ValidationError`, masking API contract regressions.

### Files to Modify

#### `src/sales_portal_tests/data/models/order.py`
#### `src/sales_portal_tests/data/models/product.py`
#### `src/sales_portal_tests/data/models/customer.py`

**Step 16.1 — Find all `default=""` patterns**
```bash
grep -rn 'default=""' src/sales_portal_tests/data/models/
```

**Step 16.2 — For fields that are always returned by the API, remove the default**
```python
# BEFORE
created_on: str = Field(alias="createdOn", default="")

# AFTER
created_on: str = Field(alias="createdOn")
```

**Step 16.3 — For fields that are genuinely optional (nullable in the API), use `None`**
```python
# BEFORE
delivery_date: str = Field(alias="deliveryDate", default="")

# AFTER
delivery_date: str | None = Field(alias="deliveryDate", default=None)
```

**Step 16.4 — Run API smoke tests to find fields that are actually missing**
```bash
pytest tests/api/ -m smoke -x
```
For each `ValidationError`, determine whether the field is truly optional in the API
contract. If optional → use `None` default. If required → investigate the API response.

### Acceptance Criteria

- [ ] `grep -rn 'default=""' src/sales_portal_tests/data/models/` returns zero matches.
- [ ] `pytest tests/ -m regression` passes with no `ValidationError`.
- [ ] `mypy --strict src/` passes.

---

## Implementation Order & Dependencies

```
STEP 1  ──────────────────────────────────────► (independent, do first)
STEP 2  ──────────────────────────────────────► (independent, do first)
STEP 3  ──────────────────────────────────────► (independent)
STEP 4  ──────────────────────────────────────► (independent, but superseded by STEP 5)
STEP 5  ── depends on STEP 3 (uses TokenProvider) + supersedes STEP 4
STEP 6  ──────────────────────────────────────► (independent)
STEP 7  ──────────────────────────────────────► (independent)
STEP 8  ──────────────────────────────────────► (independent)
STEP 9  ──────────────────────────────────────► (independent)
STEP 10 ──────────────────────────────────────► (independent)
STEP 11 ──────────────────────────────────────► (independent)
STEP 12 ── depends on STEP 5 (parallel safety requires decoupled store)
STEP 13 ──────────────────────────────────────► (independent)
STEP 14 ──────────────────────────────────────► (independent)
STEP 15 ──────────────────────────────────────► (independent, needs mock helpers)
STEP 16 ──────────────────────────────────────► (independent, run tests to detect)
```

**Recommended execution order:**

1. STEP 11 (remove dead code — trivial)
2. STEP 1 (auth headers — simple DRY fix)
3. STEP 2 (delivery helper — simple DRY fix)
4. STEP 8 (Faker seed — simple, no breaking changes)
5. STEP 10 (integration conftest — small addition)
6. STEP 9 (remove hard assert — small change)
7. STEP 6 (JsonResponse alias — medium scope refactor)
8. STEP 7 (HTTP retry — medium scope, self-contained)
9. STEP 13 (coverage reporting — independent tool config)
10. STEP 16 (tighten Pydantic models — audit-driven)
11. STEP 3 (TokenProvider — prerequisite for STEP 5)
12. STEP 5 (decouple EntitiesStore — largest change, most impactful)
13. STEP 12 (parallel CI target — validation of STEP 5)
14. STEP 14 (Docker Compose in CI — requires CI environment test)
15. STEP 15 (expand integration tests — new test writing)

> **After each step:** Run `ruff check src/ tests/`, `mypy --strict src/ tests/`,
> and `pytest tests/ -x --timeout=120` to verify nothing is broken.
