#!/bin/sh

set -e
docker-compose -f docker-compose-jenkins.yml build
docker-compose -f docker-compose-jenkins.yml up korben-test
