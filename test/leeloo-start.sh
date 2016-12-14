#!/bin/bash -xe
python /app/leeloo/manage.py migrate
python /app/leeloo/manage.py loaddata /app/leeloo/fixtures/metadata.yaml
python /app/leeloo/manage.py loaddata /app/leeloo/fixtures/undefined.yaml
python /app/leeloo/manage.py collectstatic --noinput
pushd /app/leeloo
python /app/test/leeloo-setup.py
python /app/leeloo/manage.py runserver 0.0.0.0:8000
popd
