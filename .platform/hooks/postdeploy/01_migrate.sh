#!/bin/bash
set -euo pipefail

# Activate the virtual environment
source /var/app/venv/*/bin/activate

echo "=== EB postdeploy: collecting static files ==="
python /var/app/current/manage.py collectstatic --noinput --clear

echo "=== EB postdeploy: running migrations ==="
python /var/app/current/manage.py migrate --noinput

echo "=== EB postdeploy: checking Django configuration ==="
python /var/app/current/manage.py check --deploy
