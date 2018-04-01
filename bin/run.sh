#!/bin/bash
python manage.py db upgrade
exec gunicorn -b :80 --access-logfile - manage:app --threads 4
