#!/bin/bash
set -e

export LANGUAGE="en_GB.UTF-8"
export LANG="en_GB.UTF-8"
export LC_ALL="en_GB.UTF-8"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE cdms_psql;
    GRANT ALL PRIVILEGES ON DATABASE cdms_psql TO $POSTGRES_USER;
EOSQL
