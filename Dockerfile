FROM python:3.15-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependencies
FROM base AS dependencies

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Runtime
FROM base AS dist

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

RUN groupadd --system app \
    && useradd --system --gid app app

COPY --chown=app:app --from=dependencies /app/.venv ./.venv
COPY --chown=app:app alembic.ini ./
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app src ./src

USER app

EXPOSE 3000

CMD ["sh", "-c", "exec uvicorn src.app:app --host 0.0.0.0 --port ${PORT}"]
