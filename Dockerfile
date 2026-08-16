FROM ghcr.io/astral-sh/uv:python3.14-trixie

WORKDIR /app
ENV PYTHONPATH=/app/src/knowledge_api

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY alembic.ini ./
COPY src ./src

CMD ["uv", "run", "fastapi", "run", "src/knowledge_api/main.py", "--host", "0.0.0.0", "--port", "8000"]
