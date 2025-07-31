#!/bin/sh

sleep 2 #solution to ensure that the database is ready #programming like a senior TOOD: pg_isready

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
