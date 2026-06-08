#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
gunicorn FinansTakip.wsgi:application
