.PHONY: help setup infra-up infra-down dev-api dev-web dev-worker dev db-migrate db-revision test-api test-web test lint format docker-up docker-down clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Run setup-dev.sh
	@bash infrastructure/scripts/setup-dev.sh

infra-up: ## Start only infrastructure services (postgres, redis, minio)
	@cd infrastructure && docker-compose up -d postgres redis minio

infra-down: ## Stop infrastructure services
	@cd infrastructure && docker-compose down

dev-api: ## Run FastAPI dev server
	@cd apps/api && uvicorn ares.main:app --reload --port 8000

dev-web: ## Run Next.js dev server
	@cd apps/web && npm run dev

dev-worker: ## Run Celery worker
	@cd apps/api && celery -A ares.workers.celery_app worker --loglevel=info

dev: ## Run all dev services in parallel (requires multi-tab or tool like overmind)
	@echo "Starting all dev services using make jobs..."
	$(MAKE) -j3 dev-api dev-web dev-worker

db-migrate: ## Run Alembic migrations
	@cd apps/api && alembic upgrade head

db-revision: ## Create new Alembic revision
	@cd apps/api && alembic revision --autogenerate -m "auto"

test-api: ## Run pytest for backend
	@cd apps/api && pytest

test-web: ## Run vitest for frontend
	@cd apps/web && npm run test

test: test-api test-web ## Run all tests

lint: ## Run all linters
	@cd apps/api && ruff check . && mypy .
	@cd apps/web && npm run lint

format: ## Run all formatters
	@cd apps/api && ruff format .
	@cd apps/web && npm run format

docker-up: ## Full docker compose up (infra + apps)
	@cd infrastructure && docker-compose up --build -d

docker-down: ## Full docker compose down
	@cd infrastructure && docker-compose down

clean: ## Remove all containers, volumes, caches
	@cd infrastructure && docker-compose down -v --remove-orphans
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name "node_modules" -exec rm -rf {} +
	@find . -type d -name ".next" -exec rm -rf {} +
