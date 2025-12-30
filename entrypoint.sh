#!/bin/bash
set -e

echo "Running database migrations..."
flask --app flask_app.app:create_app db upgrade

echo "Starting Gunicorn server..."
exec gunicorn -b 0.0.0.0:5000 "flask_app.app:create_app()"
