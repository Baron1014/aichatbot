#!/bin/bash +x

# setup environment variables
ROOT="$PWD"
source "$ROOT/env_setup.sh"

# run the docker container
echo "docker folder: $ROOT"
cd "$ROOT"
cp env_setup.sh Docker/ 

if [ $RUN_FLASK == true ]; then
    cd Docker
    cp ../env_setup.sh .env
    docker-compose build --build-arg UID=$(id -u) --build-arg GID=$(id -g) --build-arg NAME=$(id -un)   
    COMPOSE_PROJECT_NAME=$COURSE docker-compose up -d

    if [ $OSTYPE == "msys" ]; then
        winpty docker exec -it "playlab-$COURSE-flask" bash
    else
        docker exec -it "playlab-$COURSE-flask" bash
    fi
else
    bash run-docker.sh
fi
