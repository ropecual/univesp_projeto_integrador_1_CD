#!/bin/sh

# Function to wait for the database
wait_for_db() {
    echo "Waiting for database..."
    # Attempt to connect using manage.py dbshell connection check
    # Loop until the check succeeds (exit code 0)
    until python manage.py shell -c "from django.db import connection; connection.ensure_connection()" > /dev/null 2>&1; do
      echo "Database is unavailable - sleeping"
      sleep 1
    done
    echo "Database is up!"
}

wait_for_db # Call the wait function

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate --noinput || { echo "Migrations failed"; exit 1; }

# Collect static files
# Added --clear to ensure old files are removed
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || { echo "Collectstatic failed"; exit 1; }

# Create superuser using the standard command (more robust)
echo "Creating superuser (if necessary)..."
export DJANGO_SUPERUSER_USERNAME=administrador
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=A123456b # Ensure you use this password to log in

# Check if user exists first using Django shell, exit with 1 if not exists, 0 if exists
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exists = User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists(); import sys; sys.exit(0) if exists else sys.exit(1)"

# $? holds the exit status of the last command
if [ $? -eq 1 ]; then
    # User does not exist, attempt to create
    python manage.py createsuperuser --noinput || { echo "Superuser creation failed"; exit 1; }
    echo "Superuser '${DJANGO_SUPERUSER_USERNAME}' created."
else
    # User already exists
    echo "Superuser '${DJANGO_SUPERUSER_USERNAME}' already exists."
fi

# Start the Django development server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000