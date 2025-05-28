SHELL := /bin/bash

# Project variables
APP_NAME := rag-fastpi-app
DOCKER_IMAGE_NAME ?= $(APP_NAME)
DOCKER_IMAGE_TAG ?= latest
APP_DIR = app


.PHONY: help
help: ## Show this help message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_0-9.-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# ==============================================================================
# DEVELOPMENT ENVIRONMENT
# ==============================================================================

.PHONY: setup
setup: ## 📦 Install project dependencies using uv
	@echo ">>> Installing dependencies from pyproject.toml..."
	@uv sync --all-groups
	@echo ">>> Dependencies intalled."

.PHONY: pre-commit-install
pre-commit-install: ## 🎣 Install pre-commit hooks
	@echo ">>> Installing pre-commit hooks..."
	@uv run pre-commit install
	@echo ">>> Pre-commit hooks installed."

# ==============================================================================
# CLEANING
# ==============================================================================

.PHONY: clean
clean: ## 🧹 Remove cache files and build artifacts
	@echo ">>> Cleaning project..."
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@rm -rf .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	# Add any other specific cache/build directories here
	@echo ">>> Project cleaned."

# ==============================================================================
# LINTING AND FORMATTING
# ==============================================================================

.PHONY: lint.fix
lint.fix: ## 💅 Format code and fix linting errors with Ruff
	@echo ">>> Formatting code with Ruff..."
	@uv run ruff format .
	@echo ">>> Fixing linting errors with Ruff..."
	@uv run ruff check --fix .
	@echo ">>> Linting and formatting complete."

.PHONY: lint.check
lint.check: ## 👀 Check code formatting and linting with Ruff (no changes made)
	@echo ">>> Checking code formatting with Ruff..."
	@uv run ruff format --check .
	@echo ">>> Checking linting with Ruff..."
	@uv run ruff check .
	@echo ">>> Linting checks complete."

.PHONY: type.check
type.check: ## 🧐 Perform static type checking with Pyright
	@echo ">>> Running Pyright type checker..."
	@uv run pyright
	@echo ">>> Type checking complete."

# ==============================================================================
# Testing
# ==============================================================================

.PHONY: test
test: ## 🧪 Run unit tests with coverage report
	@echo ">>> Running unit tests with coverage..."
	@uv run pytest --cov=$(APP_DIR)
	@echo ">>> Unit tests with coverage finished. Report in .test_results/."

# ==============================================================================
# APPLICATION & DOCKER
# ==============================================================================

.PHONY: run.app
run.app: ## 🚀 Run the FastAPI application locally using Uvicorn
	@echo ">>> Starting FastAPI application locally..."
	@uv run uvicorn app:build_service_app --reload --host 0.0.0.0 --port 8000 --log-level info

.PHONY: build.docker
build.docker: ## 🐳 Build the Docker image for the application
	@echo ">>> Building Docker image $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)..."
	@docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) .
	@echo ">>> Docker image built: $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)"

.PHONY: run.docker
run.docker: ## 🐳 Run the application using the Docker image
	@echo ">>> Running Docker container from image $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)..."
	@docker run -d -p 8000:8000 --name $(APP_NAME)-container $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	@echo ">>> Container $(APP_NAME)-container started. Access at http://localhost:8000/docs"
	@echo ">>> View logs with: docker logs -f $(APP_NAME)-container"

.PHONY: stop.docker
stop.docker: ## 🐳 Stop and remove the running Docker container
	@echo ">>> Stopping and removing Docker container $(APP_NAME)-container..."
	@-docker stop $(APP_NAME)-container 2>/dev/null || echo "Container $(APP_NAME)-container not running or already stopped."
	@-docker rm $(APP_NAME)-container 2>/dev/null || echo "Container $(APP_NAME)-container not found or already removed."
	@echo ">>> Docker container stopped and removed."

.PHONY: logs.docker
logs.docker: ## 🐳 View logs of the running Docker container
	@echo ">>> Tailing logs for container $(APP_NAME)-container..."
	@docker logs -f $(APP_NAME)-container
