FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY pyproject.toml poetry.lock* /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN chmod +x /code/scripts/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./scripts/entrypoint.sh"]
