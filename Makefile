.PHONY: dev lint typecheck test

dev:
	fastapi dev src/knowledge_api/main.py

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

test:
	uv run pytest

ALEMBIC = uv run alembic -c src/user/infrastructure/alembic.ini
ENV = set -a && . ./.env && set +a &&

# ── Docker ────────────────────────────────────────────────────────────────────

up:
	docker compose up --build

down:
	docker compose down

# ── Migrations ────────────────────────────────────────────────────────────────

migrate:
	$(ENV) $(ALEMBIC) upgrade head

downgrade:
	$(ENV) $(ALEMBIC) downgrade -1

# Usage: make migration MSG="Added users table"
migration:
	$(ENV) $(ALEMBIC) revision --autogenerate -m "$(MSG)"

# Usage: make makemigration MSG="Added users table"
makemigration:
	docker compose up postgres -d
	@until docker compose exec postgres pg_isready -U $$(. ./.env && echo $$POSTGRES_USER) > /dev/null 2>&1; do sleep 1; done
	$(ENV) $(ALEMBIC) upgrade head
	$(ENV) $(ALEMBIC) revision --autogenerate -m "$(MSG)"; \
	docker compose stop postgres

# ── Dev ───────────────────────────────────────────────────────────────────────

run:
	uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

format:
	uv run ruff format .

lint:
	uv run ruff check .

install:
	uv sync

.PHONY: up down up-db migrate downgrade migration makemigration run format lint install