# Copilot Instructions — Sales Portal Python Test Framework

## Big picture

- This repo is a **pytest + Playwright** (sync API) test framework with **API + UI** coverage.
- The main package lives in `src/sales_portal_tests/` and is imported as `from sales_portal_tests.…`.
- Tests live in `tests/` and are split by type: `tests/api/` vs `tests/ui/` (including `tests/ui/integration/`).
- Core layers:
  - **API:**
    - `src/sales_portal_tests/api/api_clients/` — `ApiClient` Protocol + `PlaywrightApiClient` (Playwright `APIRequestContext`)
    - `src/sales_portal_tests/api/api/` — endpoint wrappers (one class per domain: `ProductsApi`, `CustomersApi`, `OrdersApi`, etc.)
    - `src/sales_portal_tests/api/service/` — single-domain business flows (`ProductsApiService`, `OrdersApiService`, etc.)
    - `src/sales_portal_tests/api/facades/` — cross-domain orchestration (`OrdersFacadeService`)
  - **UI:**
    - `src/sales_portal_tests/ui/pages/` — Page Objects (`BasePage` → `SalesPortalPage` → domain pages)
    - `src/sales_portal_tests/ui/service/` — higher-level UI flows (e.g., `AddNewProductUIService`, `OrderDetailsUIService`)
  - **Mock:**
    - `src/sales_portal_tests/mock/` — Playwright route interception helpers
  - **Data:**
    - `src/sales_portal_tests/data/models/` — Pydantic / dataclass models per entity
    - `src/sales_portal_tests/data/schemas/` — JSON Schema dicts for response validation
    - `src/sales_portal_tests/data/sales_portal/` — enums, constants, data generators, DDT case tables
    - `src/sales_portal_tests/data/status_codes.py` — `StatusCodes(IntEnum)`
    - `src/sales_portal_tests/data/tags.py` — test marker/tag constants
  - **Utils:**
    - `src/sales_portal_tests/utils/validation/` — `validate_response()`, `validate_json_schema()`
    - `src/sales_portal_tests/utils/` — dates, enums, masking, logging, file helpers, assertions, notifications

## Golden rules (follow these first)

1. **Use repo fixtures, not ad-hoc clients.** All API clients and services are wired up in `tests/conftest.py` (session-scoped) and `tests/ui/conftest.py` (function-scoped page objects + UI services). Request them by name in test signatures.
2. **Never hardcode URLs, endpoints, timeouts, or status codes:**
   - Endpoints → `sales_portal_tests.config.api_config` (module-level constants and functions)
   - Environment → `sales_portal_tests.config.env` (loads `.env` / `.env.dev`)
   - Status codes → `sales_portal_tests.data.status_codes.StatusCodes`
   - Timeouts/constants → `sales_portal_tests.data.sales_portal.constants`
3. **Use `@allure.step()` directly** — it works as a decorator and context manager in Python. No custom `@log_step` wrapper is needed.
4. **Imports always start with `sales_portal_tests.…`** — never `src.sales_portal_tests.…` (the `src/` layout makes the package importable directly).
5. **Keep lint happy:**
   - `ruff check src/ tests/` must pass (rules: E, F, W, I, UP, B, SIM, RUF; line-length 120).
   - `mypy --strict src/ tests/` must pass (Pydantic plugin enabled, `ignore_missing_imports = true`).
6. **Use `pytest-check` for soft assertions** — `from pytest_check import check` → `check.equal(a, b)`. Reserve hard `assert` for invariants that must stop the test immediately (e.g., token must exist).

## Developer workflows

- **Install deps:** `pip install -r requirements.txt` + `pip install -e .`, then `playwright install --with-deps chromium`.
- **Env files:** Default loads `.env`; set `TEST_ENV=dev` to load `.env.dev`. Required vars are in `config/env.py` (`SALES_PORTAL_URL`, `SALES_PORTAL_API_URL`, `USER_NAME`, `USER_PASSWORD`, `MANAGER_IDS`).
- **Common commands** (see `Makefile`):
  - `make test-api` / `make test-ui` / `make test-smoke` / `make test-all`
  - `make lint` (ruff + mypy)
  - `make report` (generate + open Allure report)

## Fixtures (pytest `conftest.py` hierarchy)

pytest discovers fixtures automatically via `conftest.py` files at each directory level. There is no `mergeTests()` or manual fixture imports.

| Level                  | Scope      | Fixtures provided                                                                                                                                                                        |
| ---------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tests/conftest.py`    | `session`  | `api_client`, `login_api`, `login_service`, `admin_token`, `products_api`, `customers_api`, `orders_api`, `notifications_api`, `products_service`, `customers_service`, `orders_service` |
| `tests/conftest.py`    | `function` | `cleanup` (yields `EntitiesStore`, auto-deletes tracked entities in teardown)                                                                                                            |
| `tests/ui/conftest.py` | `session`  | `storage_state_path`, `browser_context_args` (auth injection + viewport)                                                                                                                 |
| `tests/ui/conftest.py` | `function` | Page objects (`login_page`, `home_page`, `products_list_page`, etc.), UI services (`login_ui_service`, `add_new_product_ui_service`, etc.), `mock`                                       |

### Quick snippet — API test skeleton

```python
"""API tests — POST /api/products (Create Product)."""

import allure
import pytest

from sales_portal_tests.data.status_codes import StatusCodes
from sales_portal_tests.utils.validation.validate_response import validate_response


@allure.suite("API")
@allure.sub_suite("Products")
@pytest.mark.api
@pytest.mark.products
class TestCreateProduct:
    @allure.title("Create product — positive: {case}")
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.parametrize("case", CREATE_PRODUCT_POSITIVE_CASES)
    def test_create_product_positive(
        self,
        case: CreateProductCase,
        products_api: ProductsApi,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        response = products_api.create(case.product_data, admin_token)
        validate_response(response, status=case.expected_status, schema=CREATE_PRODUCT_SCHEMA)
        cleanup.products.add(response.body["Product"]["_id"])
```

### Quick snippet — UI test skeleton

```python
"""UI tests — Create Order via the Create Order modal."""

import allure
import pytest
from playwright.sync_api import expect


@allure.suite("UI")
@allure.sub_suite("Orders")
@pytest.mark.ui
@pytest.mark.orders
class TestCreateOrder:
    @allure.title("Create order with 1 product")
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_create_order(
        self,
        orders_list_page: OrdersListPage,
        customers_service: CustomersApiService,
        products_service: ProductsApiService,
        admin_token: str,
        cleanup: EntitiesStore,
    ) -> None:
        customer = customers_service.create(admin_token)
        cleanup.customers.add(customer.id)

        product = products_service.create(admin_token)
        cleanup.products.add(product.id)

        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()

        create_modal = orders_list_page.click_create_order_button()
        created_order = create_modal.create_order(customer.name, [product.name])
        cleanup.orders.add(created_order.id)
```

### Quick snippet — Integration (mock) test skeleton

```python
"""Integration tests — mock API responses via Playwright route interception."""

import allure
import pytest

from sales_portal_tests.mock.mock import Mock


@allure.suite("UI")
@allure.sub_suite("Integration")
@pytest.mark.integration
class TestMockOrders:
    def test_mock_orders_list(
        self,
        mock: Mock,
        orders_list_page: OrdersListPage,
    ) -> None:
        mock.orders.mock_get_all(orders=[...])
        orders_list_page.open("#/orders")
        orders_list_page.wait_for_opened()
```

## How tests are written here

- **DDT case tables** live in `src/sales_portal_tests/data/sales_portal/<domain>/`. They export `*_POSITIVE_CASES` and `*_NEGATIVE_CASES` lists of `pytest.param(CaseDataclass(...), id="case-name")`.
- **Tagging** uses `@pytest.mark.<marker>` decorators. Available markers are defined in `pyproject.toml` under `[tool.pytest.ini_options].markers`.
- **Allure suites** — use `@allure.suite("API"/"UI")` and `@allure.sub_suite("<Domain>")` on test classes.
- **Test class naming** — `TestCreateProduct`, `TestOrderDelivery`, etc. (noun-based, no `test_` prefix on the class).
- **Test method naming** — `test_create_product_positive`, `test_delete_order_not_found`, etc.

## Validation + schemas

- Use `validate_response()` from `sales_portal_tests.utils.validation.validate_response` to assert status / IsSuccess / ErrorMessage.
- When a JSON schema exists, pass it: `validate_response(response, status=..., schema=SOME_SCHEMA)`.
- Schemas live in `src/sales_portal_tests/data/schemas/` (domain folders: `products/`, `customers/`, `orders/`, `delivery/`, `login/`, `users/`).
- Prefer `StatusCodes.OK`, `StatusCodes.CREATED`, etc. from `data/status_codes.py` — avoid raw numbers like `200`.
- `validate_response()` uses `pytest-check` soft assertions intentionally; don't upgrade to hard assertions unless the test truly must stop immediately.

## Cleanup conventions (important)

- The root `conftest.py` provides a per-test `cleanup` fixture that yields a fresh `EntitiesStore` and auto-deletes all tracked entities in teardown.
- If a UI test creates data via API services, simply request the `cleanup` fixture in the test signature.
- Register entities: `cleanup.products.add(product_id)`, `cleanup.customers.add(customer_id)`, `cleanup.orders.add(order_id)`.
- `OrdersApiService` can also use an internal `EntitiesStore`; keep that pattern (don't replace with globals).

## API architecture (how to add new endpoints)

1. Define/extend endpoint URLs in `src/sales_portal_tests/config/api_config.py` (module-level constants or functions).
2. Add wrapper method in `src/sales_portal_tests/api/api/<domain>_api.py` with `@allure.step()`.
3. Add/extend a domain service in `src/sales_portal_tests/api/service/<domain>_service.py` for multi-step flows.
4. For cross-domain flows, add/extend a facade in `src/sales_portal_tests/api/facades/`.
5. Use `validate_response()` + schemas from `data/schemas/`.
6. Register entities in `cleanup` so teardown stays reliable.

## UI architecture (Page Objects + UI services)

- Page Objects live in `src/sales_portal_tests/ui/pages/`.
  - Inheritance: `BasePage` → `SalesPortalPage` → domain page.
  - `SalesPortalPage` subclasses must define `unique_element`.
- UI flows live in `src/sales_portal_tests/ui/service/`.
- Use `@allure.step("...")` on public methods for Allure reporting.
- Use timeout constants from `data/sales_portal/constants.py` — avoid magic numbers.

### Page Object + UI service checklist

- [ ] Page Objects extend `BasePage` or `SalesPortalPage`.
- [ ] `SalesPortalPage` subclasses define `unique_element`.
- [ ] Public methods use `@allure.step("...")`.
- [ ] Timeouts come from `data/sales_portal/constants.py`.
- [ ] Multi-step UI flows go in `ui/service/`, not in Page Objects.

## Test data patterns

- Typed generators live in `src/sales_portal_tests/data/sales_portal/<domain>/generate_*_data.py` using `faker`.
- DDT tables (`*_POSITIVE_CASES`, `*_NEGATIVE_CASES`) live in the same domain folders and use `pytest.param(..., id="name")`.
- Enums (`Country`, `Manufacturers`, `OrderStatus`, `DeliveryCondition`, etc.) live in `data/sales_portal/`.

## Reporting / notifications

- **Allure** is the primary reporter (configured via `--alluredir=allure-results`).
- The `pytest_sessionfinish` hook writes `environment.properties` to `allure-results/`.
- The `pytest_runtest_makereport` hook auto-attaches screenshots on UI test failure.
- CI sends a Telegram notification via `scripts/notify_telegram.py` using `TelegramService` from `utils/notifications/`.

## Python-specific conventions (different from the TS project)

- **No `I`-prefix on Protocols** — use `ApiClient` (Protocol), not `IApiClient`.
- **Modules over static-method classes** — `api_config.py` has module-level constants/functions, not `ApiConfig.Endpoints.xxx`.
- **`conftest.py` IS the fixture system** — no `mergeTests()` equivalent; fixtures auto-discovered by directory hierarchy.
- **`@allure.step()` directly** — no custom `@log_step` wrapper needed.
- **Stdlib first** — `urllib.parse.urlencode()`, `datetime.strftime()`, `csv.DictReader()` instead of third-party equivalents.
- **`pytest.param(..., id="name")` for DDT** — keeps test ID next to its data.
- **Plain data containers** — `EntitiesStore` exposes `set` attributes directly (`store.orders.add(id)`).
