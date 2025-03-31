FROM python:3.12-slim as base

RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 && \
    apt clean && \
    rm -rf /var/cache/apt/* \

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    netcat-openbsd \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN chmod +x /code/scripts/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./scripts/entrypoint.sh"]
