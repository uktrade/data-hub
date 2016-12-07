#!/bin/bash

source commands.sh # ☜  load all the functions

trap "container-rm" EXIT

container-up

test-run
test-result
EXIT_CODE=$?
test-results

exit $EXIT_CODE
