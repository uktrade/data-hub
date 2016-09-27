import pytest

import functools
import os
import time
import urllib

import django
from django import apps as django_apps
from django.conf import settings as django_settings_module
from django.core.management import call_command as django_call_command
import psycopg2

import etl.target_models


SQL_PUBLIC_TABLE_NAMES = '''
SELECT table_name FROM information_schema.tables
    WHERE table_schema='public';
'''

SQL_TABLE_COUNTS = '''
SELECT relname, n_live_tup FROM pg_stat_user_tables
    ORDER BY n_live_tup DESC;
'''

def get_connection(url):
    while True:
        try:
            return psycopg2.connect(url)
        except psycopg2.OperationalError as exc:
            time.sleep(1)


def execute_ignore_existing(cursor, sql):
    try:
        cursor.execute(sql)
        cursor.connection.commit()
    except psycopg2.ProgrammingError as exc:
        if 'already exists' not in exc.pgerror:
            raise
        cursor.connection.rollback()

def truncate_public_tables(url):
    cursor = get_connection(url).cursor()
    cursor.execute(SQL_PUBLIC_TABLE_NAMES)
    public_table_names = cursor.fetchall()
    for (table_name,) in public_table_names:
        cursor.execute('TRUNCATE "{0}" CASCADE;'.format(table_name))
        cursor.connection.commit()
    table_counts = []
    for (table_name,) in public_table_names:
        cursor.execute('SELECT count(*) FROM "{0}"'.format(table_name))
        table_counts.append(cursor.fetchone())
    assert sum([count for (count,) in table_counts]) == 0


@pytest.yield_fixture
def tier0():
    'Mega-fixture for setting up tier0 databases, and cleaning them afterwards'
    print('For your information: Setup of tier0 db schemas commences')
    fixtures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    schema_fixtures = {
        os.environ['DATABASE_ODATA_URL']: (
            'test-create.sql', 'test-alter.sql'
        ),
        os.environ['DATABASE_URL']: ('test-django.sql',),
    }

    for url, filenames in schema_fixtures.items():
        cursor = get_connection(url).cursor()
        for name in filenames:
            with open(os.path.join(fixtures_path, name), 'r') as sql_fh:
                execute_ignore_existing(cursor, sql_fh.read())
        cursor.connection.close()


    class TargetModelsApp(django_apps.AppConfig):
        label = 'etl.target_models'


    django_db_url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

    django_settings = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'HOST': django_db_url.hostname,
                'NAME': django_db_url.path.lstrip('/'),
                'USER': django_db_url.username,
            }
        },
        'INSTALLED_APPS': [
            TargetModelsApp('etl.target_models', etl.target_models),
        ],
    }
    django_settings_module.configure(**django_settings)
    django.setup()
    yield
    for url in schema_fixtures.keys():
        truncate_public_tables(url)


@pytest.yield_fixture
def odata_fetchall():
    cursor = get_connection(os.environ['DATABASE_ODATA_URL']).cursor()

    def fetcher(sql):
        cursor.execute(sql)
        return cursor.fetchall()
    yield fetcher
    cursor.connection.close()
