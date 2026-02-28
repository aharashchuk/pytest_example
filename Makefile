.PHONY: test-api test-ui test-smoke test-all test-integration lint report clean help

# Default target
help: ## Show this help message
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# ---------------------------------------------------------------------------
# Test targets
# ---------------------------------------------------------------------------

test-api: ## Run API smoke + regression tests
	pytest tests/api/ -m "smoke or regression" --alluredir=allure-results

test-ui: ## Run UI smoke + regression tests
	pytest tests/ui/ -m "smoke or regression" --alluredir=allure-results

test-smoke: ## Run smoke tests only (API + UI)
	pytest -m smoke --alluredir=allure-results

test-all: ## Run all tests
	pytest --alluredir=allure-results

test-integration: ## Run integration (mock) tests
	pytest tests/ui/integration/ -m integration --alluredir=allure-results

test-api-parallel: ## Run API tests in parallel
	pytest tests/api/ -m "smoke or regression" -n auto --alluredir=allure-results

# ---------------------------------------------------------------------------
# Linting & type-checking
# ---------------------------------------------------------------------------

lint: ## Run ruff linter + mypy type checker
	ruff check src/ tests/
	mypy src/ tests/

lint-fix: ## Run ruff with auto-fix
	ruff check src/ tests/ --fix

format: ## Format code with ruff
	ruff format src/ tests/

# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

report: ## Generate and open Allure report
	allure generate allure-results -o allure-report --clean
	allure open allure-report

report-generate: ## Generate Allure report (without opening)
	allure generate allure-results -o allure-report --clean

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

clean: ## Remove generated artifacts
	rm -rf allure-results/ allure-report/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -e .
	playwright install --with-deps chromium

install-dev: ## Install dependencies including dev extras
	pip install -r requirements.txt
	pip install -e ".[dev]"
	playwright install --with-deps chromium
	pre-commit install
