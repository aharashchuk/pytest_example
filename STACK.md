# Technology Stack & Architecture

> **Project:** AQA_4_PROD_SALES_PORTAL — End-to-end test automation framework for the Sales Portal web application  
> **Repository:** [github.com/DorityTM/AQA_4_PROD_SALES_PORTAL](https://github.com/DorityTM/AQA_4_PROD_SALES_PORTAL)  
> **Dev environment:** [`sales-portal/`](./sales-portal/) — full backend (Express + MongoDB) + frontend (vanilla JS) + Docker Compose setup

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

---

## 1. Overview

This project is a **Playwright + TypeScript** test-automation framework providing both **API** and **UI** test coverage for the Sales Portal product. It follows a multi-layered architecture separating low-level HTTP clients, business-level services, Page Objects, fixtures, data generation, and JSON-schema validation. Tests are organised by type (API / UI / integration) and tagged for selective execution (smoke, regression, etc.).

### Application Under Test (`sales-portal/`)

The Sales Portal development environment lives in the `sales-portal/` folder. Run it locally via Docker Compose:

```bash
cd sales-portal && docker-compose up --build
```

| Service       | URL                              | Notes                  |
| ------------- | -------------------------------- | ---------------------- |
| Frontend      | `http://localhost:8585`          | Vanilla JS SPA         |
| Backend API   | `http://localhost:8686`          | Express + MongoDB      |
| Swagger       | `http://localhost:8686/api/docs` | Full API documentation |
| Mongo Express | `http://localhost:8081`          | DB admin (admin/admin) |

Default admin credentials: `admin@example.com` / `admin123`

The backend serves a REST API under `/api` with JWT Bearer auth covering: Auth, Products, Customers, Orders (+ delivery, status, receive, comments, manager assignment), Notifications, Metrics, Users, and Rebates. Real-time notifications use Socket.IO. Request validation uses JSON Schema middleware + per-field regex validation.

---

## 2. Core Technologies

| Technology                 | Version (approx.) | Purpose                                                                           |
| -------------------------- | ----------------- | --------------------------------------------------------------------------------- |
| **TypeScript**             | 5.9               | Primary language; strict mode enabled                                             |
| **Node.js**                | 22+ (CI)          | Runtime environment                                                               |
| **Playwright Test**        | 1.57              | Test runner, browser automation, API request context                              |
| **CommonJS** module system | —                 | `"type": "commonjs"` in `package.json`; `"module": "nodenext"` in `tsconfig.json` |

---

## 3. Libraries & Dependencies

### 3.1 Production Dependencies

| Library                              | Purpose                                                                                 |
| ------------------------------------ | --------------------------------------------------------------------------------------- |
| **@faker-js/faker** ^10.1            | Randomised test-data generation (products, customers, orders, delivery addresses, etc.) |
| **ajv** ^8.17 + **ajv-formats** ^3.0 | JSON Schema validation of API response bodies                                           |
| **lodash** ^4.17                     | Utility belt — `_.omit`, `_.pick`, deep merge, etc.                                     |
| **moment** ^2.30                     | Date formatting / parsing (`YYYY/MM/DD`, `LLL`, ISO-8601 conversions)                   |
| **bson** ^7.0                        | `ObjectId` generation for mock / stub response data                                     |
| **dotenv** ^17.2                     | Loading `.env` / `.env.dev` files per environment                                       |
| **node-telegram-bot-api** ^0.67      | Sending test-run notifications to a Telegram chat                                       |

### 3.2 Dev Dependencies

| Library                                                                     | Purpose                                                    |
| --------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **@playwright/test** ^1.57                                                  | Test runner, assertions, fixtures, browser & API context   |
| **allure-playwright** ^3.4 + **allure-commandline** ^2.34                   | Allure reporting integration                               |
| **typescript** ^5.9                                                         | Compiler                                                   |
| **ts-node** ^10.9                                                           | On-the-fly TS execution                                    |
| **eslint** ^9.39 + **@typescript-eslint** ^8.48                             | Static analysis with TypeScript-aware rules                |
| **prettier** ^3.7 + **eslint-config-prettier** / **eslint-plugin-prettier** | Code formatting, integrated into ESLint                    |
| **husky** ^9.1                                                              | Git hooks (pre-commit)                                     |
| **lint-staged** ^16.2                                                       | Run linters on staged files only                           |
| **cross-env** ^7.0                                                          | Cross-platform env variable setting (e.g., `TEST_ENV=dev`) |
| **globals** ^16.5                                                           | ESLint globals for Node.js                                 |
| **jiti** ^2.6                                                               | ESM config loader (supports `eslint.config.mts`)           |

### 3.3 Type Definitions (dev)

`@types/bson`, `@types/dotenv`, `@types/lodash`, `@types/node`, `@types/node-telegram-bot-api`

---

## 4. Project Architecture

The framework follows a **multi-layer service-oriented architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                      Tests Layer                        │
│   src/tests/api/**    src/tests/ui/**    integration/** │
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
        │         Fixtures (DI Layer)         │
        │  api.fixture / pages.fixture / mock │
        │        merged via index.ts          │
        └───────────────┬─────────────────────┘
                        │
        ┌───────────────▼─────────────────────┐
        │       Data Layer                    │
        │  Types · Schemas · Generators · DDT │
        └─────────────────────────────────────┘
```

### Key Design Principles

- **Dependency Injection via Playwright Fixtures** — all API clients, services, page objects, and utilities are provided through `test.extend<>()` fixtures, enabling per-test isolation and automatic teardown.
- **Service / Facade Pattern** — business-level operations (create order with delivery, bulk creation, full cleanup) are encapsulated in service classes, keeping tests declarative.
- **Page Object Model (POM)** — every UI page/modal has a dedicated class; abstract base classes (`BasePage`, `SalesPortalPage`, `BaseModal`) handle common behaviours (spinners, toasts, cookies, request/response interception).
- **Data-Driven Testing (DDT)** — positive/negative test-case tables exported from `src/data/salesPortal/**` are iterated in `for...of` loops inside tests.
- **Schema Validation** — AJV JSON schemas are maintained per domain entity and applied via `validateResponse()`.

---

## 5. Layer-by-Layer Breakdown

### 5.1 API Client Layer (`src/api/apiClients/`)

| File               | Role                                                                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| `baseApiClient.ts` | Abstract class `BaseApiClient` implementing `IApiClient`; defines `send()` and `transformResponse()` contracts                        |
| `requestApi.ts`    | Concrete client wrapping Playwright's `APIRequestContext.fetch()`; auto-attaches request/response JSON to Allure steps; masks secrets |
| `types.ts`         | `IApiClient` interface                                                                                                                |

### 5.2 API Endpoint Wrappers (`src/api/api/`)

One class per domain entity, each accepting an `IApiClient` via constructor injection:

| File                   | Endpoints covered                                                                   |
| ---------------------- | ----------------------------------------------------------------------------------- |
| `login.api.ts`         | `POST /api/login`                                                                   |
| `products.api.ts`      | CRUD on `/api/products`                                                             |
| `customers.api.ts`     | CRUD + list/all on `/api/customers`                                                 |
| `orders.api.ts`        | CRUD, delivery, status, receive, assign/unassign manager, comments on `/api/orders` |
| `notifications.api.ts` | `/api/notifications`, mark-read                                                     |

Every public method uses the `@logStep()` decorator for automatic Allure step reporting.

### 5.3 API Services (`src/api/service/`)

Higher-level business flows built on top of API wrappers:

| Service               | Highlights                                                                                                                                   |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `LoginService`        | `loginAsAdmin()` — authenticates and returns a Bearer token                                                                                  |
| `ProductsApiService`  | `create()`, `update()`, `delete()`, `bulkCreate()`, `deleteAllProducts()` with built-in `validateResponse()`                                 |
| `CustomersApiService` | Similar CRUD + validation                                                                                                                    |
| `OrdersApiService`    | Orchestrates multi-step flows: `createOrderAndEntities()`, `createOrderWithDelivery()`, status transitions, full cleanup via `EntitiesStore` |
| `EntitiesStore`       | Tracks created entity IDs (`orders`, `customers`, `products`) in `Set<string>` for deterministic teardown                                    |

### 5.4 API Facades (`src/api/facades/`)

| Facade                | Purpose                                                                                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OrdersFacadeService` | Composes end-to-end order lifecycle (create → add delivery → process → receive → cancel) without internal response validation — used when tests need raw responses |

### 5.5 UI Page Objects (`src/ui/pages/`)

Inheritance chain:

```
BasePage  (cookie helpers, request/response interception)
  └─ SalesPortalPage  (spinner waits, toast locator, open(route), uniqueElement)
       ├─ BaseModal  (waitForClosed)
       ├─ HomePage, NavBar, LoginPage
       ├─ Products: ProductsListPage, AddNewProductPage, EditProductPage, DeleteModal, DetailsModal
       ├─ Customers: CustomersListPage, AddNewCustomerPage, DetailsModal
       └─ Orders: OrdersListPage, OrderDetailsPage, CreateOrderModal, EditProductsModal, Components/*
```

### 5.6 UI Services (`src/ui/service/`)

Each UI service composes one or more Page Objects for multi-step user flows:

`LoginUIService`, `HomeUIService`, `AddNewProductUIService`, `EditProductUIService`, `ProductsListUIService`, `AddNewCustomerUIService`, `CustomersListUIService`, `OrderDetailsUIService`, `CommentsUIService`, `AssignManagerUIService`

### 5.7 Mock Layer (`src/mock/`)

`Mock` class wraps `page.route()` for Playwright network interception, providing typed methods per page/modal: `productsPage()`, `ordersPage()`, `orderDetailsModal()`, `metricsHomePage()`, etc. Used in UI integration tests.

---

## 6. Test Strategy & Patterns

### 6.1 Test Organisation

```
src/tests/
  api/
    products/   (create, getById, getAllProducts, update, delete)
    customers/  (create, getById, getList, getAll, delete)
    orders/     (create, getById, update, delete, delivery, ordersStatus,
                 receive, comment, assignAndUnassignManager, notifications)
  ui/
    auth.setup.ts   (generates storageState for authenticated sessions)
    orders/         (createOrder, orderDetails, orderDelivery, comments,
                     exportOrders, navigation, assignManager, processing,
                     receiveProducts, refreshOrder, requestedProducts,
                     orderModals, updateCustomer)
    integration/    (ordersList, createOrder, updateCustomer — mock-based)
```

### 6.2 Playwright Projects

| Project            | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `setup`            | Runs `auth.setup.ts` to create `storageState` cookie file          |
| `sales-portal-ui`  | UI tests; depends on `setup`; uses stored auth; 1920×1080 viewport |
| `sales-portal-api` | API-only tests; no browser auth needed                             |
| `chromium`         | Headless Chrome alternative                                        |

### 6.3 Fixtures & Dependency Injection

| Fixture file          | Provides                                                                |
| --------------------- | ----------------------------------------------------------------------- |
| `api.fixture.ts`      | All API classes + services + `cleanup` registry with automatic teardown |
| `pages.fixture.ts`    | All Page Objects + UI Services                                          |
| `mock.fixture.ts`     | `Mock` class for network stubbing                                       |
| `business.fixture.ts` | `loginAsAdmin()` convenience helper                                     |
| `index.ts`            | Merges all fixture sets via `mergeTests(ui, api, mock)`                 |

### 6.4 Data-Driven Testing (DDT)

Test data files under `src/data/salesPortal/` export `*_POSITIVE_CASES` / `*_NEGATIVE_CASES` arrays of typed case objects (`ICaseApi`, `ICreateDeliveryCase`, etc.). Tests iterate them with `for...of`:

```ts
for (const [index, positiveCase] of CREATE_DELIVERY_POSITIVE_CASES.entries()) {
  test(`${positiveCase.title} [${index}]`, { tag: [...] }, async ({ ordersApi }) => { ... });
}
```

### 6.5 Data Generation

| Generator                | Uses                                                            |
| ------------------------ | --------------------------------------------------------------- |
| `generateProductData()`  | `@faker-js/faker` + `MANUFACTURERS` enum                        |
| `generateCustomerData()` | Faker, `COUNTRY` enum, sanitised strings                        |
| `generateDelivery()`     | Faker, `COUNTRY`/`DELIVERY_CONDITION` enums, `moment` for dates |
| `generateOrderData()`    | Composes customer + product IDs                                 |
| Mock response builders   | `bson.ObjectId` for realistic `_id` values                      |

### 6.6 Tagging

The `TAGS` enum (`src/data/tags.ts`) defines: `@smoke`, `@regression`, `@integration`, `@api`, `@ui`, `@e2e`, `@auth`, `@home`, `@products`, `@customers`, `@orders`, `@managers`.

Tags are passed via Playwright's native `{ tag: [...] }` option.

### 6.7 Validation

- **`validateResponse()`** — asserts `status`, `IsSuccess`, `ErrorMessage`, and optional JSON schema in one call using `expect.soft()`.
- **`validateJsonSchema()`** — compiles and validates response body against an AJV JSON schema.
- **JSON Schemas** — stored per domain under `src/data/schemas/` (products, customers, orders, delivery, login, users); share common fields from `core.schema.ts`.

### 6.8 Cleanup

- `EntitiesStore` tracks created entity IDs per test.
- The `cleanup` fixture in `api.fixture.ts` auto-calls `ordersApiService.fullDelete(token)` in teardown, deleting orders → products → customers.
- UI tests that create data via API activate teardown with: `test.beforeEach(async ({ cleanup }) => { void cleanup; });`

---

## 7. Configuration & Environment

### 7.1 Environment Variables

Loaded from `.env` (default) or `.env.dev` (when `TEST_ENV=dev`):

| Variable               | Description                   | Local default (Docker Compose) |
| ---------------------- | ----------------------------- | ------------------------------ |
| `SALES_PORTAL_URL`     | UI base URL                   | `http://localhost:8585`        |
| `SALES_PORTAL_API_URL` | API base URL                  | `http://localhost:8686`        |
| `USER_NAME`            | Test user email               | `admin@example.com`            |
| `USER_PASSWORD`        | Test user password            | `admin123`                     |
| `MANAGER_IDS`          | JSON array of manager UUIDs   |                                |
| `TELEGRAM_BOT_TOKEN`   | (optional) Telegram bot token |                                |
| `TELEGRAM_CHAT_ID`     | (optional) Telegram chat ID   |                                |

### 7.2 TypeScript Configuration

| Setting                                        | Value                                                       |
| ---------------------------------------------- | ----------------------------------------------------------- |
| `baseUrl`                                      | `src` (enables absolute imports like `data/...`, `api/...`) |
| `target`                                       | `esnext`                                                    |
| `module`                                       | `nodenext`                                                  |
| `strict`                                       | `true`                                                      |
| `noUncheckedIndexedAccess`                     | `true`                                                      |
| `exactOptionalPropertyTypes`                   | `true`                                                      |
| `sourceMap` / `declaration` / `declarationMap` | `true`                                                      |

### 7.3 API Config

`src/config/apiConfig.ts` centralises all endpoint paths as a typed object with static strings and parameterised functions:

```
/api/login, /api/logout, /api/products, /api/products/all, /api/products/:id,
/api/customers, /api/customers/all, /api/customers/:id, /api/customers/:customerId/orders,
/api/orders, /api/orders/:id, /api/orders/:id/delivery, /api/orders/:id/status,
/api/orders/:id/receive, /api/orders/:id/comments, /api/orders/:id/comments/:commentId,
/api/orders/:orderId/assign-manager/:managerId, /api/orders/:orderId/unassign-manager,
/api/notifications, /api/notifications/:notificationId/read, /api/notifications/mark-all-read,
/api/metrics, /api/users, /api/users/:id, /api/users/password/:id, /api/promocodes/:id
```

> **Source of truth:** `sales-portal/backend/routers/` — see Swagger at `http://localhost:8686/api/docs` for the live interactive documentation.

---

## 8. Linting, Formatting & Git Hooks

### 8.1 ESLint

- Flat config (`eslint.config.mts`) using `typescript-eslint` + `prettier` plugin.
- Key rules: `eqeqeq: error`, `@typescript-eslint/no-floating-promises: error`, strict equality, no unused expressions.
- Targets `src/**/*.{js,mjs,cjs,ts}`.

### 8.2 Prettier

`.prettierrc`: `printWidth: 120`, `singleQuote: false`, `trailingComma: "all"`, `semi: true`.

### 8.3 Git Hooks (Husky + lint-staged)

- **Pre-commit hook** runs `npx lint-staged`.
- **lint-staged** on `*.ts` files: TypeScript build check → ESLint fix → Prettier fix.

---

## 9. CI/CD Pipeline

### 9.1 Build Check (`build.yml`)

- Triggered on **pull requests** to `main`.
- Steps: checkout → Node 22 → `npm ci` → `npx tsc --noEmit`.

### 9.2 Test Run + Report (`tests.yml`)

- Triggered on **push/PR to `main`** + manual `workflow_dispatch`.
- Runs inside official Playwright Docker image (`mcr.microsoft.com/playwright:v1.57.0-noble`).
- Steps:
  1. Checkout
  2. Install OpenJDK 17 (for Allure CLI)
  3. `npm ci`
  4. Run API regression tests (`npm run test:api:regression`)
  5. Run UI regression tests (`npm run test:ui:regression`)
  6. Generate Allure report
  7. Deploy to **GitHub Pages** (`peaceiris/actions-gh-pages@v3`)
  8. Send **Telegram notification** with link to deployed report

---

## 10. Reporting & Notifications

### 10.1 Reporters

| Reporter                         | Output                                                                                            |
| -------------------------------- | ------------------------------------------------------------------------------------------------- |
| **HTML** (built-in)              | `playwright-report/` — interactive Playwright report                                              |
| **Allure** (`allure-playwright`) | `allure-results/` → `allure-report/` — rich test report with steps, attachments, environment info |

### 10.2 Allure Integration

- Every API request/response is automatically attached to the Allure step (JSON body, masked secrets).
- The `@logStep()` TypeScript **method decorator** wraps service/page-object methods in `test.step()` for hierarchical Allure step trees.
- Environment info (ENV, UI_URL, API_URL) is embedded in the Allure report.

### 10.3 Trace, Screenshot & Video

| Artifact   | When captured                                |
| ---------- | -------------------------------------------- |
| Trace      | Always (`trace: "on"`)                       |
| Screenshot | On failure (`screenshot: "only-on-failure"`) |
| Video      | On first retry (`video: "on-first-retry"`)   |

### 10.4 Telegram Notifications

- `TelegramService` wraps `node-telegram-bot-api` behind an `INotificationService` interface (Strategy pattern).
- CI sends a curl-based Telegram message after report deployment.

---

## 11. Directory Reference

```
AQA_4_PROD_SALES_PORTAL/
├── .github/
│   ├── copilot-instructions.md
│   └── workflows/
│       ├── build.yml              # PR build check
│       └── tests.yml              # Full test run + deploy
├── .husky/pre-commit              # lint-staged hook
├── .prettierrc                    # Prettier config
├── eslint.config.mts              # ESLint flat config
├── lint-staged.config.js          # Pre-commit tasks
├── package.json
├── playwright.config.ts           # Projects, reporters, tracing
├── tsconfig.json                  # Strict TS, baseUrl=src
│
├── src/
│   ├── .auth/user.json            # Generated storage state
│   │
│   ├── config/
│   │   ├── env.ts                 # Environment variables
│   │   └── apiConfig.ts           # API base URL + all endpoint paths
│   │
│   ├── api/
│   │   ├── apiClients/            # HTTP client abstraction
│   │   │   ├── baseApiClient.ts   #   Abstract base
│   │   │   ├── requestApi.ts      #   Playwright APIRequestContext implementation
│   │   │   └── types.ts           #   IApiClient interface
│   │   ├── api/                   # Endpoint wrapper classes
│   │   │   ├── login.api.ts
│   │   │   ├── products.api.ts
│   │   │   ├── customers.api.ts
│   │   │   ├── orders.api.ts
│   │   │   └── notifications.api.ts
│   │   ├── service/               # Business-level API services
│   │   │   ├── login.service.ts
│   │   │   ├── products.service.ts
│   │   │   ├── customer.service.ts
│   │   │   ├── orders.service.ts
│   │   │   └── stores/
│   │   │       └── entities.store.ts  # Tracks IDs for cleanup
│   │   └── facades/
│   │       └── ordersFacade.service.ts  # End-to-end order lifecycle
│   │
│   ├── ui/
│   │   ├── pages/                 # Page Object Model
│   │   │   ├── base.page.ts       #   Abstract: interception, cookies
│   │   │   ├── salesPortal.page.ts #  Abstract: spinners, navigation
│   │   │   ├── base.modal.ts      #   Abstract: modal close wait
│   │   │   ├── home.page.ts
│   │   │   ├── navbar.component.ts
│   │   │   ├── login/login.page.ts
│   │   │   ├── products/          #   List, Add, Edit, Delete, Details
│   │   │   ├── customers/         #   List, Add, Details
│   │   │   └── orders/            #   List, Details, Create, Edit, Components
│   │   └── service/               # UI flow services
│   │       ├── login.ui-service.ts
│   │       ├── home.ui-service.ts
│   │       ├── addNewProduct.ui-service.ts
│   │       ├── editProduct.ui-service.ts
│   │       ├── productsList.ui-service.ts
│   │       ├── addNewCustomer.ui-service.ts
│   │       ├── customersList.ui-service.ts
│   │       ├── orderDetails.ui-service.ts
│   │       ├── comments.ui-service.ts
│   │       └── assignManager.ui-service.ts
│   │
│   ├── mock/
│   │   └── mock.ts                # Playwright route() wrappers
│   │
│   ├── fixtures/
│   │   ├── api.fixture.ts         # API DI + cleanup teardown
│   │   ├── pages.fixture.ts       # Page Object DI
│   │   ├── mock.fixture.ts        # Mock DI
│   │   ├── business.fixture.ts    # Convenience login fixture
│   │   └── index.ts               # mergeTests(ui, api, mock)
│   │
│   ├── data/
│   │   ├── tags.ts                # TAGS enum (@smoke, @regression, …)
│   │   ├── statusCodes.ts         # STATUS_CODES enum (200, 201, 204, …)
│   │   ├── types/                 # TypeScript interfaces & types
│   │   │   ├── core.types.ts      #   IRequestOptions, IResponse, IResponseFields, ICaseApi
│   │   │   ├── product.types.ts
│   │   │   ├── customer.types.ts
│   │   │   ├── order.types.ts
│   │   │   ├── delivery.types.ts
│   │   │   ├── credentials.types.ts
│   │   │   ├── metrics.types.ts
│   │   │   ├── notifications.types.ts
│   │   │   └── user.types.ts
│   │   ├── schemas/               # AJV JSON Schemas
│   │   │   ├── core.schema.ts
│   │   │   ├── products/    (create, get, getAllProducts, product)
│   │   │   ├── customers/   (create, getById, getList, getAllCustomers, update, customer)
│   │   │   ├── orders/      (create, get, getAllOrders, order)
│   │   │   ├── delivery/    (delivery)
│   │   │   ├── login/       (login)
│   │   │   └── users/       (user)
│   │   └── salesPortal/           # Test data & DDT case tables
│   │       ├── constants.ts
│   │       ├── country.ts, errors.ts, notifications.ts
│   │       ├── order-status.ts, delivery-status.ts
│   │       ├── products/    (generators, DDT: create/update/delete/getById/getAll, manufacturers)
│   │       ├── customers/   (generators, DDT: create/update/getById, invalidData, duplicatePayload)
│   │       └── orders/      (generators, DDT: create/update/delete/getById/delivery/status/receive/
│   │                          assign/comments/notifications, mock data, integration data)
│   │
│   ├── utils/
│   │   ├── validation/
│   │   │   ├── validateResponse.utils.ts   # Status + IsSuccess + ErrorMessage + schema
│   │   │   └── validateSchema.utils.ts     # AJV compile + validate
│   │   ├── report/
│   │   │   └── logStep.utils.ts            # @logStep() method decorator → test.step()
│   │   ├── notifications/
│   │   │   ├── notifications.service.ts    # INotificationService interface
│   │   │   └── telegram.service.ts         # Telegram bot implementation
│   │   ├── assertions/
│   │   │   └── confirmationModal.assert.ts # Reusable modal assertion helper
│   │   ├── files/
│   │   │   ├── csv.utils.ts                # CSV parser (BOM, delimiter detection, quotes)
│   │   │   └── exportFile.utils.ts         # Download → save → parse (CSV/JSON)
│   │   ├── orders/helpers.ts               # Order-specific helpers
│   │   ├── date.utils.ts                   # moment-based date formatters
│   │   ├── enum.utils.ts                   # getRandomEnumValue()
│   │   ├── queryParams.utils.ts            # Object → URL query string converter
│   │   ├── maskSecrets.ts                  # Redact passwords/tokens in logs
│   │   └── log.utils.ts                    # Conditional console.log
│   │
│   └── tests/
│       ├── api/
│       │   ├── products/   (create, getById, getAllProducts, update, delete)
│       │   ├── customers/  (create, getById, getList, getAll, delete)
│       │   └── orders/     (create, getById, update, delete, delivery, ordersStatus,
│       │                    receive, comment, assignAndUnassignManager, notifications)
│       └── ui/
│           ├── auth.setup.ts     # Storage state generation
│           ├── orders/           (createOrder, orderDetails, orderDelivery, comments,
│           │                      exportOrders, navigation, assignManager, processing,
│           │                      receiveProducts, refreshOrder, requestedProducts,
│           │                      orderModals, updateCustomer)
│           └── integration/      (ordersList, createOrder, updateCustomer — mock-based)
│
├── allure-results/                # Raw Allure data
├── allure-report/                 # Generated Allure HTML report
├── playwright-report/             # Playwright HTML report
└── test-results/                  # Playwright test artifacts (traces, screenshots, videos)
```

---

## Summary of Design Patterns

| Pattern                     | Where Applied                                                                      |
| --------------------------- | ---------------------------------------------------------------------------------- |
| **Page Object Model (POM)** | `src/ui/pages/` — abstract base chain + domain pages/modals                        |
| **Service Layer**           | `src/api/service/` and `src/ui/service/` — business flows                          |
| **Facade**                  | `src/api/facades/` — simplified multi-step API operations                          |
| **Strategy**                | `INotificationService` → `TelegramService`                                         |
| **Dependency Injection**    | Playwright `test.extend<>()` fixtures                                              |
| **Data-Driven Testing**     | Exported case-table arrays iterated in spec files                                  |
| **Builder / Factory**       | `generate*Data()` functions with optional overrides                                |
| **Decorator**               | `@logStep()` — TypeScript method decorator for Allure reporting                    |
| **Repository / Store**      | `EntitiesStore` — tracks created entities for teardown                             |
| **Template Method**         | `BasePage` / `SalesPortalPage` abstract methods (`uniqueElement`, `waitForOpened`) |
