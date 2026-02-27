# Implementation Plan — Python + pytest + Playwright

> **Reference:** [`STACK_PYTHON.md`](./STACK_PYTHON.md) (full architecture & library spec)  
> **Original TS project:** [`STACK.md`](./STACK.md)  
> **Approach:** Bottom-up, layer by layer — infrastructure first, then data, API, UI, tests last
>
> ### Key Pythonic Principles Applied
>
> - **Proper `src` layout** — code lives in `src/sales_portal_tests/` (a real installable package), imported as `from sales_portal_tests.config import ...` (no `src.` prefix in imports)
> - **No `I`-prefix on Protocols** — Python uses `ApiClient` (Protocol) / `PlaywrightApiClient` (implementation), not `IApiClient`
> - **Modules over static-method classes** — endpoint paths are module-level constants/functions, not Java-style `ApiConfig.Endpoints.xxx`
> - **`conftest.py` IS the fixture system** — pytest discovers fixtures via the `conftest.py` hierarchy automatically; there is no `mergeTests()` equivalent and none is needed
> - **Use `@allure.step()` directly** — it already works as a method/function decorator in Python; no custom `@log_step` wrapper needed
> - **Stdlib first** — `urllib.parse.urlencode()` instead of a custom query-param builder; `datetime.strftime()` instead of moment.js; `csv` module instead of a custom parser
> - **`pytest.param(..., id="name")` for DDT** — not the `ids=` kwarg; keeps test ID next to its data
> - **Plain data containers** — `EntitiesStore` exposes `set` attributes directly (`store.orders.add(id)`), not Java-style `trackOrders()` / `getOrderIds()`

---

## Project decisions (documented upfront)

### Decision 1 — Sync Playwright API (default)

This implementation uses Playwright **sync** API (`playwright.sync_api`) as the default.

- **Why:** it keeps tests and Page Objects simpler/shorter, fits pytest’s fixture model naturally, and matches the “imperative” style of the current TypeScript project.
- **When to reconsider async:** only if you truly need high-concurrency IO (e.g., heavy API-only suites) _and_ you’re ready to adopt `pytest-asyncio` and async-POM patterns end-to-end.

### Decision 2 — Hybrid response validation (Option C)

We use a **hybrid** validation approach:

- **Contract-level checks:** use **JSON Schema** (`jsonschema`) via `validate_response(..., schema=...)`.
- **Flow/business checks:** use **Pydantic** models for parsing/normalizing data inside services/facades.

Rules to avoid “double validation confusion”:

1. A test should normally choose **either** schema-validation **or** strict Pydantic parsing as its primary shape assertion.
2. If you do both for a critical endpoint, do it deliberately and document it in the test name/Allure description.
3. Prefer schema validation for endpoints where you only need “required fields exist”, and Pydantic for endpoints where you want typed consumption.

---

## Table of Contents

- [Phase 1 — Project Skeleton & Tooling](#phase-1--project-skeleton--tooling)
- [Phase 2 — Configuration & Environment](#phase-2--configuration--environment)
- [Phase 3 — Data Layer (Models, Enums, Schemas)](#phase-3--data-layer-models-enums-schemas)
- [Phase 4 — Utility Layer](#phase-4--utility-layer)
- [Phase 5 — API Client Abstraction](#phase-5--api-client-abstraction)
- [Phase 6 — API Endpoint Wrappers](#phase-6--api-endpoint-wrappers)
- [Phase 7 — API Services & Facades](#phase-7--api-services--facades)
- [Phase 8 — Root Fixtures (API)](#phase-8--root-fixtures-api)
- [Phase 9 — First API Tests (Login + Products)](#phase-9--first-api-tests-login--products)
- [Phase 10 — Remaining API Tests](#phase-10--remaining-api-tests)
- [Phase 11 — UI Page Objects (Base Layer)](#phase-11--ui-page-objects-base-layer)
- [Phase 12 — UI Page Objects (Domain Pages)](#phase-12--ui-page-objects-domain-pages)
- [Phase 13 — UI Services](#phase-13--ui-services)
- [Phase 14 — Mock Layer](#phase-14--mock-layer)
- [Phase 15 — UI Fixtures & Auth Setup](#phase-15--ui-fixtures--auth-setup)
- [Phase 16 — UI Tests](#phase-16--ui-tests)
- [Phase 17 — Integration Tests (Mock-based)](#phase-17--integration-tests-mock-based)
- [Phase 18 — Reporting & Notifications](#phase-18--reporting--notifications)
- [Phase 19 — CI/CD Pipelines](#phase-19--cicd-pipelines)
- [Phase 20 — Final Polish & Documentation](#phase-20--final-polish--documentation)

---

## Phase 1 — Project Skeleton & Tooling

**Goal:** Empty project with all tooling configured; `pytest --collect-only` and `mypy` pass.

### Step 1.1 — Initialise repository & Python environment

```bash
mkdir sales-portal-tests-python && cd sales-portal-tests-python
git init

# Install uv (pick one):
#   https://docs.astral.sh/uv/
#
# Create a project venv managed by uv
uv venv --python 3.12
source .venv/bin/activate
```

### Step 1.2 — Create `pyproject.toml`

Define project metadata, all dependencies, and tool configurations in one file:

```toml
[project]
name = "sales-portal-tests"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = [
    "playwright>=1.49",
    "pytest>=8.0",
    "pytest-playwright>=0.6",
    "pytest-check>=2.3",
    "allure-pytest>=2.13",
    "allure-python-commons>=2.13",
    "faker>=33.0",
    "jsonschema>=4.23",
    "pydantic>=2.10",
    "python-dotenv>=1.1",
    "python-telegram-bot>=21.0",
    "pymongo>=4.10",
    "pytest-xdist>=3.5",
    "pytest-rerunfailures>=14.0",
    "pytest-timeout>=2.3",
]
# NOTE: No `requests` — Playwright's APIRequestContext handles all HTTP calls.

[project.optional-dependencies]
dev = [
    "ruff>=0.8",
    "mypy>=1.14",
    "pre-commit>=4.0",
    "pytest-html>=4.1",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "smoke: critical-path tests",
    "regression: full regression suite",
    "integration: UI + mock integration tests",
    "api: API-only tests",
    "ui: UI-only tests",
    "e2e: end-to-end tests",
    "products", "customers", "orders", "managers",
]
addopts = "--strict-markers --tb=short -v"

# Centralized timeouts/retries defaults (override per-suite via CLI if needed)
timeout = 60
timeout_method = "thread"
reruns = 1
reruns_delay = 2

[tool.mypy]
strict = true
python_version = "3.12"
plugins = ["pydantic.mypy"]
exclude = [".venv"]

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "SIM", "RUF"]
```

### Step 1.3 — Install dependencies

```bash
uv sync --all-extras
playwright install --with-deps chromium
```

### Step 1.4 — Create initial directory structure

Create all `__init__.py` files and empty directories.  
**Important:** The package lives in `src/sales_portal_tests/` so that installing the project (via `uv sync` / editable mode) makes it importable as `from sales_portal_tests.config import ...` (never `from src. ...`).

```
src/
└── sales_portal_tests/
    ├── __init__.py
    ├── config/          __init__.py
    ├── api/
    │   ├── __init__.py
    │   ├── api_clients/ __init__.py
    │   ├── api/         __init__.py
    │   ├── service/     __init__.py
    │   │   └── stores/  __init__.py
    │   └── facades/     __init__.py
    ├── ui/
    │   ├── __init__.py
    │   ├── pages/       __init__.py
    │   │   ├── login/   __init__.py
    │   │   ├── products/ __init__.py
    │   │   ├── customers/ __init__.py
    │   │   └── orders/  __init__.py
    │   └── service/     __init__.py
    ├── mock/            __init__.py
    ├── data/
    │   ├── __init__.py
    │   ├── models/      __init__.py
    │   ├── schemas/     __init__.py
    │   │   ├── products/ customers/ orders/ delivery/ login/ users/
    │   └── sales_portal/ __init__.py
    │       ├── products/ __init__.py
    │       ├── customers/ __init__.py
    │       └── orders/  __init__.py
    └── utils/
        ├── __init__.py
        ├── validation/  __init__.py
        ├── notifications/ __init__.py
        ├── assertions/  __init__.py
        ├── files/       __init__.py
        └── orders/      __init__.py

tests/
├── conftest.py          (empty for now)
├── api/
│   ├── conftest.py
│   ├── products/
│   ├── customers/
│   └── orders/
└── ui/
    ├── conftest.py
    ├── orders/
    └── integration/
```

### Step 1.5 — Configure `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.10]
```

```bash
pre-commit install
```

### Step 1.6 — Create `.gitignore`

```
.venv/
__pycache__/
*.pyc
.mypy_cache/
.pytest_cache/
allure-results/
allure-report/
test-results/
playwright-report/
src/.auth/
.env
.env.dev
dist/
*.egg-info/
```

### Step 1.7 — Verification checkpoint

```bash
pytest --collect-only      # should find 0 tests, no errors
mypy src/ tests/           # should pass (empty modules)
ruff check src/ tests/     # should pass
python -c "import sales_portal_tests"  # package is importable
```

---

## Phase 2 — Configuration & Environment

**Goal:** `.env` loading, env variables exported, API config centralised.

### Step 2.1 — Create `.env` template

```
# .env
SALES_PORTAL_URL=https://...
SALES_PORTAL_API_URL=https://...
USER_NAME=admin@example.com
USER_PASSWORD=secret
MANAGER_IDS=["id1","id2"]
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

### Step 2.2 — `src/sales_portal_tests/config/env.py`

- Load `.env` or `.env.dev` based on `TEST_ENV` environment variable.
- Export module-level constants: `SALES_PORTAL_URL`, `SALES_PORTAL_API_URL`, `CREDENTIALS` (a `Credentials` dataclass), `MANAGER_IDS` (list).
- Use `python-dotenv`'s `load_dotenv()`.

### Step 2.3 — `src/sales_portal_tests/config/api_config.py`

Use **module-level constants and plain functions** — not a class with static methods:

```python
# api_config.py
BASE_URL = SALES_PORTAL_API_URL

# Static endpoints (module constants)
LOGIN = f"{BASE_URL}/api/login"
PRODUCTS = f"{BASE_URL}/api/products"
CUSTOMERS = f"{BASE_URL}/api/customers"
ORDERS = f"{BASE_URL}/api/orders"
NOTIFICATIONS = f"{BASE_URL}/api/notifications"
METRICS = f"{BASE_URL}/api/metrics"
USERS = f"{BASE_URL}/api/users"

# Parameterised endpoints (plain functions)
def product_by_id(product_id: str) -> str:
    return f"{PRODUCTS}/{product_id}"

def customer_by_id(customer_id: str) -> str:
    return f"{CUSTOMERS}/{customer_id}"

def order_by_id(order_id: str) -> str:
    return f"{ORDERS}/{order_id}"

# ... delivery, status, comments, etc.
```

Cover all endpoints: login, products, customers, orders (CRUD + delivery + status + receive + comments + assign-manager), notifications, metrics, users.

### Step 2.4 — Verification checkpoint

```bash
python -c "from sales_portal_tests.config.env import SALES_PORTAL_URL; print(SALES_PORTAL_URL)"
python -c "from sales_portal_tests.config.api_config import product_by_id; print(product_by_id('123'))"
mypy src/
```

---

## Phase 3 — Data Layer (Models, Enums, Schemas)

**Goal:** All type models, enums, JSON schemas, and DDT case structures ready.

### Step 3.1 — Enums & Constants

Create the following in `src/sales_portal_tests/data/`:

| File              | Contents                                                                                                                                    | TS Equivalent    |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| `status_codes.py` | `StatusCodes(IntEnum)` — OK=200, CREATED=201, DELETED=204, BAD_REQUEST=400, UNAUTHORIZED=401, NOT_FOUND=404, CONFLICT=409, SERVER_ERROR=500 | `statusCodes.ts` |
| `tags.py`         | Constants or `StrEnum` for marker names (SMOKE, REGRESSION, etc.)                                                                           | `tags.ts`        |

Create in `src/sales_portal_tests/data/sales_portal/`:

| File                        | Contents                                                                                                           |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `constants.py`              | Timeout values (`TIMEOUT_10_S = 10_000`, `TIMEOUT_30_S = 30_000`)                                                  |
| `country.py`                | `Country(StrEnum)` with all supported countries                                                                    |
| `errors.py`                 | `ResponseErrors` class with error message constants                                                                |
| `order_status.py`           | `OrderStatus(StrEnum)` — Draft, InProcess, Processing, etc.                                                        |
| `delivery_status.py`        | `DeliveryCondition(StrEnum)`, `DeliveryLocation(StrEnum)`, `IDeliveryAddress` dataclass, `IDeliveryInfo` dataclass |
| `notifications.py`          | Modal copy data (titles, messages, button text)                                                                    |
| `products/manufacturers.py` | `Manufacturers(StrEnum)`                                                                                           |

### Step 3.2 — Pydantic / Dataclass Models (`src/sales_portal_tests/data/models/`)

Create one module per domain entity. Use **pydantic `BaseModel`** for API request/response bodies (runtime validation + serialisation) and **`@dataclass`** for lightweight internal data (DDT cases, config):

| File               | Models                                                                                                                                                               |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `core.py`          | `RequestOptions` (dataclass), `Response[T]` (generic dataclass), `ResponseFields` (dataclass), `CaseApi` (dataclass: title, expected_status, expected_error_message) |
| `credentials.py`   | `Credentials` (dataclass: username, password)                                                                                                                        |
| `product.py`       | `Product`, `ProductFromResponse`, `ProductResponse`, `ProductsResponse`, `OrderProductFromResponse`                                                                  |
| `customer.py`      | `Customer`, `CustomerFromResponse`, `CustomerResponse`, `CustomersResponse`, `CustomerListResponse`                                                                  |
| `order.py`         | `OrderCreateBody`, `OrderUpdateBody`, `OrderFromResponse`, `OrderResponse`, `OrdersResponse`                                                                         |
| `delivery.py`      | `DeliveryCase`, delivery UI case models                                                                                                                              |
| `metrics.py`       | `ResponseMetrics`                                                                                                                                                    |
| `notifications.py` | `NotificationsResponse`                                                                                                                                              |
| `user.py`          | `User` model                                                                                                                                                         |

### Step 3.3 — JSON Schemas (`src/sales_portal_tests/data/schemas/`)

Create schema dicts (Python dicts matching JSON Schema spec):

| Directory        | Schemas                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------ |
| `core_schema.py` | `OBLIGATORY_FIELDS_SCHEMA`, `OBLIGATORY_REQUIRED_FIELDS`                                                     |
| `products/`      | `create_schema`, `get_schema`, `get_all_products_schema`, `product_schema`                                   |
| `customers/`     | `create_schema`, `get_by_id_schema`, `get_list_schema`, `get_all_schema`, `update_schema`, `customer_schema` |
| `orders/`        | `create_schema`, `get_schema`, `get_all_orders_schema`, `order_schema`                                       |
| `delivery/`      | `delivery_schema`                                                                                            |
| `login/`         | `login_schema`                                                                                               |
| `users/`         | `user_schema`                                                                                                |

### Step 3.4 — Data Generators (`src/sales_portal_tests/data/sales_portal/`)

| File                                  | Function                                                   | Uses                                                |
| ------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| `products/generate_product_data.py`   | `generate_product_data(**overrides)` → `Product`           | `faker`, `Manufacturers` enum                       |
| `products/generate_product_data.py`   | `generate_product_response_data()` → `ProductFromResponse` | + `bson.ObjectId`                                   |
| `customers/generate_customer_data.py` | `generate_customer_data(**overrides)` → `Customer`         | `faker`, `Country` enum                             |
| `orders/generate_delivery_data.py`    | `generate_delivery(**overrides)` → `DeliveryInfo`          | `faker`, `Country`, `DeliveryCondition`, `datetime` |
| `orders/generate_order_data.py`       | `generate_order_data()`                                    | Composes IDs                                        |

### Step 3.5 — DDT Case Tables (`src/sales_portal_tests/data/sales_portal/`)

Create positive and negative case lists per domain. Use `pytest.param()` with explicit `id` for each case — this keeps the test ID right next to its data:

```python
# Example: src/sales_portal_tests/data/sales_portal/orders/create_delivery_ddt.py
from dataclasses import dataclass
import pytest

@dataclass
class DeliveryCase:
    title: str
    delivery: dict
    expected_status: int
    expected_error: str | None = None

CREATE_DELIVERY_POSITIVE_CASES = [
    pytest.param(
        DeliveryCase(title="Standard delivery", delivery={...}, expected_status=200),
        id="standard-delivery",
    ),
    pytest.param(
        DeliveryCase(title="Express delivery", delivery={...}, expected_status=200),
        id="express-delivery",
    ),
]
```

| File                                        | Exports                                                            |
| ------------------------------------------- | ------------------------------------------------------------------ |
| `products/create_product_test_data.py`      | `CREATE_PRODUCT_POSITIVE_CASES`, `CREATE_PRODUCT_NEGATIVE_CASES`   |
| `products/update_product_test_data.py`      | `UPDATE_PRODUCT_POSITIVE_CASES`, `UPDATE_PRODUCT_NEGATIVE_CASES`   |
| `products/delete_product_test_data.py`      | `DELETE_PRODUCT_*_CASES`                                           |
| `products/get_product_by_id_test_data.py`   | `GET_PRODUCT_*_CASES`                                              |
| `products/get_all_products_test_data.py`    | `GET_ALL_PRODUCTS_*_CASES`                                         |
| `customers/create_customer_test_data.py`    | `CREATE_CUSTOMER_*_CASES`                                          |
| `customers/update_customer_test_data.py`    | `UPDATE_CUSTOMER_*_CASES`                                          |
| `customers/get_by_id_customer_test_data.py` | `GET_BY_ID_*_CASES`                                                |
| `orders/create_order_test_data.py`          | `CREATE_ORDER_*_CASES`                                             |
| `orders/create_delivery_ddt.py`             | `CREATE_DELIVERY_POSITIVE_CASES`, `CREATE_DELIVERY_NEGATIVE_CASES` |
| `orders/orders_status_ddt.py`               | `ORDERS_STATUS_*_CASES`                                            |
| `orders/receive_ddt.py`                     | `RECEIVE_*_CASES`                                                  |
| `orders/assign_manager_ddt.py`              | `ASSIGN_MANAGER_*_CASES`                                           |
| `orders/comment_order_test_data.py`         | Comment cases                                                      |
| `orders/notifications_test_data.py`         | Notification cases                                                 |
| `orders/update_order_test_data.py`          | `UPDATE_ORDER_*_CASES`                                             |
| `orders/get_order_by_id_test_data.py`       | `GET_ORDER_*_CASES`                                                |

### Step 3.6 — Verification checkpoint

```bash
mypy src/data/
python -c "from sales_portal_tests.data.sales_portal.products.generate_product_data import generate_product_data; print(generate_product_data())"
```

---

## Phase 4 — Utility Layer

**Goal:** All helper utilities ready for use by API/UI layers.

### Step 4.1 — Validation utilities (`src/sales_portal_tests/utils/validation/`)

| File                   | Function                                                                       | Details                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| `validate_schema.py`   | `validate_json_schema(body: dict, schema: dict)`                               | Uses `jsonschema.validate()`; logs result; soft-assert on failure                        |
| `validate_response.py` | `validate_response(response, *, status, is_success?, error_message?, schema?)` | Asserts status, IsSuccess, ErrorMessage; calls `validate_json_schema` if schema provided |

**Hybrid validation rule (Decision 2):**

- Use `validate_response(..., schema=...)` when the **schema is the test assertion** (contract checks).
- Use Pydantic parsing (`Model.model_validate(...)`) when you need **typed data to drive a flow**.
- Avoid validating the same payload both ways in the same test unless there’s a strong reason.

### Step 4.2 — Assertions (soft checks)

TypeScript uses `expect.soft()` for “continue collecting failures”. In pytest, add **`pytest-check`**.

- Prefer `check.equal(a, b)` / `check.is_true(...)` for soft assertions.
- Keep a small number of hard assertions (`assert ...`) for “stop the test immediately” invariants (e.g., login token must exist).

Create a tiny helper module (optional) under `src/sales_portal_tests/utils/assertions/` only if you want naming consistency; otherwise, import directly:

- `from pytest_check import check`

### Step 4.2 — Reporting

> **No custom `@log_step` decorator needed.** In Python, `@allure.step("description")` already works as both a method decorator and a context manager (`with allure.step("…"):`). Use it directly on service/page-object methods — no wrapper layer.

### Step 4.2.1 — Allure attachment conventions (recommended)

To keep reports consistent and searchable, standardize attachment names and formats:

- **API request**: `"request.json"` (or `"request (POST /api/orders).json"`)
- **API response**: `"response.json"` + include status code in the step title
- **UI artifacts**:
  - screenshot: `"screenshot.png"`
  - page HTML (on failure): `"page.html"`
  - Playwright trace: link or attach path depending on how you run

Security convention:

- Always run payloads through `mask_secrets()` before attaching (passwords, Authorization headers, refresh tokens).

### Step 4.3 — Other utilities (`src/sales_portal_tests/utils/`)

| File                               | Function                                                                                                                                                  |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `date_utils.py`                    | `convert_to_date(value)`, `convert_to_date_and_time(value)`, `convert_to_full_date_and_time(value)` — **stdlib `datetime.strftime()` only**, no 3rd-party |
| `enum_utils.py`                    | `get_random_enum_value(enum_cls)` using `random.choice(list(enum_cls))`                                                                                   |
| `mask_secrets.py`                  | `mask_secrets(data: str) -> str` — module-level function using `re.sub()` to redact password/authorization tokens                                         |
| `log_utils.py`                     | `log(message: str)` — conditional `print()` based on `TEST_ENV`                                                                                           |
| `files/csv_utils.py`               | `parse_csv_to_records(text: str) -> list[dict]` — **stdlib `csv.DictReader`**, no custom parser                                                           |
| `files/export_file_utils.py`       | `save_download(download, tmp_path)`, `parse_downloaded_export(download, tmp_path)`                                                                        |
| `assertions/confirmation_modal.py` | `assert_confirmation_modal(modal, copy)` — reusable assertion helper                                                                                      |
| `orders/helpers.py`                | Order-specific helper functions                                                                                                                           |

> **No `query_params.py`** — use `urllib.parse.urlencode(params)` from the stdlib inline where needed.

### Step 4.4 — Notification utilities (`src/sales_portal_tests/utils/notifications/`)

| File                      | Details                                                                   |
| ------------------------- | ------------------------------------------------------------------------- |
| `notification_service.py` | `NotificationService` Protocol with `post_notification(text: str)` method |
| `telegram_service.py`     | `TelegramService` implementing the protocol via `python-telegram-bot`     |

### Step 4.5 — Verification checkpoint

```bash
mypy src/
python -c "from sales_portal_tests.utils.validation.validate_schema import validate_json_schema; print('OK')"
python -c "from sales_portal_tests.utils.date_utils import convert_to_date; print(convert_to_date('2025-12-31'))"
```

---

## Phase 5 — API Client Abstraction

**Goal:** Abstract HTTP client + Playwright concrete implementation with Allure attachments.

### Step 5.1 — Protocol (`src/sales_portal_tests/api/api_clients/types.py`)

Define `ApiClient` as a `typing.Protocol` — **no `I` prefix** (Python convention):

```python
from typing import Protocol

class ApiClient(Protocol):
    def send(self, options: RequestOptions) -> Response: ...
```

### Step 5.2 — Base client (`src/sales_portal_tests/api/api_clients/base_api_client.py`)

Abstract base class (`ABC`):

- Abstract method: `send(options: RequestOptions) -> Response`
- Abstract method: `_transform_response(raw_response) -> Response`

### Step 5.3 — Playwright client (`src/sales_portal_tests/api/api_clients/playwright_api_client.py`)

Concrete implementation:

- Constructor takes `APIRequestContext`.
- `send()`:
  1. Calls `self._api_context.fetch(url, **options)`.
  2. Calls `_transform_response()` to extract status, body, headers.
  3. Attaches request JSON to Allure step (`allure.attach()`).
  4. Attaches response JSON to Allure step.
  5. Masks secrets in attachments.
  6. Returns typed `Response` object.

### Step 5.4 — Verification checkpoint

```bash
mypy src/api/api_clients/
```

---

## Phase 6 — API Endpoint Wrappers

**Goal:** One class per domain entity covering all endpoints.

### Step 6.1 — `src/sales_portal_tests/api/api/login_api.py`

- `LoginApi.__init__(self, client: ApiClient)`
- `@allure.step("POST /api/login")`
- `login(credentials: Credentials) -> Response[LoginResponse]`

### Step 6.2 — `src/sales_portal_tests/api/api/products_api.py`

- `ProductsApi.__init__(self, client: ApiClient)`
- Methods (all with `@allure.step`):
  - `create(product: Product, token: str) -> Response[ProductResponse]`
  - `update(id: str, product: Product, token: str) -> Response[ProductResponse]`
  - `get_by_id(id: str, token: str) -> Response[ProductResponse]`
  - `get_all(token: str) -> Response[ProductsResponse]`
  - `delete(id: str, token: str) -> Response[None]`

### Step 6.3 — `src/sales_portal_tests/api/api/customers_api.py`

- `CustomersApi.__init__(self, client: ApiClient)`
- Methods: `create`, `delete`, `get_list`, `get_all`, `get_by_id`, `update`

### Step 6.4 — `src/sales_portal_tests/api/api/orders_api.py`

- `OrdersApi.__init__(self, client: ApiClient)`
- Methods: `create`, `get_by_id`, `get_all`, `update`, `delete`, `add_delivery`, `update_status`, `receive_products`, `assign_manager`, `unassign_manager`, `add_comment`, `get_comments`, `delete_comment`

### Step 6.5 — `src/sales_portal_tests/api/api/notifications_api.py`

- `NotificationsApi.__init__(self, client: ApiClient)`
- Methods: `get_user_notifications`, `mark_as_read`, `mark_all_as_read`

### Step 6.6 — Verification checkpoint

```bash
mypy src/api/api/
```

---

## Phase 7 — API Services & Facades

**Goal:** Business-level flows with built-in validation and cleanup tracking.

### Step 7.1 — `EntitiesStore` (`src/sales_portal_tests/api/service/stores/entities_store.py`)

A plain data container — **expose `set` attributes directly**, no Java-style getter/setter methods:

```python
@dataclass
class EntitiesStore:
    orders: set[str] = field(default_factory=set)
    customers: set[str] = field(default_factory=set)
    products: set[str] = field(default_factory=set)

    def clear(self) -> None:
        self.orders.clear()
        self.customers.clear()
        self.products.clear()
```

Usage: `store.orders.add(order_id)` — not `store.track_orders(order_id)`.

### Step 7.2 — `LoginService` (`src/sales_portal_tests/api/service/login_service.py`)

- `login_as_admin(credentials=None) -> str` (returns token)
- Calls `login_api.login()`, validates response, extracts `authorization` header.

### Step 7.3 — `ProductsApiService` (`src/sales_portal_tests/api/service/products_service.py`)

- Methods: `create()`, `update()`, `delete()`, `delete_products()`, `delete_all_products()`, `bulk_create()`
- Each method calls the corresponding API wrapper + `validate_response()`.

### Step 7.4 — `CustomersApiService` (`src/sales_portal_tests/api/service/customers_service.py`)

- Methods: `create()`, `delete()`, `get_by_id()`, `get_all()`, `get_list()`, `update()`
- Same pattern: API call + validate.

### Step 7.5 — `OrdersApiService` (`src/sales_portal_tests/api/service/orders_service.py`)

- Constructor takes: `OrdersApi`, `ProductsApiService`, `CustomersApiService`, `EntitiesStore`
- Key methods:
  - `create(token, customer_id, product_ids)` — simple order creation
  - `create_order_and_entities(token, num_products)` — creates customer + products + order; tracks in store
  - `create_order_with_delivery(token, num_products)` — above + adds delivery
  - Status transition methods
  - `full_delete(token)` — deletes orders → products → customers from store
- All methods decorated with `@allure.step()`.

### Step 7.6 — `OrdersFacadeService` (`src/sales_portal_tests/api/facades/orders_facade_service.py`)

- Composes: `OrdersApi`, `CustomersApiService`, `ProductsApiService`
- Methods: `create()`, `create_order_with_delivery()`, `create_order_in_process()`, `create_canceled_order()`, `create_partially_received_order()`, `create_received_order()`
- Returns raw responses (no internal validation).

### Step 7.7 — Verification checkpoint

```bash
mypy src/api/service/ src/api/facades/
```

---

## Phase 8 — Root Fixtures (API)

**Goal:** All API fixtures wired up in `conftest.py`; cleanup auto-teardown works.

> **Key concept:** In pytest, `conftest.py` **IS** the fixture/plugin system. Fixtures defined in `conftest.py` are auto-discovered by all tests in that directory and below. There is no `mergeTests()` or manual fixture-file imports — just place fixtures at the right level:
>
> - `tests/conftest.py` → available to ALL tests (session-scoped infra)
> - `tests/api/conftest.py` → available to API tests only
> - `tests/ui/conftest.py` → available to UI tests only

### Step 8.1 — `tests/conftest.py` (root)

Session-scoped infrastructure — created once, shared across all tests:

```python
import pytest
from playwright.sync_api import Playwright
from sales_portal_tests.api.api_clients.playwright_api_client import PlaywrightApiClient
from sales_portal_tests.api.api.login_api import LoginApi
from sales_portal_tests.api.service.login_service import LoginService

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    context = playwright.request.new_context()
    yield context
    context.dispose()

@pytest.fixture(scope="session")
def api_client(api_request_context):
    return PlaywrightApiClient(api_request_context)

@pytest.fixture(scope="session")
def login_api(api_client):
    return LoginApi(api_client)

@pytest.fixture(scope="session")
def login_service(login_api):
    return LoginService(login_api)

@pytest.fixture(scope="session")
def admin_token(login_service):
    return login_service.login_as_admin()
```

### Step 8.2 — `tests/api/conftest.py`

API wrappers and services — **also session-scoped** (they are stateless, just hold a reference to the client).  
Only the `cleanup` fixture is function-scoped (per-test teardown):

```python
import pytest
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore

# --- Session-scoped (stateless wrappers) ---

@pytest.fixture(scope="session")
def products_api(api_client):
    return ProductsApi(api_client)

@pytest.fixture(scope="session")
def customers_api(api_client):
    return CustomersApi(api_client)

@pytest.fixture(scope="session")
def orders_api(api_client):
    return OrdersApi(api_client)

@pytest.fixture(scope="session")
def products_service(products_api):
    return ProductsApiService(products_api)

@pytest.fixture(scope="session")
def customers_service(customers_api):
    return CustomersApiService(customers_api)

@pytest.fixture(scope="session")
def orders_service(orders_api, products_service, customers_service):
    return OrdersApiService(orders_api, products_service, customers_service)

# --- Function-scoped (per-test cleanup) ---

@pytest.fixture
def cleanup(orders_service, login_service):
    """Per-test cleanup: yields a fresh store, auto-deletes tracked entities in teardown."""
    store = EntitiesStore()
    orders_service.entities_store = store
    yield store
    token = login_service.login_as_admin()
    orders_service.full_delete(token)
    store.clear()
```

### Step 8.3 — Verification checkpoint

```bash
pytest --collect-only tests/api/   # fixtures should resolve without errors
```

---

## Phase 9 — First API Tests (Login + Products)

**Goal:** First working tests proving the entire API stack works end-to-end.

### Step 9.1 — Login smoke test

`tests/api/test_login.py` (or in `products/` conftest as setup validation):

- Test that `login_service.login_as_admin()` returns a non-empty token.

### Step 9.2 — `tests/api/products/test_create.py`

- Import DDT cases from `sales_portal_tests.data.sales_portal.products.create_product_test_data`.
- `@pytest.mark.parametrize("case", CREATE_PRODUCT_POSITIVE_CASES)` — each case is already a `pytest.param(…, id="name")`, so test IDs appear automatically.
- Positive: create product → `validate_response()` → validate schema.
- Negative: `@pytest.mark.parametrize("case", CREATE_PRODUCT_NEGATIVE_CASES)` → expect error status + error message.
- Use `cleanup` fixture for teardown.

### Step 9.3 — Products: get_by_id, get_all, update, delete

- `test_get_by_id.py` — create product via service → get by id → assert fields match.
- `test_get_all.py` — bulk create → get all → assert count.
- `test_update.py` — create → update → get → assert new fields.
- `test_delete.py` — create → delete → verify 204 → get → verify 404.

### Step 9.4 — Run & verify

```bash
pytest tests/api/products/ -v --alluredir=allure-results
allure serve allure-results   # verify Allure steps & attachments
```

---

## Phase 10 — Remaining API Tests

**Goal:** Full API test coverage matching the TS project.

### Step 10.1 — Customer API tests

| Test file           | Coverage                       |
| ------------------- | ------------------------------ |
| `test_create.py`    | Positive + negative DDT        |
| `test_get_by_id.py` | Get existing + non-existent    |
| `test_get_list.py`  | With query params              |
| `test_get_all.py`   | List all customers             |
| `test_delete.py`    | Delete existing + non-existent |

### Step 10.2 — Order API tests

| Test file                         | Coverage                                                         |
| --------------------------------- | ---------------------------------------------------------------- |
| `test_create.py`                  | Create order positive/negative                                   |
| `test_get_by_id.py`               | Get existing + non-existent                                      |
| `test_update.py`                  | Update order fields                                              |
| `test_delete.py`                  | Delete order                                                     |
| `test_delivery.py`                | Add delivery positive/negative DDT (port `createDeliveryDDT.ts`) |
| `test_orders_status.py`           | Status transitions DDT                                           |
| `test_receive.py`                 | Receive products DDT                                             |
| `test_comment.py`                 | Add/get/delete comments                                          |
| `test_assign_unassign_manager.py` | Assign/unassign manager DDT                                      |
| `test_notifications.py`           | Notifications after order events                                 |

### Step 10.3 — Verification checkpoint

```bash
pytest tests/api/ -v -m "smoke or regression"
# All tests should pass; Allure report should show full step hierarchy
```

---

## Phase 11 — UI Page Objects (Base Layer)

**Goal:** Abstract base classes that all page objects inherit from.

### Step 11.1 — `src/sales_portal_tests/ui/pages/base_page.py`

```python
class BasePage(ABC):
    def __init__(self, page: Page): ...
    def intercept_request(self, url, trigger_action, *args): ...
    def intercept_response(self, url, trigger_action, *args): ...
    def expect_request(self, method, url, query_params, trigger_action, *args): ...
    def get_auth_token(self) -> str: ...       # from cookies
    def get_cookie_by_name(self, name): ...
    def expect_locked(self, input_locator): ...
```

### Step 11.2 — `src/sales_portal_tests/ui/pages/sales_portal_page.py`

```python
class SalesPortalPage(BasePage, ABC):
    @property
    def spinner(self) -> Locator: ...
    @property
    def toast_message(self) -> Locator: ...
    @property
    @abstractmethod
    def unique_element(self) -> Locator: ...

    def wait_for_opened(self): ...
    def wait_for_spinners(self): ...
    def open(self, route: str = ""): ...
```

### Step 11.3 — `src/sales_portal_tests/ui/pages/base_modal.py`

```python
class BaseModal(SalesPortalPage, ABC):
    def wait_for_closed(self): ...
```

### Step 11.4 — Verification checkpoint

```bash
mypy src/ui/pages/base_page.py src/ui/pages/sales_portal_page.py src/ui/pages/base_modal.py
```

---

## Phase 12 — UI Page Objects (Domain Pages)

**Goal:** All concrete page objects matching the TS project.

### Step 12.1 — Common pages

| File                    | Class                                                       |
| ----------------------- | ----------------------------------------------------------- |
| `login/login_page.py`   | `LoginPage` — email input, password input, submit button    |
| `home_page.py`          | `HomePage` — welcome text, module buttons, metrics locators |
| `navbar_component.py`   | `NavBar` — Home, Products, Customers, Orders nav buttons    |
| `confirmation_modal.py` | `ConfirmationModal` — title, message, confirm button        |
| `export_modal.py`       | `ExportModal` — format selection, export button             |

### Step 12.2 — Products pages

| File                               | Class                                                       |
| ---------------------------------- | ----------------------------------------------------------- |
| `products/products_list_page.py`   | `ProductsListPage` — table, search, add button, row actions |
| `products/add_new_product_page.py` | `AddNewProductPage` — form fields, save/back buttons        |
| `products/edit_product_page.py`    | `EditProductPage` — form fields, save button                |
| `products/delete_modal.py`         | `ProductDeleteModal` — confirmation dialog                  |
| `products/details_modal.py`        | `ProductDetailsModal` — read-only fields                    |

### Step 12.3 — Customers pages

| File                                 | Class                  |
| ------------------------------------ | ---------------------- |
| `customers/customers_list_page.py`   | `CustomersListPage`    |
| `customers/add_new_customer_page.py` | `AddNewCustomerPage`   |
| `customers/details_modal.py`         | `CustomerDetailsModal` |

### Step 12.4 — Orders pages

| File                            | Class                                                     |
| ------------------------------- | --------------------------------------------------------- |
| `orders/orders_list_page.py`    | `OrdersListPage`                                          |
| `orders/order_details_page.py`  | `OrderDetailsPage`                                        |
| `orders/create_order_modal.py`  | `CreateOrderModal`                                        |
| `orders/edit_products_modal.py` | `EditProductsModal`                                       |
| `orders/components/*`           | Delivery section, comments section, manager section, etc. |

### Step 12.5 — Verification checkpoint

```bash
mypy src/ui/pages/
```

---

## Phase 13 — UI Services

**Goal:** Higher-level user flows composing page objects.

### Step 13.1 — Create all UI service classes

| File                             | Service                   | Key methods                               |
| -------------------------------- | ------------------------- | ----------------------------------------- |
| `login_ui_service.py`            | `LoginUIService`          | `login(credentials)`                      |
| `home_ui_service.py`             | `HomeUIService`           | `navigate_to(module)`, `verify_metrics()` |
| `add_new_product_ui_service.py`  | `AddNewProductUIService`  | `open()`, `create(product_data)`          |
| `edit_product_ui_service.py`     | `EditProductUIService`    | `open(id)`, `update(new_data)`            |
| `products_list_ui_service.py`    | `ProductsListUIService`   | `search()`, `delete()`, `open_details()`  |
| `add_new_customer_ui_service.py` | `AddNewCustomerUIService` | `open()`, `create(customer_data)`         |
| `customers_list_ui_service.py`   | `CustomersListUIService`  | `search()`, `open_details()`              |
| `order_details_ui_service.py`    | `OrderDetailsUIService`   | `verify_order()`, `update_status()`       |
| `comments_ui_service.py`         | `CommentsUIService`       | `add_comment()`, `delete_comment()`       |
| `assign_manager_ui_service.py`   | `AssignManagerUIService`  | `assign()`, `unassign()`                  |

### Step 13.2 — Verification checkpoint

```bash
mypy src/ui/service/
```

---

## Phase 14 — Mock Layer

**Goal:** Network interception helpers for integration tests.

### Step 14.1 — `src/sales_portal_tests/mock/mock.py`

```python
class Mock:
    def __init__(self, page: Page): ...

    def route_request(self, url, body: dict, status_code: int): ...
    def products_page(self, body, status_code=200): ...
    def product_details_modal(self, body, status_code=200): ...
    def metrics_home_page(self, body, status_code=200): ...
    def orders_page(self, body, status_code=200): ...
    def order_details_modal(self, body, status_code=200): ...
    def create_order_modal(self, body, status_code=201): ...
    def get_customers_all(self, body, status_code=200): ...
    def get_products_all(self, body, status_code=200): ...
    def order_by_id(self, body, order_id, status_code=200): ...
```

### Step 14.2 — Mock test data generators

`src/sales_portal_tests/data/sales_portal/orders/create_order_mock_ddt.py` — mock data cases for integration tests.
`src/sales_portal_tests/data/sales_portal/orders/orders_list_integration_data.py` — mock orders list data.

---

## Phase 15 — UI Fixtures & Auth Setup

**Goal:** All page/service fixtures + authenticated browser context.

### Step 15.1 — `tests/ui/conftest.py`

Use pytest-playwright's built-in `browser_context_args` fixture to inject storage state.  
The `storage_state_path` fixture logs in once per session and saves cookies:

**Storage-state pitfalls (read before implementing):**

- `domain` must be the **hostname only** (no scheme, no port). If `SALES_PORTAL_URL` includes a port, cookie domain rules can bite.
- `path` should almost always be `"/"` unless your app genuinely scopes cookies.
- If the app expects `Authorization` in headers (not cookies), this approach won’t work; you’ll need a real UI login flow once per session.
- If the UI and API live on different subdomains, ensure the cookie is created for the UI domain that the browser will actually visit.

If anything is flaky, prefer the most robust fallback:

- create storage state by **performing the real UI login** once per session, then save `storage_state()`.

```python
from pathlib import Path
from urllib.parse import urlparse

import pytest
from sales_portal_tests.config.env import SALES_PORTAL_URL

AUTH_STATE_PATH = Path("src/.auth/user.json")


@pytest.fixture(scope="session")
def storage_state_path(browser_type_launch_args, admin_token) -> str:
    """Generate authenticated storage state once per session."""
    from playwright.sync_api import sync_playwright

    url = urlparse(SALES_PORTAL_URL)
    with sync_playwright() as p:
        browser = p.chromium.launch(**browser_type_launch_args)
        ctx = browser.new_context()
        ctx.add_cookies([{
            "name": "Authorization",
            "value": admin_token,
            "domain": url.hostname,
            "path": url.path or "/",
        }])
        AUTH_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        ctx.storage_state(path=str(AUTH_STATE_PATH))
        ctx.close()
        browser.close()
    return str(AUTH_STATE_PATH)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, storage_state_path):
    """Override pytest-playwright's built-in fixture to inject auth + viewport."""
    return {
        **browser_context_args,
        "storage_state": storage_state_path,
        "viewport": {"width": 1920, "height": 1080},
    }
```

### Step 15.2 — Page & service fixtures (still in `tests/ui/conftest.py`)

Function-scoped — each test gets fresh page objects tied to its own `page`:

```python
from sales_portal_tests.ui.pages.home_page import HomePage
from sales_portal_tests.ui.pages.products.products_list_page import ProductsListPage
from sales_portal_tests.ui.pages.products.add_new_product_page import AddNewProductPage
from sales_portal_tests.mock.mock import Mock

@pytest.fixture
def home_page(page):
    return HomePage(page)

@pytest.fixture
def products_list_page(page):
    return ProductsListPage(page)

@pytest.fixture
def add_new_product_page(page):
    return AddNewProductPage(page)

# ... all page objects ...

@pytest.fixture
def add_new_product_ui_service(page):
    return AddNewProductUIService(page)

@pytest.fixture
def mock(page):
    return Mock(page)

# ... all UI services ...
```

### Step 15.3 — Cleanup fixture for UI tests (still in `tests/ui/conftest.py`)

Same pattern as API — yield a fresh `EntitiesStore`, auto-delete in teardown:

**Fixture state contract (important):**

- Each test owns its own cleanup store (function-scoped) to prevent cross-test leakage.
- Any UI test that creates entities through API services must ensure teardown runs.
  - In pytest this is implicit if the fixture is used.
  - If you create data “out of band”, wire it through the same fixture to keep cleanup deterministic.

```python
from sales_portal_tests.api.service.stores.entities_store import EntitiesStore

@pytest.fixture
def cleanup(orders_service, login_service):
    store = EntitiesStore()
    orders_service.entities_store = store
    yield store
    token = login_service.login_as_admin()
    orders_service.full_delete(token)
    store.clear()
```

> Note: The `orders_service` and `login_service` fixtures are inherited from `tests/conftest.py` (root) automatically — no import needed.

### Step 15.4 — Verification checkpoint

```bash
pytest --collect-only tests/ui/
```

---

## Phase 16 — UI Tests

**Goal:** Full UI test coverage matching the TS project.

### Step 16.1 — Order UI tests (priority — most numerous)

| Test file                          | Coverage                                  |
| ---------------------------------- | ----------------------------------------- |
| `test_create_order.py`             | Create order via UI, verify response      |
| `test_order_details.py`            | Open order details, verify fields         |
| `test_order_delivery.py`           | Add delivery via UI DDT                   |
| `test_comments.py`                 | Add/delete comments on order              |
| `test_export_orders.py`            | Export orders to CSV/JSON, parse & verify |
| `test_navigation.py`               | Navigate between pages via navbar         |
| `test_assign_manager.py`           | Assign/unassign manager DDT               |
| `test_processing.py`               | Order status transitions via UI           |
| `test_receive_products.py`         | Receive all products                      |
| `test_receive_partial_products.py` | Receive partial products                  |
| `test_refresh_order.py`            | Refresh order details                     |
| `test_requested_products.py`       | Verify requested products display         |
| `test_order_modals.py`             | Confirmation/edit modals behaviour        |
| `test_update_customer.py`          | Update customer from order details        |

### Step 16.2 — Each test pattern

```python
import pytest
from playwright.sync_api import expect

@pytest.mark.ui
@pytest.mark.orders
@pytest.mark.regression
class TestOrderDetails:
    def test_order_details_displayed(self, order_details_page, orders_service, admin_token, cleanup):
        # Arrange: create order via API service
        order = orders_service.create_order_and_entities(admin_token, num_products=2)
        cleanup.orders.add(order.id)

        # Act: open order details page
        order_details_page.open(f"#/orders/{order.id}")
        order_details_page.wait_for_opened()

        # Assert: verify fields using Playwright's expect()
        expect(order_details_page.order_number).to_have_text(str(order.number))
```

### Step 16.3 — Verification checkpoint

```bash
pytest tests/ui/ -v -m smoke --headed   # visual verification
pytest tests/ui/ -v -m regression       # full run
```

---

## Phase 17 — Integration Tests (Mock-based)

**Goal:** UI tests with mocked API responses (no real backend needed).

### Step 17.1 — Integration test files

| File                                           | Coverage                                     |
| ---------------------------------------------- | -------------------------------------------- |
| `tests/ui/integration/test_orders_list.py`     | Mock orders list → verify table rendering    |
| `tests/ui/integration/test_create_order.py`    | Mock customers/products/create → verify flow |
| `tests/ui/integration/test_update_customer.py` | Mock customer data → verify update UI        |

### Step 17.2 — Pattern

```python
@pytest.mark.integration
def test_orders_list_displays_mocked_data(mock, orders_list_page):
    mock.orders_page(body=MOCK_ORDERS_RESPONSE)
    orders_list_page.open("#/orders")
    orders_list_page.wait_for_opened()
    # Assert table rows match mock data
```

---

## Phase 18 — Reporting & Notifications

**Goal:** Allure reports with full step hierarchy, attachments, and Telegram notifications.

### Step 18.1 — Allure environment file

Create a **pytest plugin hook** in `tests/conftest.py` to generate `allure-results/environment.properties`:

```python
def pytest_sessionfinish(session, exitstatus):
    """pytest hook — runs once after the entire test session."""
    import os
    from pathlib import Path
    from sales_portal_tests.config.env import SALES_PORTAL_URL, SALES_PORTAL_API_URL

    allure_dir = Path("allure-results")
    allure_dir.mkdir(exist_ok=True)
    (allure_dir / "environment.properties").write_text(
        f"ENV={os.getenv('TEST_ENV', 'default')}\n"
        f"UI_URL={SALES_PORTAL_URL}\n"
        f"API_URL={SALES_PORTAL_API_URL}\n"
    )
```

### Step 18.2 — Verify Allure step hierarchy

- API requests should show as nested steps with JSON attachments (from `PlaywrightApiClient.send()`).
- Service methods decorated with `@allure.step()` appear as parent steps.
- Page object methods decorated with `@allure.step()` appear as UI steps.
- No custom decorator needed — `@allure.step("description")` is used directly everywhere.

### Step 18.3 — Telegram notification script

Create `scripts/notify_telegram.py` for CI use:

```python
from sales_portal_tests.utils.notifications.telegram_service import TelegramService
service = TelegramService()
service.post_notification("Test run finished! Report: https://...")
```

### Step 18.4 — Verification

```bash
pytest tests/ --alluredir=allure-results -m smoke
allure serve allure-results
# Verify: environment tab, step tree, request/response attachments
```

---

## Phase 19 — CI/CD Pipelines

**Goal:** GitHub Actions workflows for lint + test + deploy.

### Step 19.1 — `.github/workflows/build.yml`

- Trigger: PR to `main`
- Steps: checkout → setup Python 3.12 → `pip install` → `ruff check` → `mypy`

### Step 19.2 — `.github/workflows/tests.yml`

- Trigger: push/PR to `main` + manual dispatch
- Steps:
  1. Checkout
  2. Setup Python 3.12
  3. `pip install -r requirements.txt`
  4. `playwright install --with-deps chromium`
  5. Install OpenJDK 17
  6. Run API regression: `pytest tests/api/ -m "regression or smoke" --alluredir=allure-results`
  7. Run UI regression: `pytest tests/ui/ -m "regression or smoke" --alluredir=allure-results`
  8. Generate Allure report: `allure generate allure-results -o allure-report --clean`
  9. Deploy to GitHub Pages
  10. Telegram notification

### Step 19.3 — Generate `requirements.txt`

```bash
pip freeze > requirements.txt
# or maintain manually with pinned versions
```

### Step 19.4 — Verification

- Push to a branch, open PR → build.yml should pass.
- Merge to main → tests.yml should run tests + deploy report.

---

## Phase 20 — Final Polish & Documentation

### Step 20.1 — README.md

- Project overview
- Prerequisites (Python 3.12+, Playwright browsers)
- Setup instructions (`pip install`, `playwright install`, `.env` config)
- Running tests (commands for API, UI, smoke, regression, parallel)
- Viewing reports (Allure, HTML)
- CI/CD overview
- Architecture overview (link to `STACK_PYTHON.md`)

### Step 20.2 — Copilot instructions

Create `.github/copilot-instructions.md` for the Python project (equivalent of the TS one).

### Step 20.3 — Code review checklist

- [ ] All `mypy --strict` passes with zero errors
- [ ] All `ruff check` passes with zero warnings
- [ ] All API tests pass against live environment
- [ ] All UI tests pass against live environment
- [ ] Integration (mock) tests pass without network
- [ ] Allure report shows correct step hierarchy
- [ ] Cleanup fixture properly deletes all created entities
- [ ] CI pipeline runs end-to-end
- [ ] Telegram notification fires after CI run
- [ ] `.env.dev` alternative env works with `TEST_ENV=dev`

### Step 20.4 — Optional enhancements

- [ ] Configure `pytest-xdist` parallel execution (`-n auto`)
- [ ] Configure `pytest-rerunfailures` retry (`--reruns 2 --reruns-delay 3`)
- [ ] Add `conftest.py` hook for automatic screenshot-on-failure attachment to Allure:
  ```python
  @pytest.hookimpl(hookwrapper=True)
  def pytest_runtest_makereport(item, call):
      outcome = yield
      report = outcome.get_result()
      if report.failed and "page" in item.funcargs:
          page = item.funcargs["page"]
          allure.attach(page.screenshot(), "screenshot", allure.attachment_type.PNG)
  ```
- [ ] Add `pytest-timeout` defaults in `pyproject.toml` (`timeout = 120`)
- [ ] Add `Makefile` with common commands:
  ```makefile
  test-api:
      pytest tests/api/ -m "smoke or regression" --alluredir=allure-results
  test-ui:
      pytest tests/ui/ -m "smoke or regression" --alluredir=allure-results
  lint:
      ruff check src/ tests/ && mypy src/ tests/
  ```

---

## Implementation Timeline (suggested)

| Phase                            | Effort (estimate) | Dependencies |
| -------------------------------- | ----------------- | ------------ |
| **Phase 1** — Project skeleton   | 0.5 day           | —            |
| **Phase 2** — Config & env       | 0.5 day           | Phase 1      |
| **Phase 3** — Data layer         | 2 days            | Phase 2      |
| **Phase 4** — Utilities          | 1 day             | Phase 3      |
| **Phase 5** — API client         | 0.5 day           | Phase 4      |
| **Phase 6** — API wrappers       | 1 day             | Phase 5      |
| **Phase 7** — API services       | 1.5 days          | Phase 6      |
| **Phase 8** — API fixtures       | 0.5 day           | Phase 7      |
| **Phase 9** — First API tests    | 1 day             | Phase 8      |
| **Phase 10** — All API tests     | 2–3 days          | Phase 9      |
| **Phase 11** — UI base pages     | 0.5 day           | Phase 4      |
| **Phase 12** — UI domain pages   | 2 days            | Phase 11     |
| **Phase 13** — UI services       | 1 day             | Phase 12     |
| **Phase 14** — Mock layer        | 0.5 day           | Phase 12     |
| **Phase 15** — UI fixtures       | 0.5 day           | Phase 13, 14 |
| **Phase 16** — UI tests          | 3–4 days          | Phase 15     |
| **Phase 17** — Integration tests | 1 day             | Phase 14, 15 |
| **Phase 18** — Reporting         | 0.5 day           | Phase 10, 16 |
| **Phase 19** — CI/CD             | 0.5 day           | Phase 18     |
| **Phase 20** — Polish & docs     | 0.5 day           | Phase 19     |
| **Total**                        | **~18–21 days**   |              |
