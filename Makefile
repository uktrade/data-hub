.PHONY: leeloo_tests leeloo_coverage

leeloo_tests:
    docker-compose run leeloo pytest


leeloo_coverage:
    docker-compose run leeloo pytest --cov=api --cov-report term

