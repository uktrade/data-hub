set -e

cp -r test leeloo
echo "ADD ./test /test" >> leeloo/Dockerfile
cat leeloo/Dockerfile

trap 'docker-compose -f test-browser.yml down --remove-orphans --volumes' EXIT
docker-compose -f test-browser.yml up --build
cd $WORKSPACE/test/browser
./run-outer.sh xvfb-run
