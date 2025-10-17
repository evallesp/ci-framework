# Makefile for project automation
.PHONY: help install dev-setup test lint format clean run dev docs

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
VENV := venv
SRC_DIR := src
TESTS_DIR := tests
DOCS_DIR := docs

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

## help: Display this help message
help:
	@echo "$(BLUE)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

## install: Install production dependencies
install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@echo "$(GREEN)Installation complete!$(NC)"

## dev-setup: Set up development environment
dev-setup: install
	@echo "$(BLUE)Setting up development environment...$(NC)"
	$(PIP) install -r dev-requirements.txt
	pre-commit install
	@echo "$(GREEN)Development environment ready!$(NC)"

## test: Run all tests
test:
	@echo "$(BLUE)Running tests...$(NC)"
	$(PYTEST) $(TESTS_DIR) -v

## test-unit: Run unit tests only
test-unit:
	@echo "$(BLUE)Running unit tests...$(NC)"
	$(PYTEST) $(TESTS_DIR)/unit/ -v

## test-integration: Run integration tests
test-integration:
	@echo "$(BLUE)Running integration tests...$(NC)"
	$(PYTEST) $(TESTS_DIR)/integration/ -v

## test-watch: Run tests in watch mode
test-watch:
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	pytest-watch $(TESTS_DIR)

## coverage: Run tests with coverage report
coverage:
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(PYTEST) --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(GREEN)Coverage report generated in htmlcov/index.html$(NC)"

## lint: Run all linters
lint: lint-python lint-yaml

## lint-python: Run Python linters
lint-python:
	@echo "$(BLUE)Running Python linters...$(NC)"
	ruff check $(SRC_DIR) $(TESTS_DIR)
	pylint $(SRC_DIR)
	mypy $(SRC_DIR)

## lint-yaml: Run YAML linter
lint-yaml:
	@echo "$(BLUE)Running YAML linter...$(NC)"
	yamllint .

## format: Auto-format code
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	black $(SRC_DIR) $(TESTS_DIR)
	isort $(SRC_DIR) $(TESTS_DIR)
	@echo "$(GREEN)Code formatted!$(NC)"

## type-check: Run type checking
type-check:
	@echo "$(BLUE)Running type checks...$(NC)"
	mypy $(SRC_DIR)

## security-scan: Run security scanning
security-scan:
	@echo "$(BLUE)Running security scan...$(NC)"
	bandit -r $(SRC_DIR)
	safety check

## clean: Remove build artifacts and cache files
clean:
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	@echo "$(GREEN)Clean complete!$(NC)"

## distclean: Remove all generated files including venv
distclean: clean
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	rm -rf $(VENV)/
	@echo "$(GREEN)Full clean complete!$(NC)"

## run: Run the application
run:
	@echo "$(BLUE)Starting application...$(NC)"
	$(PYTHON) -m myapp.main

## dev: Run application in development mode
dev:
	@echo "$(BLUE)Starting in development mode...$(NC)"
	DEBUG=true LOG_LEVEL=DEBUG $(PYTHON) -m myapp.main

## docs: Build documentation
docs:
	@echo "$(BLUE)Building documentation...$(NC)"
	cd $(DOCS_DIR) && make html
	@echo "$(GREEN)Documentation built in $(DOCS_DIR)/_build/html/$(NC)"

## docs-serve: Serve documentation locally
docs-serve: docs
	@echo "$(BLUE)Serving documentation at http://localhost:8080$(NC)"
	cd $(DOCS_DIR)/_build/html && $(PYTHON) -m http.server 8080

## docs-clean: Clean documentation build
docs-clean:
	@echo "$(BLUE)Cleaning documentation...$(NC)"
	cd $(DOCS_DIR) && make clean

## build: Build distribution packages
build: clean
	@echo "$(BLUE)Building distribution packages...$(NC)"
	$(PYTHON) -m build
	@echo "$(GREEN)Build complete! Packages in dist/$(NC)"

## install-dev: Install package in development mode
install-dev:
	@echo "$(BLUE)Installing in development mode...$(NC)"
	$(PIP) install -e .

## setup-hooks: Set up git hooks
setup-hooks:
	@echo "$(BLUE)Setting up git hooks...$(NC)"
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "$(GREEN)Git hooks installed!$(NC)"

## verify-setup: Verify development setup
verify-setup:
	@echo "$(BLUE)Verifying setup...$(NC)"
	@echo "Python version:"
	@$(PYTHON) --version
	@echo "\nPip version:"
	@$(PIP) --version
	@echo "\nInstalled packages:"
	@$(PIP) list
	@echo "\n$(GREEN)Verification complete!$(NC)"

## new-migration: Create new database migration
new-migration:
	@echo "$(BLUE)Creating new migration...$(NC)"
	alembic revision --autogenerate -m "$(m)"

## migrate: Run database migrations
migrate:
	@echo "$(BLUE)Running migrations...$(NC)"
	alembic upgrade head

## migrate-down: Rollback last migration
migrate-down:
	@echo "$(BLUE)Rolling back migration...$(NC)"
	alembic downgrade -1

## db-reset: Reset database (WARNING: destroys data)
db-reset:
	@echo "$(YELLOW)WARNING: This will destroy all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "$(BLUE)Resetting database...$(NC)"; \
		alembic downgrade base; \
		alembic upgrade head; \
		echo "$(GREEN)Database reset complete!$(NC)"; \
	fi

## container-build: Build container image
container-build:
	@echo "$(BLUE)Building container image...$(NC)"
	podman build -t myapp:latest .

## container-run: Run container
container-run:
	@echo "$(BLUE)Running container...$(NC)"
	podman run -p 8000:8000 myapp:latest

## quality: Run all quality checks
quality: lint type-check test coverage
	@echo "$(GREEN)All quality checks passed!$(NC)"

## pre-commit: Run pre-commit checks
pre-commit:
	@echo "$(BLUE)Running pre-commit checks...$(NC)"
	pre-commit run --all-files

## ci: Run CI checks locally
ci: quality security-scan
	@echo "$(GREEN)CI checks passed!$(NC)"



