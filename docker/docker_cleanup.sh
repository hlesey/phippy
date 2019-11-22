#!/bin/bash

docker stop etcd phippy
docker rm etcd phippy
docker network rm phippy