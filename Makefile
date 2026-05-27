.PHONY: dev lint typecheck test

dev:
	fastapi dev src/knowledge_api/main.py

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

test:
	uv run pytest
