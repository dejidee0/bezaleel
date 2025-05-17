#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install dependencies (to handle updates)
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

echo "Installing Puput Initial Data"
python manage.py puput_initial_data

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create a superuser if none exists
echo "Creating superuser if none exists..."
python manage.py create_superuser

# Start the server using gunicorn
echo "Starting gunicorn..."
gunicorn property.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
