#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 DOCKER_HUB_USER"
    exit 1;
fi

DOCKER_HUB_USER=$1
VER=1.0

docker tag local/phippy:${VER} ${DOCKER_HUB_USER}/phippy:${VER}
docker push ${DOCKER_HUB_USER}/phippy:${VER}