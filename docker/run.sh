#!/usr/bin/env bash

docker run -d -p 4001:4001 --name etcd elcolio/etcd:latest
docker run -d -p 31380:80 --link etcd:etcd --name web local/phippy
