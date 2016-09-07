#!/bin/bash

export COMPOSE_FILE=docker-compose-jenkins.yml

docker-compose build
docker-compose run --service-ports korben-test
docker-compose down -v
