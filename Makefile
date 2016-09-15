.PHONY: leeloo_tests leeloo_coverage

leeloo_tests:
	docker-compose run leeloo pytest

leeloo_coverage:
	docker-compose run leeloo pytest --cov=api --cov-report term

leeloo_lint:
	docker-compose run leeloo flake8

leeloo_migrate:
	docker-compose run leeloo python manage.py migrate

leeloo_makemigrations:
	docker-compose run leeloo python manage.py makemigrations

django_psql:
	docker-compose exec postgres-django psql -U postgres -d datahub

odata_psql:
	docker-compose exec postgres-odata psql -U postgres -d datahub_odata
