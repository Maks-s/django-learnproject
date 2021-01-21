#!/bin/bash

python manage.py compress
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py runserver
