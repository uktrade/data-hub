set -e
docker-compose -f test-browser.yml up --build
cd $WORKSPACE/test/browser
./run-outer.sh xvfb-run
docker-compose -f test-browser.yml down --remove-orphans --volumes
