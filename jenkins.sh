set -e

trap 'docker-compose -f test-browser.yml down --remove-orphans --volumes' EXIT
docker-compose -f test-browser.yml down --remove-orphans --volumes
docker-compose -f test-browser.yml up -d --build
printf 'Waiting for front end to become available '
until $(curl --output /dev/null --silent --head --fail http://localhost:3000); do
    printf '.'
    sleep 1
done
echo !
cd $WORKSPACE/test/browser
./run-outer.sh xvfb-run
cd $WORKSPACE
