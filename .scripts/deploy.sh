#!/bin/bash
set -e

echo "Deployment started ..."

cd /home/suresh/project/cms_backend

# Pull latest code
git fetch origin
git reset --hard origin/main
echo "New changes copied to server !"

# Install system dependencies for psycopg2
sudo apt-get install -y libpq-dev python3-dev

# Activate virtual environment
source my_env/bin/activate
echo "Virtual env 'my_env' Activated !"

# Install Python dependencies
echo "Installing Dependencies..."
pip install -r requirements.txt

# Django commands
python manage.py migrate
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart gunicorn

echo "Deployment complete!"