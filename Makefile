.PHONY: dev lint typecheck test

dev:
	fastapi dev src/knowledge_api/main.py

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

test:
	uv run pytest

ALEMBIC = uv run alembic -c alembic.ini
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
	uv run fastapi dev src/knowledge_api/main.py --host 0.0.0.0 --port 8000 --reload

format:
	uv run ruff format .

install:
	uv sync

# ── E2E ───────────────────────────────────────────────────────────────────────

HURL_FILES = e2e/hurl/01_login.hurl \
	e2e/hurl/02_post_media.hurl \
	e2e/hurl/03_post_media_record.hurl \
	e2e/hurl/04_rate_limit.hurl

hurl-e2e:
	docker compose up --build -d
	@until curl -sf http://localhost:8000/docs > /dev/null 2>&1; do sleep 1; done
	$(ENV) hurl --test --jobs 1 \
		--variable host=http://localhost:8000 \
		--variable admin_login="$$ADMIN_LOGIN" \
		--variable admin_password="$$ADMIN_PASSWORD" \
		$(HURL_FILES); \
	status=$$?; \
	docker compose down -v; \
	exit $$status

.PHONY: up down up-db migrate downgrade migration makemigration run format lint install hurl-e2e