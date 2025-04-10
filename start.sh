#!/bin/sh

python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000
