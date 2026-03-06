# Architecture Review — Sales Portal Test Framework

> **Role:** Software Test Architect review
> **Date:** 2026-03-07
> **Scope:** Full codebase — architecture, stack, issues, and prioritised improvements

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Stack Assessment](#2-stack-assessment)
3. [Strengths](#3-strengths)
4. [Issues](#4-issues)
5. [Improvements (Prioritised)](#5-improvements-prioritised)
6. [Relationship to IMPROVEMENTS_PLAN.md](#6-relationship-to-improvements_planmd)

---

## 1. Architecture Overview

The framework is a **3-layer test architecture** with a clear separation of concerns:

```
tests/
  api/        ← API tests (HTTP-only, no browser)
  ui/         ← UI tests (browser-driven, real backend)
  ui/integration/ ← Integration tests (browser + mocked network)

src/sales_portal_tests/
  api/
    api/      ← Layer 1: Raw HTTP wrappers (one class per resource)
    service/  ← Layer 2: Business-level flows (create, drive to status, cleanup)
    facades/  ← [removed — was unused]
  ui/
    pages/    ← Page Object Model (one class per page/component)
    service/  ← UI service layer (orchestrates page objects for test flows)
  mock/       ← Playwright network interception helpers (integration tests only)
  data/
    models/   ← Pydantic response models
    schemas/  ← JSON Schema dicts for structural validation
    sales_portal/ ← Domain constants, enums, DDT fixtures
  config/     ← Env vars, API endpoint registry
  utils/      ← Shared helpers (validation, masking, reporting)
```

### Request flow (API tests)

```
Test → Service → Api wrapper → PlaywrightApiClient → Playwright APIRequestContext → Backend
                                     |
                              Allure attachment
                           (masked request + response)
```

### Request flow (UI tests)

```
Test → UI Service → Page Object → Playwright Page → Browser → Backend
                                        |
                             Auth state (session cookie)
```

### Request flow (Integration tests)

```
Test → UI Service → Page Object → Playwright Page → Mock.route() → Fake JSON response
                                                         (no real backend call)
```

---

## 2. Stack Assessment

| Component | Choice | Verdict |
|---|---|---|
| Language | Python 3.12 | Correct — modern typing, PEP 695 generics available |
| Test runner | pytest 9.x | Correct — mature, extensive plugin ecosystem |
| Browser automation | Playwright (sync) | Correct — fast, reliable, built-in network interception |
| HTTP client | Playwright `APIRequestContext` | Correct — eliminates dual-library fragmentation (`requests` + Playwright) |
| Data models | Pydantic v2 | Correct — strict validation, good IDE support |
| Test data generation | Faker | Correct — sufficient for the domain |
| Assertions | pytest-check (soft) + pytest `assert` | Correct — soft assertions collect all failures per test |
| Schema validation | jsonschema | Correct for structural checks; complements Pydantic parsing |
| Reporting | Allure | Correct — rich attachments, timeline view, environment tab |
| CI | GitHub Actions + Playwright Docker image | Correct — official image simplifies browser setup |
| Static analysis | mypy (strict) + ruff | Correct — catches issues before runtime |

**No gaps** in the core stack. The deliberate decision to use Playwright for both browser and API calls is architecturally sound and reduces dependencies.

---

## 3. Strengths

### Clean 3-layer separation
`api/api/` handles raw HTTP; `api/service/` encodes business flows; tests contain only intent.
The same pattern is mirrored in the UI layer (`ui/pages/` → `ui/service/`).
Each layer has a single responsibility and is independently testable.

### Single HTTP adapter
`PlaywrightApiClient` is the only HTTP client in the entire framework.
All requests flow through one path, making logging, masking, and retry logic easy to add in one place.

### EntitiesStore + cleanup fixture
The `cleanup` fixture yields an `EntitiesStore` that tests populate with IDs of created entities.
Teardown deletes all tracked entities automatically, even when tests fail.
This prevents test pollution without requiring each test to manage its own teardown.

### Soft assertions throughout
`validate_response()` uses `pytest-check` for every check.
A test with 3 failing assertions reports all 3, not just the first.

### Integration test layer with network mocking
`Mock` wraps `page.route()` to intercept specific endpoints and return programmed responses.
Integration tests verify UI behaviour (error toasts, auth redirects, dropdown population) without a running backend.
This is rare and valuable — fast, deterministic, no shared state.

### Secret masking in Allure
`mask_secrets()` redacts `Authorization` and `password` fields before attaching request/response JSON to Allure.
Security-aware by default.

### Session-scoped auth
Login happens once per session, the token and browser auth state are reused across all tests.
UI tests restore browser cookies from a saved state file — each test starts already authenticated.

---

## 4. Issues

Issues are rated **Critical**, **Significant**, or **Minor**.

---

### Critical

#### C1 — `telegram_service.py` was incorrectly deleted; CI is now broken

`scripts/notify_telegram.py` imports `TelegramService` directly:

```python
from sales_portal_tests.utils.notifications.telegram_service import TelegramService
```

The file was removed in a dead-code cleanup pass because it had no imports in the _test_ codebase.
However, it is used by the CI script, which is executed as a separate process via:

```yaml
- name: Telegram notification
  run: python scripts/notify_telegram.py --report-url "..." --env "default"
```

**Effect:** every CI run fails at the "Telegram notification" step with an `ImportError`.
**Fix:** restore `telegram_service.py` (and keep `notification_service.py` alongside it).

---

#### C2 — `continue-on-error: true` makes CI status meaningless

Both test steps in `tests.yml` have `continue-on-error: true`:

```yaml
- name: Run API regression tests
  run: pytest tests/api/ ...
  continue-on-error: true

- name: Run UI regression tests
  run: pytest tests/ui/ ...
  continue-on-error: true
```

The pipeline always shows green regardless of how many tests fail.
Failures are only visible inside the Allure report, which requires a manual click to inspect.
This eliminates the value of CI as a quality gate.

**Fix:** remove `continue-on-error: true`. If the goal is to always publish the Allure report even when tests fail, use `if: always()` on the publish step, not `continue-on-error` on the test steps.

---

#### C3 — CI step IDs are wrong; Telegram notification always reports empty counts

The notification step reads:

```yaml
PASSED: ${{ steps.run-api.outputs.passed }}
FAILED: ${{ steps.run-ui.outputs.failed }}
```

But the steps have no `id:` field, so `steps.run-api` does not exist.
Both variables are always empty strings. The notification is sent but contains no counts.

**Fix:** add `id: run-api` / `id: run-ui` to the test steps, or parse counts from pytest's exit code / a JUnit XML output.

---

#### C4 — Dual dependency management (`pyproject.toml` + `requirements.txt`) — silent drift

The CI installs from `requirements.txt` (`pip install -r requirements.txt`), a pinned lockfile.
`pyproject.toml` defines abstract version ranges as the "source of truth."
They are not generated from each other and diverge silently on every manual update.

Current divergences found:
- `requests==2.32.5` is in `requirements.txt`; `pyproject.toml` explicitly excludes `requests` with a comment
- `python-telegram-bot` was removed from `pyproject.toml` (during this session) but remains in `requirements.txt`

**Fix:** use `pip-compile` (from `pip-tools`) to generate `requirements.txt` from `pyproject.toml` automatically, and add a CI check that verifies they are in sync.

---

### Significant

#### S1 — Token expiry in long sessions

`admin_token` is a `session`-scoped fixture — the token is obtained once at session start and cached.
For long regression runs (30–60 min), the backend JWT may expire mid-session, causing all subsequent requests to return `401`, producing a cascade of misleading failures.

**Fix:** introduce a `TokenProvider` that re-authenticates lazily (or checks expiry before each request) rather than caching the raw string for the entire session.

---

#### S2 — Cleanup is not fault-tolerant

`OrdersApiService.full_delete()` calls `self.delete()`, which calls `validate_response()` and asserts a `204` response. If any entity was already deleted by the test itself, or if a delete returns a non-`204` (e.g., `404` because the entity never existed due to a failed setup), the cleanup raises an exception.

Consequences:
- Remaining entities in the store are not cleaned up (loop stops at first failure)
- The teardown error can mask the original test failure in the output

**Fix:** wrap each delete in `try/except`, log the failure, and continue cleanup regardless.

---

#### S3 — `create_order_in_status` duplicates logic from existing methods

The `PARTIALLY_RECEIVED` and `RECEIVED` branches in `create_order_in_status` manually repeat the `update_status` + `receive_products` steps that `create_partially_received_order()` and `create_received_order()` already encapsulate. If either method's logic changes, only one path gets updated.

**Fix:** delegate to the existing methods:

```python
if status == OrderStatus.PARTIALLY_RECEIVED:
    return self.create_partially_received_order(token, num_products)
if status == OrderStatus.RECEIVED:
    return self.create_received_order(token, num_products)
```

---

#### S4 — `_auth_headers()` copy-pasted across all five API files

The identical helper (and `_JSON_AUTH_HEADERS` constant) appears in:
`login_api.py`, `products_api.py`, `customers_api.py`, `orders_api.py`, `notifications_api.py`.

Any change to the auth header name or format requires updating five files.

**Fix:** extract to `api/api_clients/auth_headers.py` and import from there. Already documented in `IMPROVEMENTS_PLAN.md` Step 1.

---

### Minor

#### M1 — `data/tags.py` (`Tags` enum) is defined but never used

No test uses `@pytest.mark.Tags.*`. The enum adds noise without value.

**Fix:** wire it up as a marker alias, or remove it.

---

#### M2 — `ORDERS_ALL` endpoint defined in `api_config.py` but never referenced

`ORDERS_ALL: str = f"{BASE_URL}/api/orders/all"` exists but is not imported anywhere.

**Fix:** remove it.

---

#### M3 — Auth state path is a hardcoded relative string

```python
_AUTH_STATE_PATH = Path("src/.auth/user.json")
```

This depends on CWD being the repository root. It works in CI and standard local runs but silently breaks if pytest is invoked from a subdirectory.

**Fix:** anchor to the file's location:
```python
_AUTH_STATE_PATH = Path(__file__).parent.parent.parent / ".auth" / "user.json"
```

---

#### M4 — `notification_service.py` (Protocol) has no callers

`NotificationService` is a structural Protocol that `TelegramService` satisfies implicitly.
Nothing in the codebase type-checks against `NotificationService` — it is not used as a parameter type annotation anywhere.

**Fix (low priority):** either annotate the `scripts/notify_telegram.py` helper to accept `NotificationService` (making the Protocol meaningful), or remove it. Keep for now if a second notification backend (e.g., Slack) is planned.

---

## 5. Improvements (Prioritised)

### Priority 1 — Fix now (breaks CI or correctness)

| # | Action | File(s) |
|---|---|---|
| 1 | Restore `telegram_service.py` and `notification_service.py` | `src/sales_portal_tests/utils/notifications/` |
| 2 | Remove `continue-on-error: true` from test steps | `.github/workflows/tests.yml` |
| 3 | Add `id:` to test steps and fix Telegram notification variable references | `.github/workflows/tests.yml` |
| 4 | Sync `requirements.txt` with `pyproject.toml`; adopt `pip-compile` workflow | `requirements.txt`, `pyproject.toml` |

### Priority 2 — High value, manageable risk

| # | Action | Benefit |
|---|---|---|
| 5 | Extract `_auth_headers()` to shared module | Eliminates 5-way duplication |
| 6 | Make `full_delete()` fault-tolerant | Prevents cascading teardown failures |
| 7 | `TokenProvider` pattern for session token refresh | Eliminates token-expiry flakiness in long runs |
| 8 | Fix `create_order_in_status` — delegate to existing methods | Removes logic duplication, ensures consistency |

### Priority 3 — Architecture polish

| # | Action | Benefit |
|---|---|---|
| 9 | `JsonResponse` type alias for `dict[str, object]` | Removes `isinstance(body, dict)` noise, improves type safety |
| 10 | Anchor auth state path to `__file__` | Removes CWD dependency |
| 11 | Remove `ORDERS_ALL` unused constant | Reduces dead code |
| 12 | Wire or remove `Tags` enum | Removes misleading artifact |

### Priority 4 — Nice to have

| # | Action | Benefit |
|---|---|---|
| 13 | Faker seed control via pytest option | Reproducible test data on rerun |
| 14 | Dedicated `conftest.py` for `tests/ui/integration/` | Isolates integration fixtures from UI fixtures |
| 15 | CI parallel smoke target with `-n auto` | Faster feedback loop |

---

## 6. Relationship to IMPROVEMENTS_PLAN.md

`IMPROVEMENTS_PLAN.md` contains **LLM-executable, step-by-step implementation tasks** for a subset of the improvements above.
This document is the **high-level architectural view** — it includes issues not yet in the plan (C2, C3, C4, S2, S3, M2, M3) and provides the rationale behind each decision.

When implementing improvements, consult `IMPROVEMENTS_PLAN.md` for the exact code changes.
When evaluating scope or priority, consult this document.
