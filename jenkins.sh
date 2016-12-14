set -e

trap 'cd $WORKSPACE && docker-compose -f test-browser.yml down --remove-orphans --volumes' EXIT
echo "Bringing outer containers up ..."
docker-compose -f test-browser.yml down --remove-orphans --volumes > /dev/null 2>&1
docker-compose -f test-browser.yml up -d --build > /dev/null 2>&1
printf 'Waiting for front end to become available '
until $(curl --output /dev/null --silent --head --fail http://$(awk 'BEGIN{split(ENVIRON["DOCKER_HOST"],X,"//"); split(X[2],Y,":"); print Y[1]}'):3000); do
    printf '.'
    sleep 1
done
echo !
cd $WORKSPACE/test/browser
./run-outer.sh xvfb-run
cd $WORKSPACE
