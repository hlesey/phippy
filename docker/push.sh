#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 DOCKER_HUB_USER"
    exit 1;
fi

DOCKER_HUB_USER=$1

docker tag local/phippy DOCKER_HUB_USER/phippy
docker push trainersontheweb/phippy