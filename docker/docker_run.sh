#!/bin/bash

docker network create phippy

docker run -d --net phippy --name etcd qedzone/etcd:3.3.4

docker run -d -p 31380:80 --net phippy --name phippy local/phippy:1.0