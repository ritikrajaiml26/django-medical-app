#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations and collect static files
if [ -f "backend/manage.py" ]; then
    python backend/manage.py collectstatic --no-input
    python backend/manage.py migrate
elif [ -f "manage.py" ]; then
    python manage.py collectstatic --no-input
    python manage.py migrate
fi
