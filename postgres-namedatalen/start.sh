#!/bin/bash

chown -R postgres:postgres ${PGDATA}
if [ ! -e ${PGDATA}/PG_VERSION ]; then
    su postgres -c /usr/local/pgsql/bin/initdb ${PGDATA}
fi

su postgres -c "/usr/local/pgsql/bin/pg_ctl -D ${PGDATA} -o \"-c listen_addresses='localhost'\" -w start"
