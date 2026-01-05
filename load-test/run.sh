#!/usr/bin/env bash

UI_URL="http://phippy.clusterx.qedzone.ro"
API_URL="http://phippy-api.clusterx.qedzone.ro"

ITERATIONS=10000

for i in $(seq 1 $ITERATIONS); do

    echo "Generating requests for POST /"
    echo "------------------------"
    hey -n 1000 -m POST $UI_URL

    echo "Generating requests for GET /"
    echo "------------------------"
    hey -n 1000 -m GET $UI_URL

    echo "Generating requests for api GET /trigger_error"
    echo "------------------------"
    hey -n 10 -c 2 -m POST "$API_URL/trigger_error"

    sleep $(jot -r 1 40 130)
done