# Data Hub

![Leeloo and Korben](leeloo-korben.jpg)

This repo contains docker-compose files for development and testing. To start,
do some submodules magic to pull in all the separate repos:

```
git submodule update --init
```


Repository for Data Hub backend. It contains the following components:

* Rhod: Browser client for Django app
* Leeloo: Django app providing API to the Frontend
* Korben: Python app providing sync and ETL for custom BAE-hosted Dynamics
  instance

## Installation

Datahub backend uses Docker compose to setup and run all the necessary components.

There are six Docker Compose files: four used in testing, one for production and one for local development.

* `docker-compose.yml`: development file
* `docker-compose-dummy-korben.yml`: local development file, it uses a dummy version of Korben
* `test-leeloo.yml`

Build and run the necessary containers for the required environment:

    docker-compose -f {file.yml} up --build


### Env file

All the following environment variables must be set in a `.env` file.
```
CDMS_ADFS_URL=https://test.com
CDMS_BASE_URL=https://test.com
CDMS_USERNAME=user
CDMS_PASSWORD=password
CDMS_COOKIE_KEY=secret
CDMS_RSTS_URL=https://test.com
CDMS_COOKIE_PATH=/path/to/cookie
ODATA_ENTITY_CONTAINER_KEY=secret
DATAHUB_SECRET=secret

ES_HOST=es
ES_PORT=9200
ES_INDEX=datahub
KORBEN_HOST=korben
KORBEN_PORT=8080
DJANGO_SECRET_KEY=changeme
DATABASE_URL=postgresql://postgres@postgres-django/datahub
DATABASE_ODATA_URL=postgresql://postgres@postgres-odata/datahub_odata
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=datahubapi.settings.local
DJANGO_SENTRY_DSN=sentry_dsn
CH_TOKEN=secret
```

### Management commands

If the database is freshly built or a new versioned model is added run:

    docker-compose -f {file.yml} run leeloo python manage.py createinitialrevisions

Load metadata:

    docker-compose -f {file.yml} run leeloo python manage.py loaddata /app/leeloo/fixtures/metadata.yaml
    docker-compose -f {file.yml} run leeloo python manage.py loaddata /app/leeloo/fixtures/undefined.yaml
    docker-compose -f {file.yml} run leeloo python manage.py loaddata /app/leeloo/fixtures/datahub_businesstypes.yaml

Apply migrations:
    
    docker-compose -f {file.yml} run leeloo python manage.py migrate
    
## Testings

Tests run automatically on Circle CI. To run test on
local machine use the provided shell script:

    - `test/jenkins.sh`

