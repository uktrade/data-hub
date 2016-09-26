.PHONY: leeloo_tests leeloo_coverage leeloo_lint leeloo_migrate leeloo_makemigrations django_psql odata_psql

leeloo-tests:
	docker-compose run leeloo pytest -s

leeloo-coverage:
	docker-compose run leeloo pytest -s --cov=/app/leeloo --cov-report term-missing --cov-config .coveragerc

leeloo-lint:
	docker-compose run leeloo flake8

leeloo-migrate:
	docker-compose run leeloo python manage.py migrate

leeloo-runserver:
	docker-compose run leeloo python manage.py runserver 0.0.0.0:8000

leeloo-makemigrations:
	docker-compose run leeloo python manage.py makemigrations

leeloo-shellplus:
	docker-compose run leeloo python manage.py shell_plus --ipython

psql-django:
	docker-compose exec	 postgres-django psql -U postgres -d datahub

psql-odata:
	docker-compose exec postgres-odata psql -U postgres -d datahub_odata

import_companieshouse_companies:
	docker-compose run korben-sync-poll korben sync ch

sync_companyhouse:
	docker-compose run korben-sync-poll korben sync es-initial

PSQL_CSV_OUT = psql -P pager=off -t -A -F"," -U postgres

count-odata:
	docker-compose exec postgres-odata ${PSQL_CSV_OUT} -d datahub_odata -c "SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE n_live_tup > 0 ORDER BY n_live_tup DESC;"

count-django:
	docker-compose exec postgres-django ${PSQL_CSV_OUT} -d datahub -c "SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE n_live_tup > 0 ORDER BY n_live_tup DESC;"

test-odata-psql:
	cd odata-psql && docker-compose up --build test
