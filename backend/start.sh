#!/bin/bash
# start.sh - Script to run Redis, Celery worker, and start the Flask app.

# NOTE: Ensure Redis is installed.
# You can run redis with:
#   redis-server
# in a separate terminal, or use Docker:
#   docker run --name redis -p 6379:6379 -d redis

echo "Please ensure that Redis is running in a separate terminal."

# Start Celery worker in the background
echo "Starting Celery worker..."
celery -A backend.tasks worker --loglevel=info &

# Optionally, wait a few seconds to ensure Celery is running.
sleep 3

# Start the Flask application with auto migration via manage.py
echo "Starting Flask app via manage.py..."
python manage.py