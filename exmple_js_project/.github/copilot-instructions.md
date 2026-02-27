# Copilot instructions (AQA_4_PROD_SALES_PORTAL)

## Big picture

- This repo is a Playwright + TypeScript test framework with **API + UI** coverage.
- Tests live in `src/tests/` and are split by type: `src/tests/api/` vs `src/tests/ui/`.
- Core layers:
  - API:
    - `src/api/api/` (endpoint wrappers)
    - `src/api/apiClients/` (HTTP client abstractions: `BaseApiClient` / `RequestApi`)
    - `src/api/service/` (single-domain business flows)
    - `src/api/facades/` (cross-domain orchestration / facades)
  - UI:
    - `src/ui/pages/` (Page Objects)
    - `src/ui/service/` (higher-level UI flows)
  - Data: `src/data/` (types, JSON schemas, generators, DDT case tables)

## Golden rules (follow these first)

- Prefer repo fixtures (`fixtures/*`) over creating Playwright `request/page` clients manually.
- Don’t hardcode URLs, endpoints, timeouts, or status codes:
  - endpoints: `config/apiConfig.ts`
  - timeouts: `data/salesPortal/constants.ts`
  - status codes: `data/statusCodes.ts`
- Add Allure-friendly steps:
  - UI/services/pages: use the `@logStep()` decorator from `utils/report/logStep.utils.js` on public methods.
  - API calls already run inside `test.step(...)` via `RequestApi`.
- Keep lint happy:
  - **Always `await` promises** (`@typescript-eslint/no-floating-promises` is `error`).
  - Use strict equality only (`eqeqeq` is `error`).

## Developer workflows

- Install deps: `npm ci` (CI) or `npm install`, then `npx playwright install`.
- Env files:
  - Default loads `.env`; set `TEST_ENV=dev` to load `.env.dev` (see `playwright.config.ts`).
  - Required vars are read from `src/config/env.ts` (`SALES_PORTAL_URL`, `SALES_PORTAL_API_URL`, `USER_NAME`, `USER_PASSWORD`, plus `MANAGER_IDS` as JSON).
- Common commands (see `package.json`):
  - `npm run test:api` / `npm run test:ui`
  - `npm run test:dev` (loads `.env.dev`)
  - `npm run allure-report-open` / `npm run html-report-open`

## Playwright projects + auth

- Playwright projects are defined in `playwright.config.ts`.
- UI tests run under project `sales-portal-ui` and use `storageState: "src/.auth/user.json"`.
- The `setup` project generates this state in `src/tests/ui/auth.setup.ts` by logging in with `credentials`.

## Fixtures (import rules)

Prefer these imports (they match how this repo is written):

- API-only tests: `import { test, expect } from "fixtures/api.fixture"`
- UI-only tests and most integration UI flows: `import { test, expect } from "fixtures"`
  - `fixtures` merges UI + API + mock fixtures via `src/fixtures/index.ts`.
- Use `fixtures/pages.fixture` only if you truly need _just_ Page Objects and no API/mock.

Available fixture packs:

- `fixtures/api.fixture`: API clients + API services + `cleanup` registry
- `fixtures/pages.fixture`: Page Objects + UI services
- `fixtures/mock.fixture`: `mock` helper (Playwright routing/fulfill)
- `fixtures/business.fixture`: higher-level convenience flows like `loginAsAdmin()`

### Quick snippets (copy these patterns)

API-only test skeleton:

```ts
import { test, expect } from "fixtures/api.fixture";
import { TAGS } from "data/tags";
import { STATUS_CODES } from "data/statusCodes";
import { validateResponse } from "utils/validation/validateResponse.utils";

test.describe("[API][Domain][Action]", () => {
  test("does something", { tag: [TAGS.API] }, async ({ someApi }) => {
    const res = await someApi.someCall(/* ... */);
    validateResponse(res, { status: STATUS_CODES.OK, IsSuccess: true });
  });
});
```

UI/integration test skeleton (merged fixtures):

```ts
import { test, expect } from "fixtures";
import { TAGS } from "data/tags";

test.describe("[UI][Orders][Something]", () => {
  test.beforeEach(async ({ cleanup }) => {
    void cleanup; // activates API teardown when UI creates data via API
  });

  test("does something", { tag: [TAGS.UI] }, async ({ loginAsAdmin, ordersListPage }) => {
    await loginAsAdmin();
    await ordersListPage.waitForOpened();
  });
});
```

## How tests are written here

- API tests commonly use DDT case tables from `src/data/salesPortal/**`.
  - Example pattern: `src/data/salesPortal/orders/createDeliveryDDT.ts` exports `*_POSITIVE_CASES` and `*_NEGATIVE_CASES` arrays; tests loop them (see `src/tests/api/orders/delivery.spec.ts`).
- Tagging uses the `TAGS` enum in `src/data/tags.ts` and is passed via Playwright `test(..., { tag: [...] }, ...)`.

Naming conventions:

- Use bracketed suite names like: `test.describe("[API][Orders][Delivery]", ...)` or `"[UI][Orders][...]"`.
- Prefer stable tags from `data/tags.ts` (e.g. `[TAGS.SMOKE, TAGS.REGRESSION, TAGS.API]`).

## Validation + schemas

- Use `validateResponse()` from `src/utils/validation/validateResponse.utils.ts` to assert status/IsSuccess/ErrorMessage.
- When a JSON schema exists, pass it to `validateResponse({ schema: ... })`.
  - Schemas live under `src/data/schemas/**` (domain folders: products/customers/orders/delivery/users).

Conventions:

- Prefer `STATUS_CODES` from `data/statusCodes.ts` (avoid raw numbers like `200`).
- `validateResponse()` uses `expect.soft()` intentionally; don’t “upgrade” to hard assertions unless the test truly must stop immediately.

## Cleanup conventions (important)

- API fixture provides a per-test `cleanup` registry that auto-deletes tracked entities in teardown (see `src/fixtures/api.fixture.ts`).
- If a UI test creates data via API services, activate teardown by touching the fixture:
  - Pattern used in repo: `test.beforeEach(async ({ cleanup }) => { void cleanup; });`

Extra guidance:

- Prefer creating test data through API services/facades and registering ids via `cleanup.addProduct/addCustomer/addOrder`.
- `OrdersApiService` uses a per-test `EntitiesStore` to track entities; keep that pattern (don’t replace with globals).

## Project-specific TypeScript conventions

- TS path aliases assume `baseUrl: "src"` (see `tsconfig.json`), so imports are typically absolute like `data/...`, `api/...`, `ui/...`.
- With `module: nodenext`, some internal imports intentionally use a `.js` suffix (example: `utils/report/logStep.utils.js`); keep this style when adding new decorator usage.

## API architecture (how to add new endpoints)

- Define/extend endpoints in `config/apiConfig.ts` (single source of truth).
- Add endpoint wrapper methods in `src/api/api/*.api.ts`.
- Use `RequestApi` (`src/api/apiClients/requestApi.ts`) as the transport client — it wraps calls in `test.step` and attaches request/response to the report.
- Put per-domain flows in `src/api/service/*.service.ts`.
- Put cross-domain orchestration in `src/api/facades/*Facade*.ts` (example: `OrdersFacadeService`).

### New endpoint checklist

- [ ] Add endpoint path/function in `config/apiConfig.ts`.
- [ ] Add wrapper method in `src/api/api/<domain>.api.ts` using the existing `RequestApi` client.
- [ ] Add/extend a domain service in `src/api/service/<domain>.service.ts` if the test needs multi-step flows.
- [ ] For cross-domain flows (e.g., create order + product + customer), add/extend a facade in `src/api/facades/`.
- [ ] Use `validateResponse()` and schemas from `src/data/schemas/**`.
- [ ] Register entities in `cleanup` (or via service tracking) so teardown stays reliable.

## UI architecture (Page Objects + UI services)

- Page Objects live in `src/ui/pages/**`.
  - Reuse inheritance:
    - `BasePage` (common helpers and response interception)
    - `SalesPortalPage` (spinner/toast behavior + `uniqueElement` contract)
- UI flows live in `src/ui/service/**`.
- Prefer meaningful `@logStep("...")` messages on user actions and verifications.
- Use exported timeout constants from `data/salesPortal/constants.ts` (avoid magic numbers).

### Page Object + UI service checklist

- [ ] Page Objects should extend `BasePage` or `SalesPortalPage`.
- [ ] `SalesPortalPage` subclasses must define `uniqueElement`.
- [ ] Public methods should use `@logStep("...")` from `utils/report/logStep.utils.js`.
- [ ] Use timeouts from `data/salesPortal/constants.ts`.
- [ ] Prefer UI services (`src/ui/service/**`) for multi-step user flows.

## Test data patterns

- Prefer typed generators under `src/data/salesPortal/**/generate*.ts` using `@faker-js/faker`.
- Keep DDT tables (`*_POSITIVE_CASES`, `*_NEGATIVE_CASES`) in `src/data/salesPortal/**` and make them deterministic/stable where practical.

## Reporting/notifications

- Allure is configured in `playwright.config.ts`.
- CI posts a Telegram notification from the GitHub Actions workflow (see `.github/workflows/tests.yml`); locally you can use `TelegramService` from `src/utils/notifications/telegram.service.ts` when `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID` are set.
