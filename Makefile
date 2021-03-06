.PHONY: test-leeloo

test-leeloo:
	docker-compose -f test-leeloo.yml build && docker-compose -f test-leeloo.yml run leeloo pytest -s

drop-es-test-index:
	curl -XDELETE 'localhost:9200/test?pretty'

test-leeloo-coverage:
	docker-compose run leeloo pytest -s --cov=/app/leeloo --cov-report term-missing --cov-config .coveragerc

leeloo-migrate:
	docker-compose run leeloo python manage.py migrate

leeloo-makemigrations:
	docker-compose run leeloo python manage.py makemigrations

leeloo-shellplus:
	docker-compose run leeloo python manage.py shell_plus --ipython

leeloo-load-metadata:
	docker-compose run leeloo python manage.py loaddata metadata.yaml

leeloo-load-testdata:
	docker-compose run leeloo python manage.py loaddata test_data.yaml

psql-django:
	docker-compose exec postgres-django psql -U postgres -d datahub

psql-odata:
	docker-compose exec postgres-odata psql -U postgres -d datahub_odata

korben-sync-ch:
	docker-compose exec korben korben sync ch

korben-sync-es:
	docker-compose exec korben korben sync es

korben-sync-django:
	docker-compose exec korben korben sync django

PSQL_CSV_OUT = psql -P pager=off -t -A -F"," -U postgres

count-odata:
	docker-compose exec postgres-odata ${PSQL_CSV_OUT} -d datahub_odata -c " \
	ANALYZE; \
	SELECT relname, n_live_tup \
		FROM pg_stat_user_tables \
		WHERE n_live_tup > 0 \
		ORDER BY n_live_tup DESC; \
	"

count-django:
	docker-compose exec postgres-django ${PSQL_CSV_OUT} -d datahub -c " \
	ANALYZE; \
	SELECT relname, n_live_tup \
		FROM pg_stat_user_tables \
		WHERE n_live_tup > 0 \
		ORDER BY n_live_tup DESC; \
	"

test-odata-psql:
	cd odata-psql && docker-compose up --build test

test-korben-tier0:
	docker-compose -f test-korben-tier0.yml build && docker-compose -f test-korben-tier0.yml run --service-ports test

test-korben-tier2:
	docker-compose -f test-korben-tier2.yml build && docker-compose -f test-korben-tier2.yml run --service-ports test

test-korben-unit:
	docker-compose -f test-korben-unit.yml build && docker-compose -f test-korben-unit.yml run --service-ports test

docker-cleanup:
	docker rm -f `docker ps -qa` || echo
