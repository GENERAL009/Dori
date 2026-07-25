#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! pg_isready -h postgres -p 5432 -U dori -q; do
  sleep 1
done
echo "PostgreSQL is ready."

echo "Running database migrations..."
alembic upgrade head || echo "Alembic migration skipped (tables may already exist)"

echo "Seeding database..."
python -m app.database.seed || echo "Seed skipped (may already exist)"

echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
