#!/usr/bin/env bash
set -o errexit

pip install -r library_project/requirements.txt
cd library_project
python manage.py collectstatic --noinput
python manage.py migrate
