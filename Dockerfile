FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install system deps needed by asyncpg / aiohttp
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

# Install dependencies first (cache layer)
COPY pyproject.toml poetry.lock* ./
RUN poetry install --only main --no-root

# Copy application source
COPY bot/ ./bot/

CMD ["python", "-m", "bot.main"]
