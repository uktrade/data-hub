set -e

ls -la test

trap 'docker-compose -f test-browser.yml down --remove-orphans --volumes' EXIT
docker-compose -f test-browser.yml up --build
cd $WORKSPACE/test/browser
./run-outer.sh xvfb-run
