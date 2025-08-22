#!/bin/bash
source /var/app/venv/*/bin/activate

echo "=== EB postdeploy: collecting static files ==="
python /var/app/current/manage.py collectstatic --noinput

echo "=== EB postdeploy: running migrations ==="
python /var/app/current/manage.py migrate --noinput
