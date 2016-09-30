import functools

import elasticsearch
from elasticsearch import helpers as es_helpers
import sqlalchemy as sqla

from korben import services
from korben import config
from korben import etl


def row_es_add(table, es_id_col, row):
    'Create an ES `index` action from a database row'
    return {
        '_op_type': 'index',
        "_index": etl.spec.ES_INDEX,
        "_type": table.name,
        "_id": row[es_id_col],
        "_source": dict(row),
    }


def setup_index():
    '''
    Assume that if the index exists it is complete, otherwise create it and
    populate with mappings
    '''
    indices_client = elasticsearch.client.IndicesClient(
        client=services.es.client
    )
    if not indices_client.exists(etl.spec.ES_INDEX):
        indices_client.create(index=etl.spec.ES_INDEX)
        for doc_type, body in etl.spec.get_es_types().items():
            indices_client.put_mapping(
                doc_type=doc_type,
                body=body,
                index=etl.spec.ES_INDEX,
            )


def joined_select(table):
    fkey_data_cols = []
    joined = table
    # knock together the joins in a general, if rather assumptive manner
    for col in filter(lambda col: bool(col.foreign_keys), table.columns):
        fkey = next(iter(col.foreign_keys))  # assume fkeys
                                             # are non-composite
        # outer join is used here because data from cdms is incomplete
        # TODO: make scrape code more thorough, or maybe fix etl
        joined = joined.outerjoin(
            fkey.column.table,
            onclause=fkey.column.table.c.id == col  # assume join clause is
        )                                           # this simple
        # label column to lose `_id` suffix
        local_name = col.name[:-3]
        # potential remote column names
        potential_remotes = ('name', 'first_name')
        remote_column = None
        for remote_name in potential_remotes:
            try:
                remote_column = getattr(fkey.column.table.c, remote_name)
            except AttributeError:
                pass
        if remote_column is None:
            import ipdb;ipdb.set_trace()
            pass
        else:
            fkey_data_cols.append(remote_column.label(local_name))
    cols = list(filter(lambda col: not bool(col.foreign_keys), table.columns))
    return sqla.select(cols + fkey_data_cols, from_obj=joined)


def main():
    django_metadata = services.db.poll_for_metadata(config.database_url)
    setup_index()
    for name in etl.spec.DJANGO_LOOKUP:
        if name == 'company_companieshousecompany':
            continue
        table = django_metadata.tables[name]
        select = joined_select(table)
        rows = django_metadata.bind.execute(select).fetchall()
        actions = map(functools.partial(row_es_add, table, 'id'), rows)
        es_helpers.bulk(
            client=services.es.client,
            actions=actions,
            stats_only=True,
            chunk_size=1000,
            request_timeout=300,
        )

    # do ch company logic
    name = 'company_companieshousecompany'
    company_table = django_metadata.tables['company_company']
    result = django_metadata.bind.execute(
        sqla.select([company_table.columns['company_number']])
            .where(company_table.columns['company_number'] != None)
    ).fetchall()
    linked_companies = frozenset([x.company_number for x in result])
    table = django_metadata.tables[name]
    rows = django_metadata.bind.execute(table.select()).fetchall()
    filtered_rows = filter(
        lambda row: row.company_number in linked_companies, rows
    )
    actions = map(
        functools.partial(row_es_add, company_table, 'company_number'),
        filtered_rows
    )
    elasticsearch.helpers.bulk(
        client=services.es.client,
        actions=actions,
        stats_only=True,
        chunk_size=10,
        request_timeout=300,
        raise_on_error=True,
        raise_on_exception=True,
    )
