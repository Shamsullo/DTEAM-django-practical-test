#!/bin/bash

set -e
set -x

echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Applying database migrations..."
poetry run python manage.py migrate --noinput

# Load fixtures
poetry run python manage.py loaddata fixtures/*.json

echo "Running collectstatic..."
poetry run python manage.py collectstatic --noinput