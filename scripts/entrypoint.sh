#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate --no-input

if [ "$DJANGO_ENV" = "development" ]; then
  echo "Starting development server..."
  exec python manage.py runserver 0.0.0.0:8000
else
  echo "Collecting static files..."
  python manage.py collectstatic --no-input --clear
  echo "Starting Gunicorn (production)..."
  exec gunicorn --bind 0.0.0.0:8000 --workers 4 CVProject.wsgi:application
fi