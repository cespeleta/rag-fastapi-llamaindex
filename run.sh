#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Set default values for environment variables if they are not already set.
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}
LOG_LEVEL=${LOG_LEVEL:-info}
RELOAD_FLAG=""

# For development, set RELOAD=true
if [[ "${REALOAD,}" == "true" ]]; then
    RELOAD_FLAG="--reload"
    echo "Reloading is enabled."
fi

echo "Starting Uvicorn server..."
echo "Host: $HOST"
echo "Port: $PORT"
echo "Workers: $WORKERS"
echo "Log Level: $LOG_LEVEL"

# Run uvicorn server
exec /opt/venv/bin/uvicorn app.main:build_service_app \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level "$LOG_LEVEL" \
    $RELOAD_FLAG
