# Data Hub backend

[![CircleCI](https://circleci.com/gh/uktrade/data-hub-backend/tree/master.svg?style=svg)](https://circleci.com/gh/uktrade/data-hub-backend/tree/master)

Repository for Data Hub backend. It contains due different components:

* Leeloo: Django app providing API to the Frontend
* Korben: Python app providing sync and ETL

## Installation

Datahub backend uses Docker compose to setup and run all the necessary components.

There are six Docker Compose files: four used in testing, one for production and one for local development.

* `docker-compose.yml`: production file
* `docker-compose-dummy-korben.yml`: local development file, it uses a dummy version of Korben
* `test-leeloo.yml`
* `test-korben-tier0.yml`
* `test-korben-tier1.yml`
* `test-korben-tier2.yml`

Build and run the necessary containers for the required environment:

    docker-compose -f {file.yml} up --build

### Env file

All the following environment variables must be set in a `.env` file, generate secrets using `$(openssl rand -base64 32)`

```
CDMS_ADFS_URL=https://test.com
CDMS_BASE_URL=https://test.com
CDMS_USERNAME=user
CDMS_PASSWORD=password
CDMS_COOKIE_KEY=secret
CDMS_RSTS_URL=https://test.com
CDMS_COOKIE_PATH=/path
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

Tests run automatically on Circle CI. To run test on local machine use the provided make commands:

    - make test-leeloo
    - make docker-cleanup
    - make test-odata-psql
    - make docker-cleanup
    - make test-korben-unit
    - make docker-cleanup
    - make test-korben-tier0

![Leeloo and Korben](leeloo-korben.jpg)
