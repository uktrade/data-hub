#!/bin/bash -xe
python /app/leeloo/manage.py dbwait
python /app/leeloo/manage.py migrate
python /app/leeloo/manage.py runserver_plus 0.0.0.0:8000
