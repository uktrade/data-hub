import os
import time

from lxml import etree
import psycopg2
import requests

from odata_sql_schema import main as odata_sql_schema
from separate_constraints import main as separate_constraints

TEST_SERVICE_URL = 'http://services.odata.org/V2/(S(readwrite))/OData/OData.svc/'
ATTRIB_BASE = '{http://www.w3.org/XML/1998/namespace}base'


def get_connection():
    while True:
        try:
            return psycopg2.connect(os.environ['DATABASE_URL'])
        except psycopg2.OperationalError as exc:
            time.sleep(1)


def test_load_schema():
    'Test XML metadata can be split into valid CREATE and ALTER statements'
    cursor = get_connection().cursor()
    base_url = etree.fromstring(requests.get(TEST_SERVICE_URL).content).attrib[ATTRIB_BASE]
    with open('metadata.xml', 'wb') as metadata_fh:
        metadata_fh.write(requests.get(base_url + '$metadata').content)
    metadata_sql = odata_sql_schema('metadata.xml')
    create, alter = separate_constraints(metadata_sql)
    cursor.execute(create)
    cursor.execute(alter)
