#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
python manage.py create_default_admin
gunicorn FinansTakip.wsgi:application
