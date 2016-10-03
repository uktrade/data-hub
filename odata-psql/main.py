import sys
from odata_sql_schema import main as odata_sql_schema
from separate_constraints import main as separate_constraints


def main(name_in, name_out=None):
    'Convert OData metadata.xml to SQL schema'
    create, alter = separate_constraints(odata_sql_schema(name_in))
    if not name_out:
        print(create)
        return
    with open("{0}-create.sql".format(name_out), 'w') as create_fh:
        create_fh.write(create)
    with open("{0}-alter.sql".format(name_out), 'w') as alter_fh:
        alter_fh.write(alter)

if __name__ == '__main__':
    main(*sys.argv[1:])
