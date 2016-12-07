#!/bin/bash

source commands.sh # ☜  load all the functions

trap "container-rm" EXIT

container-up

test-run $1 # ☜  the $1 is "xvfb-run" for jenkins (prepended to run command)
test-result
EXIT_CODE=$?
test-results

exit $EXIT_CODE
