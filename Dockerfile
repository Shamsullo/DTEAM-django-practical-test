# Use ARM64-compatible Python image (better performance on M1/M2)
FROM python:3.12.6-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

# Install system dependencies (add any additional ones you need)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (recommended method, no separate virtualenv needed)
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy only dependency files first (for better caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies (disable virtualenvs inside Docker)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

# Copy the rest of the application
COPY . .
