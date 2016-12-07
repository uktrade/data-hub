#!/bin/sh

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
NO_COLOUR="\033[0m"

colecho () {
    echo -e $1 "[$(date)] $2" $NO_COLOUR
}

container-rm () {
    colecho $BLUE "Drop casperjs container"
    docker ps --format '{{.Names}}' | grep casperjs && docker rm -f casperjs > /dev/null 2>&1 || colecho $YELLOW "Container not running"
}

container-build () {
    container-rm # ☜  deps
    colecho $BLUE "Building casperjs container"
    docker build . -t casperjs > /dev/null 2>&1
}

container-up () {
    container-build # ☜  deps
    colecho $BLUE "Bring casperjs container up (with proper environment, DISPLAY hooked up, etc)"

    colecho $BLUE "Stealing docker-compose .env"
    while read -r line
    do
        if [ $line ]
        then
            export $line
        fi
    done < ../../.env

    colecho $BLUE "Grab local IP to connect X server"
    LOCAL_IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
    colecho $YELLOW "Expecting an X server running at $LOCAL_IP"

    colecho $BLUE "Bring container up (with no command)"
    echo "
    docker run -d \
        -e DISPLAY=$LOCAL_IP:0 \
        -e CDMS_ADFS_URL=$CDMS_ADFS_URL \
        -e CDMS_BASE_URL=$CDMS_BASE_URL \
        -e CDMS_USERNAME=$CDMS_USERNAME \
        -e CDMS_PASSWORD=$CDMS_PASSWORD \
        -e DELETER_PORT=$DELETER_PORT \
        --name casperjs \
        casperjs \
        tail -f /dev/null
    "
}

test-run () {
    colecho $BLUE "Running test suite"
    docker exec casperjs bash run-inner.sh
}

test-result () {
    colecho $BLUE "Determine if the suites passed or failed"
    docker exec casperjs python /src/xunit.py
}

test-results () {
    colecho $BLUE Copying results out
    docker cp casperjs:/results.xml results.xml
}
