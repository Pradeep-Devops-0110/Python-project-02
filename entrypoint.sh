#!/bin/sh
set -e

# Run database migrations if requested
if [ "$1" = "migrate" ]; then
    echo "Running database migrations..."
    flask --app flask_app.app:create_app db upgrade
    exit 0
fi

# Default: start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn -b 0.0.0.0:5000 "flask_app.app:create_app()"
