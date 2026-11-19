FROM python:3.15-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

RUN pip install --no-cache-dir uv

WORKDIR /app

CMD ["sh", "-c", "uv sync --locked && exec uvicorn src.app:app --host 0.0.0.0 --port ${PORT} --reload --reload-dir src"]
