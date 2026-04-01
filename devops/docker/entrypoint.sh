#!/bin/sh

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}
WAIT_TIMEOUT=${WAIT_TIMEOUT:-30}

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
/wait-for-it.sh "$DB_HOST:$DB_PORT" --timeout=$WAIT_TIMEOUT --strict -- echo "Postgres is up!"

# Optional: wait for Redis if your app depends on it
if [ -n "$REDIS_HOST" ]; then
  echo "Waiting for Redis at $REDIS_HOST:$REDIS_PORT..."
  /wait-for-it.sh "$REDIS_HOST:$REDIS_PORT" --timeout=$WAIT_TIMEOUT --strict -- echo "Redis is up!"
fi

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
API_HOST=${API_HOST:-0.0.0.0}
API_PORT=${API_PORT:-8000}

exec uvicorn app.main:app --host "$API_HOST" --port "$API_PORT" --reload