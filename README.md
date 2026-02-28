# Sales Portal — Python Test Automation Framework

[![Run Sales Portal Tests](https://github.com/aharashchuk/pytest_example/actions/workflows/tests.yml/badge.svg)](https://github.com/aharashchuk/pytest_example/actions/workflows/tests.yml)
[![Python Build Check](https://github.com/aharashchuk/pytest_example/actions/workflows/build.yml/badge.svg)](https://github.com/aharashchuk/pytest_example/actions/workflows/build.yml)

> **pytest + Playwright** end-to-end test framework covering **API** and **UI** for the Sales Portal product.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running Tests](#running-tests)
- [Viewing Reports](#viewing-reports)
- [CI/CD](#cicd)
- [Project Structure](#project-structure)
- [Key Conventions](#key-conventions)
- [Development Environment (AUT)](#development-environment-aut)

---

## Overview

This project is a multi-layered test automation framework built with **Python 3.12+**, **pytest**, and **Playwright**. It provides both **API** and **UI** test coverage for the Sales Portal application, following a service-oriented architecture with clear separation of concerns.

Key capabilities:

- **API tests** — full CRUD coverage for Products, Customers, Orders, Notifications, Users, and Metrics
- **UI tests** — Page Object–based browser tests with authenticated sessions
- **Integration tests** — mock-based UI tests using Playwright route interception
- **DDT (Data-Driven Testing)** — `pytest.parametrize` with `pytest.param(…, id=…)` case tables
- **Hybrid validation** — JSON Schema for contract checks, Pydantic for typed flow data
- **Allure reporting** — step hierarchy, screenshots-on-failure, environment properties
- **CI/CD** — GitHub Actions pipelines with Allure report publishing and Telegram notifications

For the full architecture specification, see [`STACK_PYTHON.md`](./STACK_PYTHON.md).

---

## Architecture

```
src/sales_portal_tests/
├── config/          # Environment loading, API endpoint config
├── api/
│   ├── api_clients/ # Protocol + Playwright HTTP client
│   ├── api/         # Endpoint wrappers (one class per domain)
│   ├── service/     # Business-level flows + EntitiesStore cleanup
│   └── facades/     # Cross-domain orchestration
├── ui/
│   ├── pages/       # Page Objects (BasePage → SalesPortalPage → domain pages)
│   └── service/     # Higher-level UI flows
├── mock/            # Playwright route interception helpers
├── data/
│   ├── models/      # Pydantic/dataclass models per domain entity
│   ├── schemas/     # JSON Schema dicts for response validation
│   └── sales_portal/# Enums, constants, data generators, DDT case tables
└── utils/           # Validation, date helpers, assertions, reporting, notifications

tests/
├── conftest.py      # Root fixtures (session-scoped API infra + cleanup + Allure hooks)
├── api/             # API test suites (products, customers, orders, login)
└── ui/              # UI + integration test suites (orders, integration)
```

---

## Prerequisites

| Requirement        | Version | Notes                                   |
| ------------------ | ------- | --------------------------------------- |
| **Python**         | 3.12+   | Required for modern type-hint features  |
| **pip** or **uv**  | latest  | Dependency manager                      |
| **Playwright**     | 1.49+   | Chromium browser installed via CLI      |
| **Docker Compose** | latest  | Only for running the AUT locally        |
| **Java JRE**       | 17+     | Only for local Allure report generation |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/aharashchuk/pytest_example.git
cd pytest_example
```

### 2. Create a virtual environment and install dependencies

**Using uv (recommended):**

```bash
uv venv --python 3.12
source .venv/bin/activate
uv sync --all-extras
```

**Using pip:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 3. Install Playwright browsers

```bash
playwright install --with-deps chromium
```

### 4. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.dist .env
```

Edit `.env`:

```dotenv
SALES_PORTAL_URL=http://localhost:8585
SALES_PORTAL_API_URL=http://localhost:8686
USER_NAME=admin@example.com
USER_PASSWORD=admin123
MANAGER_IDS=["<manager-user-id>"]

# Optional — Telegram notifications
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

To use a separate dev environment, set `TEST_ENV=dev` and create a `.env.dev` file.

### 5. Start the application under test (local)

```bash
cd sales-portal
docker-compose up --build
```

| Service       | URL                            |
| ------------- | ------------------------------ |
| Frontend      | http://localhost:8585          |
| Backend API   | http://localhost:8686          |
| Swagger       | http://localhost:8686/api/docs |
| Mongo Express | http://localhost:8081          |

Default credentials: `admin@example.com` / `admin123`

---

## Running Tests

### Quick commands (via Makefile)

```bash
make test-api          # Run API smoke + regression tests
make test-ui           # Run UI smoke + regression tests
make test-smoke        # Run smoke tests only (API + UI)
make test-all          # Run all tests
make lint              # Run ruff + mypy
make report            # Generate and open Allure report
```

### Direct pytest commands

```bash
# All API tests
pytest tests/api/ -m "regression or smoke" --alluredir=allure-results

# All UI tests
pytest tests/ui/ -m "regression or smoke" --alluredir=allure-results

# Smoke tests only
pytest -m smoke --alluredir=allure-results

# Specific domain
pytest tests/api/products/ --alluredir=allure-results
pytest tests/ui/orders/ --alluredir=allure-results

# Integration (mock) tests
pytest tests/ui/integration/ -m integration --alluredir=allure-results

# Parallel execution
pytest tests/api/ -n auto --alluredir=allure-results

# With retries
pytest tests/ui/ --reruns 2 --reruns-delay 3 --alluredir=allure-results

# Dev environment
TEST_ENV=dev pytest tests/api/ --alluredir=allure-results
```

### Pytest markers

| Marker        | Description                  |
| ------------- | ---------------------------- |
| `smoke`       | Critical-path tests          |
| `regression`  | Full regression suite        |
| `api`         | API-only tests               |
| `ui`          | UI-only tests                |
| `integration` | UI + mock integration tests  |
| `e2e`         | End-to-end tests             |
| `products`    | Product-related tests        |
| `customers`   | Customer-related tests       |
| `orders`      | Order-related tests          |
| `managers`    | Manager-related tests        |
| `auth`        | Authentication-related tests |

---

## Viewing Reports

### Allure Report

```bash
# Generate report from results
allure generate allure-results -o allure-report --clean

# Open in browser
allure open allure-report

# Or use the Makefile shortcut
make report
```

The Allure report includes:

- **Step hierarchy** — `@allure.step()` decorators on service/page-object methods
- **Request/response attachments** — API calls with masked secrets
- **Screenshots** — automatically captured on UI test failure
- **Environment tab** — target URL and environment name
- **Test categorization** — via `@allure.suite()` / `@allure.sub_suite()`

### CI Report

After CI runs, the Allure report is published to GitHub Pages:  
🔗 https://aharashchuk.github.io/pytest_example/allure-report/

---

## CI/CD

Two GitHub Actions workflows are configured in `.github/workflows/`:

### `tests.yml` — Test Execution

- **Triggers:** push/PR to `main`, manual dispatch
- **Steps:**
  1. Checkout + install dependencies + Playwright browsers
  2. Run API regression tests (`pytest tests/api/`)
  3. Run UI regression tests (`pytest tests/ui/`)
  4. Generate Allure report
  5. Deploy report to GitHub Pages
  6. Send Telegram notification with results

### `build.yml` — Build Check

- **Triggers:** PRs to `main`
- **Steps:**
  1. Install dependencies
  2. Run `ruff check src/ tests/`
  3. Run `mypy src/ tests/`

### Required secrets

| Secret                 | Description               |
| ---------------------- | ------------------------- |
| `SALES_PORTAL_URL`     | AUT frontend URL          |
| `SALES_PORTAL_API_URL` | AUT backend API URL       |
| `USER_NAME`            | Admin login email         |
| `USER_PASSWORD`        | Admin login password      |
| `MANAGER_IDS`          | JSON array of manager IDs |
| `TELEGRAM_BOT_TOKEN`   | Telegram Bot API token    |
| `TELEGRAM_CHAT_ID`     | Telegram chat/channel ID  |

---

## Project Structure

```
├── .env.dist                          # Environment variable template
├── .github/
│   ├── copilot-instructions.md        # AI assistant coding guidelines
│   └── workflows/
│       ├── tests.yml                  # CI test execution pipeline
│       └── build.yml                  # PR lint/type-check gate
├── .pre-commit-config.yaml            # Ruff + mypy pre-commit hooks
├── pyproject.toml                     # Project metadata, deps, tool config
├── requirements.txt                   # Pinned dependencies
├── Makefile                           # Common command shortcuts
├── scripts/
│   └── notify_telegram.py             # CI Telegram notification helper
├── src/sales_portal_tests/            # Main package (installable)
│   ├── config/
│   │   ├── env.py                     # .env loading + exported constants
│   │   └── api_config.py             # API endpoint URLs + path functions
│   ├── api/
│   │   ├── api_clients/              # ApiClient Protocol + PlaywrightApiClient
│   │   ├── api/                      # Endpoint wrappers per domain
│   │   ├── service/                  # Business-level API services
│   │   │   └── stores/              # EntitiesStore (cleanup tracking)
│   │   └── facades/                  # Cross-domain orchestration
│   ├── ui/
│   │   ├── pages/                    # Page Objects hierarchy
│   │   └── service/                  # UI flow services
│   ├── mock/                         # Playwright route interception
│   ├── data/
│   │   ├── models/                   # Pydantic/dataclass models
│   │   ├── schemas/                  # JSON Schema dicts
│   │   ├── sales_portal/            # Enums, generators, DDT tables
│   │   ├── status_codes.py          # HTTP status code enum
│   │   └── tags.py                  # Test marker/tag constants
│   └── utils/                        # Validation, dates, reporting, etc.
├── tests/
│   ├── conftest.py                   # Root fixtures + Allure hooks
│   ├── api/
│   │   ├── conftest.py              # API-specific fixture notes
│   │   ├── test_login.py            # Login smoke test
│   │   ├── products/                # Product API test suites
│   │   ├── customers/               # Customer API test suites
│   │   └── orders/                  # Order API test suites
│   └── ui/
│       ├── conftest.py              # UI fixtures (auth, pages, services, mock)
│       ├── orders/                  # Order UI test suites
│       └── integration/             # Mock-based integration tests
└── sales-portal/                     # Application under test (Docker Compose)
```

---

## Key Conventions

### Imports

The package is installed as `sales_portal_tests` (via `src/` layout). Always import as:

```python
from sales_portal_tests.config.env import SALES_PORTAL_URL
from sales_portal_tests.data.status_codes import StatusCodes
```

Never use `from src.sales_portal_tests...`.

### Fixtures

- **`tests/conftest.py`** — session-scoped infra (API client, login, services, cleanup)
- **`tests/ui/conftest.py`** — UI fixtures (auth state, page objects, UI services, mock)
- `cleanup` fixture — yields a fresh `EntitiesStore` per test; auto-deletes tracked entities in teardown

### Validation

- **`validate_response()`** — soft-asserts on status, IsSuccess, ErrorMessage, optional schema
- **JSON Schema** — for contract-level "shape" assertions
- **Pydantic** — for typed data consumption in services
- **`pytest-check`** — for soft assertions (`check.equal()`, `check.is_true()`)

### Allure

- `@allure.step()` on service/page-object methods (no custom wrapper needed)
- `@allure.suite()` / `@allure.sub_suite()` on test classes
- Screenshots auto-attached on UI test failure via `pytest_runtest_makereport` hook

### Cleanup

```python
def test_something(cleanup: EntitiesStore, products_service, admin_token):
    product = products_service.create(admin_token)
    cleanup.products.add(product.id)
    # ... assertions ...
    # teardown: all tracked entities deleted automatically
```

---

## Development Environment (AUT)

The `sales-portal/` directory contains the full Sales Portal application:

- **Backend:** Express.js + MongoDB (port 8686)
- **Frontend:** Vanilla JS SPA (port 8585)
- **Database:** MongoDB 6.0 + Mongo Express UI (port 8081)

See the [Dev Environment Reference](./IMPLEMENTATION_PLAN_PYTHON.md#dev-environment-reference-sales-portal) in the implementation plan for the complete API route map, JSON schemas, validation rules, and enum values.
