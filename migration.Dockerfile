FROM python:3.15-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

RUN groupadd --system app \
    && useradd --system --gid app app \
    && chown -R app:app /app

COPY --chown=app:app alembic.ini ./
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app src ./src

USER app

ENTRYPOINT ["alembic", "upgrade", "head"]
