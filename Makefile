.PHONY: leeloo_tests leeloo_coverage leeloo_lint leeloo_migrate leeloo_makemigrations django_psql odata_psql

leeloo_tests:
	docker-compose run leeloo pytest -s

leeloo_coverage:
	docker-compose run leeloo pytest -s --cov=/app/leeloo --cov-report term-missing --cov-config .coveragerc

leeloo_lint:
	docker-compose run leeloo flake8

leeloo_migrate:
	docker-compose run leeloo python manage.py migrate

leeloo_runserver:
	docker-compose run leeloo python manage.py runserver 0.0.0.0:8000

leeloo_makemigrations:
	docker-compose run leeloo python manage.py makemigrations

leeloo_shellplus:
	docker-compose run leeloo python manage.py shell_plus --ipython

django_psql:
	docker-compose exec	 postgres-django psql -U postgres -d datahub

odata_psql:
	docker-compose exec postgres-odata psql -U postgres -d datahub_odata

import_companieshouse_companies:
	docker-compose run korben-sync-poll korben sync ch

sync_companyhouse:
	docker-compose run korben-sync-poll korben sync es-initial

count-odata:
	docker-compose exec postgres-odata psql -U postgres -d datahub_odata -c "ANALYZE; SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE n_live_tup > 0 ORDER BY n_live_tup DESC;"

count-django:
	docker-compose exec postgres-django psql -U postgres -d datahub_django -c "ANALYZE; SELECT relname, n_live_tup FROM pg_stat_user_tables WHERE n_live_tup > 0 ORDER BY n_live_tup DESC;"
