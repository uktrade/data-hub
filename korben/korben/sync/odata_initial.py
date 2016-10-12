'''
Parse database rows in the form of CSV files from response bodies, throw into
database
'''
import csv
import logging
import os


from korben import services
from korben import utils

LOGGER = logging.getLogger('korben.sync.populate')


def resp_csv(cache_dir, csv_dir, col_names, entity_name, page):
    entries = utils.parse_json_entries(cache_dir, entity_name, page)
    if entries is None:
        LOGGER.error('Unpickle of %s failed on page %s', entity_name, page)
        return None, None
    csv_path = os.path.join(csv_dir, page)
    if os.path.isfile(csv_path):
        return None, csv_path
    csv_fh = open(csv_path, 'w')
    writer = csv.DictWriter(csv_fh, col_names, dialect='excel')
    rowcount = 0
    for entry in entries:
        writer.writerow(utils.entry_row(col_names, entry))
        rowcount += 1
    csv_fh.close()
    return rowcount, csv_path


def entity_csv(cache_dir, col_names, entity_name, start=0):
    csv_dir = os.path.join(cache_dir, 'csv', entity_name)
    pages = list(
        filter(
            lambda P: int(P) >= start,
            sorted(
                os.listdir(os.path.join(cache_dir, 'json', entity_name)),
                key=int,
            )
        )
    )
    LOGGER.info('%s pages for %s', len(pages), entity_name)
    csv_paths = []
    rowcount = 0
    for page in pages:
        n_rows, csv_path = resp_csv(
            cache_dir, csv_dir, col_names, entity_name, page
        )
        if n_rows and csv_path:
            csv_paths.append(csv_path)
            rowcount += n_rows
        elif csv_path:
            csv_paths.append(csv_path)
            with open(csv_path) as csv_fh:
                for i, _ in enumerate(csv_fh):
                    pass
                rowcount += i + 1
    LOGGER.info('%s rows for %s', rowcount, entity_name)
    if len(pages) and not rowcount:
        raise Exception(csv_path)
    return csv_paths


def csv_psql(cursor, csv_path, table):
    LOGGER.info("Using COPY FROM on {0}".format(csv_path))
    with open(csv_path, 'r') as csv_fh:
        cursor.copy_expert(
            '''COPY "{0}" FROM STDIN DELIMITER ',' CSV'''.format(table.name),
            csv_fh
        )
        cursor.connection.commit()


def populate_entity(cache_dir, metadata, entity_name):
    os.makedirs(os.path.join(cache_dir, 'csv', entity_name), exist_ok=True)
    table = metadata.tables[entity_name]
    rowcount = metadata.bind.connect().execute(table.count()).scalar()
    col_names = [col.name for col in table.columns]
    csv_paths = entity_csv(cache_dir, col_names, entity_name, rowcount)
    for csv_path in csv_paths:
        try:
            cursor = metadata.bind.connection.cursor()
            csv_psql(cursor, csv_path, table)
        except Exception as exc:
            metadata.bind.connection.rollback()
            LOGGER.info('csv_psq call failed for %s', csv_path)
            LOGGER.error(exc)


def main(cache_dir='cache', entity_name=None, metadata=None):
    if not metadata:
        metadata = services.db.get_odata_metadata()
    if entity_name:
        populate_entity(cache_dir, metadata, entity_name)
        return
    for entity_name in os.listdir(os.path.join(cache_dir, 'json')):
        populate_entity(cache_dir, metadata, entity_name)