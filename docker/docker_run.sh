#!/bin/bash

docker run -d -p 4001:4001 --name etcd trainersontheweb/etcd:3.3.4
docker run -d -p 31380:80 --link etcd:etcd --name phippy local/phippy