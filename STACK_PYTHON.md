# Technology Stack & Architecture — Python Implementation

> **Project:** Sales Portal — End-to-end test automation framework (Python re-implementation)  
> **Original (TypeScript):** see [`STACK.md`](./STACK.md)  
> **Dev environment:** [`sales-portal/`](./sales-portal/) (Express + MongoDB backend, vanilla JS frontend, Docker Compose)  
> **Goal:** Reproduce every capability of the TypeScript framework using **Python + pytest + Playwright**

---

## Table of Contents

1. [Overview](#1-overview)
2. [Core Technologies](#2-core-technologies)
3. [Libraries & Dependencies](#3-libraries--dependencies)
4. [Project Architecture](#4-project-architecture)
5. [Layer-by-Layer Breakdown](#5-layer-by-layer-breakdown)
6. [Test Strategy & Patterns](#6-test-strategy--patterns)
7. [Configuration & Environment](#7-configuration--environment)
8. [Linting, Formatting & Git Hooks](#8-linting-formatting--git-hooks)
9. [CI/CD Pipeline](#9-cicd-pipeline)
10. [Reporting & Notifications](#10-reporting--notifications)
11. [Directory Reference](#11-directory-reference)
12. [TypeScript → Python Migration Map](#12-typescript--python-migration-map)

---

## 1. Overview

This project is a **pytest + Playwright for Python** test-automation framework providing both **API** and **UI** test coverage for the Sales Portal product. It preserves the same multi-layered, service-oriented architecture as the original TypeScript project — separating HTTP clients, business-level services, Page Objects, pytest fixtures, data generation, and JSON-schema validation — while leveraging Python-native idioms (dataclasses, type hints, pytest parametrize, context managers).

### Application Under Test

The Sales Portal is a full-stack web application located in the `sales-portal/` directory of this repository. It consists of:

- **Backend:** Express.js + MongoDB (Mongoose), running on port 8686
- **Frontend:** Vanilla JavaScript SPA, running on port 8585
- **Database:** MongoDB 6.0, accessible via Mongo Express UI on port 8081

**Local setup:**

```bash
cd sales-portal && docker-compose up --build
```

| URL                              | Description                          |
| -------------------------------- | ------------------------------------ |
| `http://localhost:8585`          | Frontend UI                          |
| `http://localhost:8686`          | Backend API                          |
| `http://localhost:8686/api/docs` | Swagger API documentation            |
| `http://localhost:8081`          | Mongo Express DB admin (admin/admin) |

**Default admin:** `admin@example.com` / `admin123`

The backend exposes a REST API under `/api` with JWT Bearer token authentication. The API covers: **Auth** (login/logout), **Products** (CRUD + filtering/sorting), **Customers** (CRUD + filtering/sorting), **Orders** (CRUD + delivery + status transitions + receive + comments + manager assignment), **Notifications** (real-time via WebSocket + REST), **Metrics** (dashboard data), **Users** (CRUD + password change), and **Rebates** (promocodes).

Real-time notifications are delivered via Socket.IO WebSocket. The backend validates all request bodies using JSON Schema middleware and per-field regex validation in custom middleware.

---

## 2. Core Technologies

| Technology              | Version (recommended) | Purpose                                                                      | TS Equivalent                 |
| ----------------------- | --------------------- | ---------------------------------------------------------------------------- | ----------------------------- |
| **Python**              | 3.12+                 | Primary language; strict type hints via `mypy`                               | TypeScript 5.9                |
| **pytest**              | 8.x                   | Test runner, fixtures, parametrize, markers, plugins                         | Playwright Test runner        |
| **playwright** (Python) | 1.49+                 | Browser automation & `APIRequestContext` for HTTP calls                      | `@playwright/test`            |
| **pytest-playwright**   | 0.6+                  | Pytest plugin — provides `page`, `browser`, `context`, `playwright` fixtures | Built into `@playwright/test` |
| **uv**                  | latest                | Fast project/dependency manager (venv + lock + sync)                         | `npm ci` / lockfile workflow  |

---

## 3. Libraries & Dependencies

### 3.1 Core Test Dependencies

| Library                    | Purpose                                                                      | TS Equivalent                |
| -------------------------- | ---------------------------------------------------------------------------- | ---------------------------- |
| **pytest** ^8.0            | Test framework: collection, execution, fixtures, markers                     | `@playwright/test` runner    |
| **playwright** ^1.49       | Browser automation (sync & async API) + `APIRequestContext`                  | `@playwright/test`           |
| **pytest-playwright** ^0.6 | Integrates Playwright fixtures (`page`, `browser_context`, etc.) into pytest | Built-in Playwright fixtures |

### 3.2 API & Validation

| Library               | Purpose                                                                                   | TS Equivalent                             |
| --------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------- |
| _(none)_              | Use Playwright `APIRequestContext` for HTTP calls (no separate requests/httpx dependency) | Playwright `APIRequestContext.fetch()`    |
| **jsonschema** ^4.23  | JSON Schema validation (Draft 2020-12 support)                                            | `ajv` + `ajv-formats`                     |
| **pydantic** ^2.10    | Data models with runtime validation, serialisation, type safety                           | TypeScript interfaces + manual validation |
| **pytest-check** ^2.3 | Soft assertions — continue collecting failures without stopping the test                  | `expect.soft()` in Playwright             |

**Validation strategy (hybrid):** JSON Schema is used for contract-level assertions; Pydantic is used where typed parsing makes service flows clearer.

### 3.3 Data Generation

| Library                                                      | Purpose                                                         | TS Equivalent     |
| ------------------------------------------------------------ | --------------------------------------------------------------- | ----------------- |
| **faker** ^33.0                                              | Randomised test data (names, emails, addresses, numbers, dates) | `@faker-js/faker` |
| **bson** (via **pymongo** ^4.10 or standalone **bson** ^0.5) | `ObjectId` generation for mock response data                    | `bson` (npm)      |

### 3.4 Utilities

| Library                                                     | Purpose                        | TS Equivalent           |
| ----------------------------------------------------------- | ------------------------------ | ----------------------- |
| **python-dotenv** ^1.1                                      | Load `.env` / `.env.dev` files | `dotenv`                |
| **python-dateutil** ^2.9 _or_ stdlib `datetime` (preferred) | Date parsing / formatting      | `moment`                |
| **python-telegram-bot** ^21.x                               | Telegram notifications         | `node-telegram-bot-api` |

### 3.5 Reporting

| Library                           | Purpose                                                      | TS Equivalent                 |
| --------------------------------- | ------------------------------------------------------------ | ----------------------------- |
| **allure-pytest** ^2.13           | Allure reporting plugin for pytest                           | `allure-playwright`           |
| **allure-python-commons** ^2.13   | Allure API (`@allure.step`, `allure.attach`, `allure.title`) | `allure-playwright` internals |
| **pytest-html** ^4.1 _(optional)_ | Lightweight HTML report as fallback                          | Playwright HTML reporter      |

### 3.6 Linting, Formatting & Type Checking

| Tool                | Purpose                                                       | TS Equivalent               |
| ------------------- | ------------------------------------------------------------- | --------------------------- |
| **ruff** ^0.8       | Ultra-fast linter + formatter (replaces flake8, isort, black) | ESLint + Prettier           |
| **mypy** ^1.14      | Static type checking                                          | TypeScript compiler (`tsc`) |
| **pre-commit** ^4.0 | Git hook manager                                              | Husky + lint-staged         |

### 3.7 Optional / Nice-to-Have

| Library                                   | Purpose                                                      |
| ----------------------------------------- | ------------------------------------------------------------ |
| **pytest-xdist** ^3.5                     | Parallel test execution across workers                       |
| **pytest-rerunfailures** ^14.0            | Auto-retry failed tests (equivalent to Playwright `retries`) |
| **pytest-timeout** ^2.3                   | Per-test timeout enforcement                                 |
| **pytest-order** ^1.3                     | Control test execution order                                 |
| **structlog** ^24.4 _or_ stdlib `logging` | Structured logging with secret masking                       |

---

## 4. Project Architecture

The framework preserves the same **multi-layer service-oriented architecture** as the TypeScript version, adapted to Python conventions:

```
┌─────────────────────────────────────────────────────────┐
│                      Tests Layer                        │
│   tests/api/**        tests/ui/**       integration/**  │
└───────────────┬─────────────────────┬───────────────────┘
                │                     │
        ┌───────▼───────┐     ┌───────▼───────┐
        │  API Services │     │  UI Services  │
        │  (Facades)    │     │  (UI-Service) │
        └───────┬───────┘     └───────┬───────┘
                │                     │
        ┌───────▼───────┐     ┌───────▼───────┐
        │  API Wrappers │     │  Page Objects │
        │  (Endpoint)   │     │  (POM)        │
        └───────┬───────┘     └───────┬───────┘
                │                     │
        ┌───────▼───────┐     ┌───────▼───────┐
        │  API Client   │     │  Base Page /  │
        │  (HTTP)       │     │  SalesPortal  │
        └───────────────┘     └───────────────┘
                │                     │
        ┌───────▼─────────────────────▼───────┐
        │       Fixtures (DI Layer)           │
        │    conftest.py (root + per-dir)     │
        └───────────────┬─────────────────────┘
                        │
        ┌───────────────▼─────────────────────┐
        │       Data Layer                    │
        │  Models · Schemas · Generators · DDT│
        └─────────────────────────────────────┘
```

### Key Design Principles (mapped from TS)

| Principle                     | TypeScript                        | Python                                         |
| ----------------------------- | --------------------------------- | ---------------------------------------------- |
| **Dependency Injection**      | `test.extend<>()` fixtures        | pytest `@pytest.fixture` in `conftest.py`      |
| **Service / Facade Pattern**  | Service classes                   | Service classes (identical)                    |
| **Page Object Model**         | Abstract TS classes + inheritance | ABC + inheritance (or protocol classes)        |
| **Data-Driven Testing**       | `for...of` loops over case arrays | `@pytest.mark.parametrize` with case lists     |
| **Schema Validation**         | AJV (JS)                          | `jsonschema` (Python)                          |
| **Type Safety**               | TypeScript strict mode            | `mypy` strict + type hints + `pydantic` models |
| **Decorator-based Reporting** | `@logStep()` → `test.step()`      | `@allure.step()` decorator                     |

### Key implementation decisions

- **Playwright sync API is the default** (`playwright.sync_api`) to keep tests/fixtures simple and aligned with classic pytest patterns.
- **Dependency management uses `uv` project flow** (venv + lock + `uv sync`) for fast, reproducible installs in CI and locally.

---

## 5. Layer-by-Layer Breakdown

### 5.1 API Client Layer (`src/api/api_clients/`)

| Module                     | Role                                                                                                     | TS Equivalent      |
| -------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------ |
| `base_api_client.py`       | Abstract base class (`ABC`) defining `send()` and `_transform_response()` contracts                      | `baseApiClient.ts` |
| `playwright_api_client.py` | Concrete client wrapping `APIRequestContext.fetch()`; attaches request/response to Allure; masks secrets | `requestApi.ts`    |
| `types.py`                 | `Protocol` class `ApiClient` (structural typing — no `I` prefix per Python convention)                   | `types.ts`         |

**Python-specific notes:**

- Use `typing.Protocol` (PEP 544) instead of TypeScript `interface` for structural subtyping — name protocols without `I` prefix (e.g., `ApiClient`, not `IApiClient`).
- Use `@dataclass` or `pydantic.BaseModel` for `RequestOptions` and `Response` instead of plain TS interfaces.
- Secret masking via `re.sub()` in the attach step.

### 5.2 API Endpoint Wrappers (`src/api/api/`)

One class per domain entity, each accepting an `ApiClient` via `__init__`:

| Module                 | Endpoints covered                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `login_api.py`         | `POST /api/login`, `POST /api/logout`                                                                                       |
| `products_api.py`      | CRUD on `/api/products` + `/api/products/all` (unfiltered) + sorted/filtered list via query params                          |
| `customers_api.py`     | CRUD + `/api/customers/all` + sorted/filtered list + `/api/customers/:id/orders`                                            |
| `orders_api.py`        | CRUD, delivery (POST), status (PUT), receive (POST), assign/unassign manager (PUT), comments (POST/DELETE) on `/api/orders` |
| `notifications_api.py` | `GET /api/notifications`, `PATCH /:id/read`, `PATCH /mark-all-read`                                                         |
| `users_api.py`         | `GET /api/users`, `GET /:id`, `POST` (register), `DELETE /:id`, `PATCH /password/:id`                                       |
| `metrics_api.py`       | `GET /api/metrics`                                                                                                          |

> **Source of truth:** `sales-portal/backend/routers/` — each router file documents exact routes, HTTP methods, parameters, and Swagger schemas.

Every public method is decorated with `@allure.step("...")` for automatic reporting.

### 5.3 API Services (`src/api/service/`)

| Service               | Highlights                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `LoginService`        | `login_as_admin()` → returns Bearer token                                                                                             |
| `ProductsApiService`  | `create()`, `update()`, `delete()`, `bulk_create()`, `delete_all_products()` with `validate_response()`                               |
| `CustomersApiService` | Similar CRUD + validation                                                                                                             |
| `OrdersApiService`    | Multi-step flows: `create_order_and_entities()`, `create_order_with_delivery()`, status transitions, full cleanup via `EntitiesStore` |
| `EntitiesStore`       | Tracks created entity IDs in `set[str]` for deterministic teardown                                                                    |

### 5.4 API Facades (`src/api/facades/`)

| Facade                | Purpose                                                                                                 |
| --------------------- | ------------------------------------------------------------------------------------------------------- |
| `OrdersFacadeService` | End-to-end order lifecycle (create → delivery → process → receive → cancel) without internal validation |

### 5.5 UI Page Objects (`src/ui/pages/`)

Inheritance chain (using Python ABC):

```
BasePage  (ABC — cookie helpers, request/response interception via page.expect_request/response)
  └─ SalesPortalPage  (spinner waits, toast locator, open(route), abstract unique_element)
       ├─ BaseModal  (wait_for_closed)
       ├─ HomePage, NavBar, LoginPage
       ├─ Products: ProductsListPage, AddNewProductPage, EditProductPage, DeleteModal, DetailsModal
       ├─ Customers: CustomersListPage, AddNewCustomerPage, DetailsModal
       └─ Orders: OrdersListPage, OrderDetailsPage, CreateOrderModal, EditProductsModal, Components/*
```

**Python-specific notes:**

- `@property` for locators instead of TS class fields: `self.page.locator(...)`.
- `@abstractmethod` for `unique_element` property.
- Playwright's sync API (`page.locator()`, `page.goto()`) used by default; async API available if needed.

### 5.6 UI Services (`src/ui/service/`)

Each UI service composes one or more Page Objects:

`LoginUIService`, `HomeUIService`, `AddNewProductUIService`, `EditProductUIService`, `ProductsListUIService`, `AddNewCustomerUIService`, `CustomersListUIService`, `OrderDetailsUIService`, `CommentsUIService`, `AssignManagerUIService`

### 5.7 Mock Layer (`src/mock/`)

`Mock` class wraps `page.route()` for network interception, providing typed methods: `products_page()`, `orders_page()`, `order_details_modal()`, `metrics_home_page()`, etc.

---

## 6. Test Strategy & Patterns

### 6.1 Test Organisation

```
tests/
  api/
    products/   (test_create, test_get_by_id, test_get_all, test_update, test_delete)
    customers/  (test_create, test_get_by_id, test_get_list, test_get_all, test_delete)
    orders/     (test_create, test_get_by_id, test_update, test_delete, test_delivery,
                 test_orders_status, test_receive, test_comment,
                 test_assign_unassign_manager, test_notifications)
  ui/
    conftest.py         (auth setup — storage_state fixture)
    orders/             (test_create_order, test_order_details, test_order_delivery,
                         test_comments, test_export_orders, test_navigation,
                         test_assign_manager, test_processing,
                         test_receive_products, test_refresh_order,
                         test_requested_products, test_order_modals,
                         test_update_customer)
    integration/        (test_orders_list, test_create_order, test_update_customer — mock-based)
  conftest.py           (root — shared fixtures, env loading, api fixtures)
```

### 6.2 Pytest Configuration & Marks

Defined in `pyproject.toml` under `[tool.pytest.ini_options]`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "smoke: critical-path tests",
    "regression: full regression suite",
    "integration: UI + mock integration tests",
    "api: API-only tests",
    "ui: UI-only tests",
    "e2e: end-to-end tests",
    "products",
    "customers",
    "orders",
    "managers",
]
```

**Run commands (equivalents of `package.json` scripts):**

```bash
# All tests
pytest

# API only
pytest tests/api/ -m "regression or smoke"

# UI only
pytest tests/ui/ -m "regression or smoke"

# Smoke only
pytest -m smoke

# With Allure
pytest --alluredir=allure-results

# Parallel (with xdist)
pytest -n 5
```

### 6.3 Fixtures & Dependency Injection (`conftest.py`)

| Fixture                       | Scope      | Provides                                                | TS Equivalent                 |
| ----------------------------- | ---------- | ------------------------------------------------------- | ----------------------------- |
| `api_client`                  | `session`  | `PlaywrightApiClient` wrapping `APIRequestContext`      | `RequestApi`                  |
| `login_api`                   | `session`  | `LoginApi` instance                                     | `loginApi` fixture            |
| `products_api`                | `session`  | `ProductsApi` instance                                  | `productsApi` fixture         |
| `customers_api`               | `session`  | `CustomersApi` instance                                 | `customersApi` fixture        |
| `orders_api`                  | `session`  | `OrdersApi` instance                                    | `ordersApi` fixture           |
| `products_service`            | `session`  | `ProductsApiService`                                    | `productsApiService` fixture  |
| `customers_service`           | `session`  | `CustomersApiService`                                   | `customersApiService` fixture |
| `orders_service`              | `session`  | `OrdersApiService` (stateless; store injected per test) | `ordersApiService` fixture    |
| `orders_facade`               | `session`  | `OrdersFacadeService`                                   | `ordersFacadeService` fixture |
| `login_service`               | `session`  | `LoginService`                                          | `loginApiService` fixture     |
| `admin_token`                 | `session`  | Cached Bearer token string                              | (inline `loginAsAdmin()`)     |
| `cleanup`                     | `function` | Cleanup registry; auto-deletes in teardown (`yield`)    | `cleanup` fixture             |
| `home_page`                   | `function` | `HomePage(page)`                                        | `homePage` fixture            |
| `products_list_page`          | `function` | `ProductsListPage(page)`                                | `productsListPage` fixture    |
| `mock`                        | `function` | `Mock(page)`                                            | `mock` fixture                |
| _…etc for all pages/services_ |            |                                                         |                               |

**Python fixture teardown** uses `yield`:

```python
@pytest.fixture
def cleanup(orders_service, login_service):
    """Per-test cleanup: yields a fresh store, auto-deletes tracked entities in teardown."""
    store = EntitiesStore()
    orders_service.entities_store = store
    yield store                         # test runs here
    token = login_service.login_as_admin()
    orders_service.full_delete(token)   # automatic teardown
    store.clear()
```

### 6.4 Authentication & Storage State

```python
# tests/ui/conftest.py
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, storage_state_path):
    return {**browser_context_args, "storage_state": storage_state_path}

@pytest.fixture(scope="session")
def storage_state_path(playwright, api_client, login_service):
    """Generate storage state once per session (equivalent of auth.setup.ts)."""
    token = login_service.login_as_admin()
    state_path = "src/.auth/user.json"
    # create context, add cookies, save state
    ...
    return state_path
```

### 6.5 Data-Driven Testing (DDT)

Instead of `for...of` loops, use `@pytest.mark.parametrize`:

```python
# data/sales_portal/orders/create_delivery_ddt.py
import pytest

CREATE_DELIVERY_POSITIVE_CASES = [
    pytest.param(
        DeliveryCase(title="All required fields", delivery_data=generate_delivery(), expected_status=200),
        id="all-required-fields",
    ),
    pytest.param(
        DeliveryCase(title="Pickup condition", delivery_data=generate_delivery(condition=PICKUP), expected_status=200),
        id="pickup-condition",
    ),
]

# tests/api/orders/test_delivery.py
@pytest.mark.parametrize("case", CREATE_DELIVERY_POSITIVE_CASES)
def test_add_delivery_positive(case, orders_api, admin_token, order):
    response = orders_api.add_delivery(admin_token, order.id, case.delivery_data)
    validate_response(response, status=case.expected_status, ...)
```

### 6.6 Data Generation

| Generator function         | Libraries used                                           | TS Equivalent             |
| -------------------------- | -------------------------------------------------------- | ------------------------- |
| `generate_product_data()`  | `faker`, `Manufacturers` enum                            | `generateProductData()`   |
| `generate_customer_data()` | `faker`, `Country` enum                                  | `generateCustomerData()`  |
| `generate_delivery()`      | `faker`, `Country`/`DeliveryCondition` enums, `datetime` | `generateDelivery()`      |
| `generate_order_data()`    | Composes customer + product IDs                          | `generateOrderData()`     |
| Mock response builders     | `bson.ObjectId`                                          | Mock builders with `bson` |

**Python-specific:** Use `@dataclass` or `pydantic.BaseModel` with factory functions, or `faker` providers.

### 6.7 Validation

| Utility                           | Implementation                                                             | TS Equivalent                   |
| --------------------------------- | -------------------------------------------------------------------------- | ------------------------------- |
| `validate_response()`             | Asserts `status`, `is_success`, `error_message`; calls `validate_schema()` | `validateResponse()`            |
| `validate_schema()`               | `jsonschema.validate(instance, schema)`                                    | `validateJsonSchema()` with AJV |
| JSON Schemas                      | Python dicts or `.json` files under `data/schemas/`                        | TS schema objects               |
| `pydantic` models _(alternative)_ | Replace JSON Schemas with Pydantic model validation                        | —                               |

### 6.8 Cleanup

- `EntitiesStore` tracks created entity IDs in `set[str]`.
- The `cleanup` fixture uses `yield` + teardown to call `orders_service.full_delete(token)`.
- Deletion order: orders → products → customers (same as TS).

---

## 7. Configuration & Environment

### 7.1 Environment Variables

Loaded via `python-dotenv` from `.env` (default) or `.env.dev` (when `TEST_ENV=dev`):

| Variable               | Description                   | Local default (Docker Compose) |
| ---------------------- | ----------------------------- | ------------------------------ |
| `SALES_PORTAL_URL`     | UI base URL                   | `http://localhost:8585`        |
| `SALES_PORTAL_API_URL` | API base URL                  | `http://localhost:8686`        |
| `USER_NAME`            | Test user email               | `admin@example.com`            |
| `USER_PASSWORD`        | Test user password            | `admin123`                     |
| `MANAGER_IDS`          | JSON array of manager UUIDs   |                                |
| `TELEGRAM_BOT_TOKEN`   | (optional) Telegram bot token |                                |
| `TELEGRAM_CHAT_ID`     | (optional) Telegram chat ID   |                                |

> **Local dev setup:** Run `docker-compose up --build` in `sales-portal/` to start the application. Swagger docs are at `http://localhost:8686/api/docs`.

### 7.2 Configuration Module (`src/config/`)

```python
# src/sales_portal_tests/config/env.py
from dotenv import load_dotenv
import os, json

load_dotenv(dotenv_path=".env.dev" if os.getenv("TEST_ENV") == "dev" else ".env")

SALES_PORTAL_URL = os.environ["SALES_PORTAL_URL"]
SALES_PORTAL_API_URL = os.environ["SALES_PORTAL_API_URL"]
CREDENTIALS = {"username": os.environ["USER_NAME"], "password": os.environ["USER_PASSWORD"]}
MANAGER_IDS: list[str] = json.loads(os.environ["MANAGER_IDS"])
```

```python
# src/sales_portal_tests/config/api_config.py
# Module-level constants and plain functions — not a class with static methods.
# Derived from actual backend routes in sales-portal/backend/routers/
from sales_portal_tests.config.env import SALES_PORTAL_API_URL

BASE_URL = SALES_PORTAL_API_URL

# Static endpoints (module constants)
LOGIN = f"{BASE_URL}/api/login"
LOGOUT = f"{BASE_URL}/api/logout"
PRODUCTS = f"{BASE_URL}/api/products"
PRODUCTS_ALL = f"{BASE_URL}/api/products/all"
CUSTOMERS = f"{BASE_URL}/api/customers"
CUSTOMERS_ALL = f"{BASE_URL}/api/customers/all"
ORDERS = f"{BASE_URL}/api/orders"
NOTIFICATIONS = f"{BASE_URL}/api/notifications"
NOTIFICATIONS_MARK_ALL_READ = f"{BASE_URL}/api/notifications/mark-all-read"
METRICS = f"{BASE_URL}/api/metrics"
USERS = f"{BASE_URL}/api/users"

# Parameterised endpoints (plain functions)
def product_by_id(product_id: str) -> str:
    return f"{PRODUCTS}/{product_id}"

def customer_by_id(customer_id: str) -> str:
    return f"{CUSTOMERS}/{customer_id}"

def customer_orders(customer_id: str) -> str:
    return f"{CUSTOMERS}/{customer_id}/orders"

def order_by_id(order_id: str) -> str:
    return f"{ORDERS}/{order_id}"

def order_delivery(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/delivery"

def order_status(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/status"

def order_receive(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/receive"

def order_comments(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/comments"

def order_comment_by_id(order_id: str, comment_id: str) -> str:
    return f"{ORDERS}/{order_id}/comments/{comment_id}"

def assign_manager(order_id: str, manager_id: str) -> str:
    return f"{ORDERS}/{order_id}/assign-manager/{manager_id}"

def unassign_manager(order_id: str) -> str:
    return f"{ORDERS}/{order_id}/unassign-manager"

def notification_read(notification_id: str) -> str:
    return f"{NOTIFICATIONS}/{notification_id}/read"

def user_by_id(user_id: str) -> str:
    return f"{USERS}/{user_id}"

def user_password(user_id: str) -> str:
    return f"{USERS}/password/{user_id}"

def promocode_by_name(name: str) -> str:
    return f"{BASE_URL}/api/promocodes/{name}"
# ... etc
```

### 7.3 Project Configuration (`pyproject.toml`)

All Python tooling is configured in a single `pyproject.toml`:

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
    "pymongo>=4.10",           # for bson.ObjectId
    "pytest-xdist>=3.5",
    "pytest-rerunfailures>=14.0",
    "pytest-timeout>=2.3",
]
# NOTE: No `requests` — Playwright's APIRequestContext handles all HTTP calls.

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

[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "SIM", "RUF"]
```

---

## 8. Linting, Formatting & Git Hooks

### 8.1 Ruff (Linter + Formatter)

Replaces ESLint + Prettier in one tool:

```bash
ruff check src/ tests/          # lint
ruff check src/ tests/ --fix    # lint + auto-fix
ruff format src/ tests/         # format (like black)
```

### 8.2 Mypy (Static Type Checking)

```bash
mypy src/ tests/                # strict type checking
```

Equivalent to `tsc --noEmit` from the TS build check.

### 8.3 Git Hooks (pre-commit)

`.pre-commit-config.yaml`:

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

| TS Tool        | Python Equivalent                           |
| -------------- | ------------------------------------------- |
| Husky          | pre-commit                                  |
| lint-staged    | pre-commit (built-in staged-file filtering) |
| ESLint         | Ruff lint                                   |
| Prettier       | Ruff format                                 |
| `tsc --noEmit` | `mypy --strict`                             |

---

## 9. CI/CD Pipeline

### 9.1 Lint & Type Check (`build.yml`)

```yaml
name: Python Lint & Type Check
on:
  pull_request:
    branches: [main]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff mypy pydantic
      - run: ruff check src/ tests/
      - run: mypy src/ tests/
```

### 9.2 Test Run + Report (`tests.yml`)

```yaml
name: Run Sales Portal Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write
  pages: write

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    env:
      SALES_PORTAL_API_URL: ${{ secrets.SALES_PORTAL_API_URL }}
      SALES_PORTAL_URL: ${{ secrets.SALES_PORTAL_URL }}
      USER_NAME: ${{ secrets.USER_NAME }}
      USER_PASSWORD: ${{ secrets.USER_PASSWORD }}
      MANAGER_IDS: ${{ secrets.MANAGER_IDS }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: |
          uv sync --all-extras
          playwright install --with-deps chromium

      - name: Install OpenJDK (for Allure)
        run: |
          sudo apt-get update && sudo apt-get install -y openjdk-17-jre

      - name: Run API regression tests
        run: pytest tests/api/ -m "regression or smoke" --alluredir=allure-results
        continue-on-error: true

      - name: Run UI regression tests
        run: pytest tests/ui/ -m "regression or smoke" --alluredir=allure-results
        continue-on-error: true

      - name: Generate Allure report
        run: allure generate allure-results -o allure-report --clean

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./allure-report

      - name: Telegram notification
        if: success()
        run: |
          MESSAGE="Python test run finished!\n\nReport: https://..."
          curl -s -X POST \
            -d "{\"chat_id\":\"${{ secrets.TELEGRAM_CHAT_ID }}\",\"text\":\"${MESSAGE}\"}" \
            -H "Content-Type: application/json" \
            https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage
```

---

## 10. Reporting & Notifications

### 10.1 Reporters

| Reporter                              | Configuration                | TS Equivalent            |
| ------------------------------------- | ---------------------------- | ------------------------ |
| **Allure** (`allure-pytest`)          | `--alluredir=allure-results` | `allure-playwright`      |
| **HTML** (`pytest-html`) _(optional)_ | `--html=report.html`         | Playwright HTML reporter |
| **JUnit XML** (built-in)              | `--junitxml=results.xml`     | —                        |

### 10.2 Allure Integration

- `@allure.step("...")` decorator on service/page methods (equivalent of `@logStep()`).
- `allure.attach(body, name, attachment_type)` for request/response JSON.
- `@allure.title()`, `@allure.feature()`, `@allure.story()` for test metadata.
- `allure.dynamic.tag()` for runtime tagging.
- Environment info written to `allure-results/environment.properties`.

### 10.3 Trace, Screenshot & Video

Configured via `pytest.ini` / `pyproject.toml` or `conftest.py`:

| Artifact   | Configuration                  | TS Equivalent                   |
| ---------- | ------------------------------ | ------------------------------- |
| Trace      | `--tracing=on`                 | `trace: "on"`                   |
| Screenshot | `--screenshot=only-on-failure` | `screenshot: "only-on-failure"` |
| Video      | `--video=on-first-retry`       | `video: "on-first-retry"`       |

### 10.4 Telegram Notifications

`TelegramService` class wrapping `python-telegram-bot`, behind a `NotificationService` protocol (Strategy pattern — identical to TS).

---

## 11. Directory Reference

```
sales-portal-tests-python/
├── .github/
│   └── workflows/
│       ├── build.yml                  # Lint + type check on PR
│       └── tests.yml                  # Full test run + Allure deploy
├── .pre-commit-config.yaml            # ruff + mypy hooks
├── pyproject.toml                     # Project metadata, pytest, mypy, ruff config
├── requirements.txt                   # Pinned dependencies (or use pyproject.toml)
│
├── src/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── env.py                     # Environment variables (dotenv)
│   │   └── api_config.py             # API base URL + all endpoint paths
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api_clients/               # HTTP client abstraction
│   │   │   ├── __init__.py
│   │   │   ├── base_api_client.py     #   ABC defining send() contract
│   │   │   ├── playwright_api_client.py  # Playwright APIRequestContext implementation
│   │   │   └── types.py              #   Protocol class ApiClient
│   │   ├── api/                       # Endpoint wrapper classes
│   │   │   ├── __init__.py
│   │   │   ├── login_api.py
│   │   │   ├── products_api.py
│   │   │   ├── customers_api.py
│   │   │   ├── orders_api.py
│   │   │   ├── notifications_api.py
│   │   │   ├── users_api.py
│   │   │   └── metrics_api.py
│   │   ├── service/                   # Business-level API services
│   │   │   ├── __init__.py
│   │   │   ├── login_service.py
│   │   │   ├── products_service.py
│   │   │   ├── customers_service.py
│   │   │   ├── orders_service.py
│   │   │   └── stores/
│   │   │       ├── __init__.py
│   │   │       └── entities_store.py  # Tracks IDs for cleanup
│   │   └── facades/
│   │       ├── __init__.py
│   │       └── orders_facade_service.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── pages/                     # Page Object Model
│   │   │   ├── __init__.py
│   │   │   ├── base_page.py           #   ABC: interception, cookies
│   │   │   ├── sales_portal_page.py   #   ABC: spinners, navigation
│   │   │   ├── base_modal.py          #   ABC: modal close wait
│   │   │   ├── home_page.py
│   │   │   ├── navbar_component.py
│   │   │   ├── login/
│   │   │   │   ├── __init__.py
│   │   │   │   └── login_page.py
│   │   │   ├── products/              #   List, Add, Edit, Delete, Details
│   │   │   ├── customers/             #   List, Add, Details
│   │   │   └── orders/                #   List, Details, Create, Edit, Components
│   │   └── service/                   # UI flow services
│   │       ├── __init__.py
│   │       ├── login_ui_service.py
│   │       ├── home_ui_service.py
│   │       ├── add_new_product_ui_service.py
│   │       ├── edit_product_ui_service.py
│   │       ├── products_list_ui_service.py
│   │       ├── add_new_customer_ui_service.py
│   │       ├── customers_list_ui_service.py
│   │       ├── order_details_ui_service.py
│   │       ├── comments_ui_service.py
│   │       └── assign_manager_ui_service.py
│   │
│   ├── mock/
│   │   ├── __init__.py
│   │   └── mock.py                    # Playwright route() wrappers
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── tags.py                    # Marker name constants
│   │   ├── status_codes.py            # StatusCodes enum (IntEnum)
│   │   ├── models/                    # Pydantic / dataclass models
│   │   │   ├── __init__.py
│   │   │   ├── core.py                #   RequestOptions, Response, ResponseFields
│   │   │   ├── product.py
│   │   │   ├── customer.py
│   │   │   ├── order.py
│   │   │   ├── delivery.py
│   │   │   ├── credentials.py
│   │   │   ├── metrics.py
│   │   │   ├── notifications.py
│   │   │   └── user.py
│   │   ├── schemas/                   # JSON Schema dicts or .json files
│   │   │   ├── core_schema.py
│   │   │   ├── products/
│   │   │   ├── customers/
│   │   │   ├── orders/
│   │   │   ├── delivery/
│   │   │   ├── login/
│   │   │   └── users/
│   │   └── sales_portal/             # Test data & DDT case tables
│   │       ├── constants.py
│   │       ├── country.py
│   │       ├── errors.py
│   │       ├── notifications.py
│   │       ├── order_status.py
│   │       ├── delivery_status.py
│   │       ├── products/              # generators + DDT cases
│   │       ├── customers/             # generators + DDT cases
│   │       └── orders/                # generators + DDT cases
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validation/
│       │   ├── validate_response.py   # Status + is_success + error_message + schema
│       │   └── validate_schema.py     # jsonschema.validate()
│       ├── notifications/
│       │   ├── notification_service.py  # Protocol (interface)
│       │   └── telegram_service.py      # Telegram implementation
│       ├── assertions/
│       │   └── confirmation_modal.py  # Reusable modal assertion helper
│       ├── files/
│       │   ├── csv_utils.py           # CSV parser (stdlib csv module)
│       │   └── export_file_utils.py   # Download → save → parse
│       ├── orders/
│       │   └── helpers.py
│       ├── date_utils.py              # datetime-based formatters
│       ├── enum_utils.py              # get_random_enum_value()
│       ├── mask_secrets.py            # re.sub() for password/token masking
│       └── log_utils.py              # Conditional logging
│
├── tests/
│   ├── conftest.py                    # Root: env loading, API fixtures, cleanup
│   ├── api/
│   │   ├── conftest.py                # API-specific fixtures (token, services)
│   │   ├── products/
│   │   │   ├── test_create.py
│   │   │   ├── test_get_by_id.py
│   │   │   ├── test_get_all.py
│   │   │   ├── test_update.py
│   │   │   └── test_delete.py
│   │   ├── customers/
│   │   │   ├── test_create.py
│   │   │   ├── test_get_by_id.py
│   │   │   ├── test_get_list.py
│   │   │   ├── test_get_all.py
│   │   │   └── test_delete.py
│   │   └── orders/
│   │       ├── test_create.py
│   │       ├── test_get_by_id.py
│   │       ├── test_update.py
│   │       ├── test_delete.py
│   │       ├── test_delivery.py
│   │       ├── test_orders_status.py
│   │       ├── test_receive.py
│   │       ├── test_comment.py
│   │       ├── test_assign_unassign_manager.py
│   │       └── test_notifications.py
│   └── ui/
│       ├── conftest.py                # Auth setup (storage_state fixture)
│       ├── orders/
│       │   ├── test_create_order.py
│       │   ├── test_order_details.py
│       │   ├── test_order_delivery.py
│       │   ├── test_comments.py
│       │   ├── test_export_orders.py
│       │   ├── test_navigation.py
│       │   ├── test_assign_manager.py
│       │   ├── test_processing.py
│       │   ├── test_receive_products.py
│       │   ├── test_refresh_order.py
│       │   ├── test_requested_products.py
│       │   ├── test_order_modals.py
│       │   └── test_update_customer.py
│       └── integration/
│           ├── test_orders_list.py
│           ├── test_create_order.py
│           └── test_update_customer.py
│
├── allure-results/
├── allure-report/
└── test-results/
```

---

## 12. TypeScript → Python Migration Map

A quick-reference for mapping every TypeScript concept to its Python equivalent:

| Concept                    | TypeScript (Current)                                      | Python (Target)                                     |
| -------------------------- | --------------------------------------------------------- | --------------------------------------------------- |
| **Language**               | TypeScript 5.9 (strict)                                   | Python 3.12+ (`mypy --strict`)                      |
| **Test runner**            | Playwright Test                                           | pytest + pytest-playwright                          |
| **Browser automation**     | `@playwright/test`                                        | `playwright` (sync API)                             |
| **HTTP client**            | `APIRequestContext.fetch()`                               | `APIRequestContext.fetch()` (Playwright sync API)   |
| **Fixtures / DI**          | `test.extend<>()`                                         | `@pytest.fixture` in `conftest.py`                  |
| **Fixture teardown**       | Callback in `use()`                                       | `yield` + cleanup after yield                       |
| **Fixture merging**        | `mergeTests(...)`                                         | Multiple `conftest.py` files (automatic)            |
| **Parametrize / DDT**      | `for...of` loops                                          | `@pytest.mark.parametrize`                          |
| **Tags / markers**         | `{ tag: [TAGS.SMOKE] }`                                   | `@pytest.mark.smoke`                                |
| **Selective run**          | `--grep @smoke`                                           | `-m smoke`                                          |
| **Interfaces**             | `interface IApiClient`                                    | `typing.Protocol` / ABC                             |
| **Type models**            | TS interfaces + manual checks                             | `pydantic.BaseModel` / `@dataclass`                 |
| **JSON Schema validation** | AJV                                                       | `jsonschema`                                        |
| **Data generation**        | `@faker-js/faker`                                         | `faker` (Python)                                    |
| **ObjectId stubs**         | `bson` (npm)                                              | `bson.ObjectId` (pymongo)                           |
| **Date formatting**        | `moment`                                                  | `datetime` / `python-dateutil`                      |
| **Utility belt**           | `lodash`                                                  | stdlib (`dict` comprehensions, `copy`, `itertools`) |
| **Env loading**            | `dotenv`                                                  | `python-dotenv`                                     |
| **Allure steps**           | `@logStep()` → `test.step()`                              | `@allure.step()`                                    |
| **Allure report**          | `allure-playwright` + `allure-commandline`                | `allure-pytest` + `allure-commandline`              |
| **Linter**                 | ESLint                                                    | Ruff                                                |
| **Formatter**              | Prettier                                                  | Ruff format                                         |
| **Type checker**           | `tsc`                                                     | `mypy`                                              |
| **Git hooks**              | Husky + lint-staged                                       | pre-commit                                          |
| **Notifications**          | `node-telegram-bot-api`                                   | `python-telegram-bot`                               |
| **Module system**          | CommonJS / ESM                                            | Python packages (`__init__.py`)                     |
| **Abstract classes**       | `abstract class`                                          | `abc.ABC` + `@abstractmethod`                       |
| **Enums**                  | `enum` (TS)                                               | `enum.Enum` / `enum.StrEnum` / `enum.IntEnum`       |
| **Decorators**             | TS stage-3 decorators                                     | Python decorators (native)                          |
| **CI container**           | `mcr.microsoft.com/playwright:...`                        | `actions/setup-python` + `playwright install`       |
| **Parallel execution**     | `workers: 5` in config                                    | `pytest-xdist -n 5`                                 |
| **Retries**                | `retries: 1` in config                                    | `pytest-rerunfailures --reruns 1`                   |
| **Config file**            | `playwright.config.ts` + `tsconfig.json` + `package.json` | `pyproject.toml` (single file)                      |

---

## Summary of Design Patterns (Preserved)

| Pattern                     | Python Implementation                                                            |
| --------------------------- | -------------------------------------------------------------------------------- |
| **Page Object Model (POM)** | ABC inheritance chain under `src/ui/pages/`                                      |
| **Service Layer**           | `src/api/service/` and `src/ui/service/` classes                                 |
| **Facade**                  | `src/api/facades/` — multi-step API operations                                   |
| **Strategy**                | `NotificationService` protocol → `TelegramService`                               |
| **Dependency Injection**    | pytest `@pytest.fixture` in `conftest.py` hierarchy                              |
| **Data-Driven Testing**     | `@pytest.mark.parametrize` with case dataclasses                                 |
| **Builder / Factory**       | `generate_*_data()` functions with optional `**kwargs` overrides                 |
| **Decorator**               | `@allure.step()` on service/page methods                                         |
| **Repository / Store**      | `EntitiesStore` — `set[str]` tracking for teardown                               |
| **Template Method**         | ABC with `@abstractmethod` (`unique_element`, `wait_for_opened`)                 |
| **Protocol**                | `typing.Protocol` for structural interfaces (`ApiClient`, `NotificationService`) |
