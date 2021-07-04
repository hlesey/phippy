#!/usr/bin/env bash

URL="http://phippy-api.clusterx.qedzone.ro:30080"

# Generating POST requests
echo "Generating POST requests"
echo "------------------------"
sleep 1;

for i in {0..500}; do
    echo "running: curl -s -XPOST $URL"
    curl -s -XPOST $URL
done

# Generating GET requests
echo "Generating GET requests"
echo "------------------------"
sleep 1;

for i in {0..1000}; do
    echo "running: curl -s -XGET $URL"
    curl -s -XGET $URL
done 

# Artificially generate errors in the app
echo "Artificially generate errors"
echo "------------------------"
sleep 1;

for i in {0..20}; do
    echo "running: curl -s -XGET "$URL/trigger_error""
    curl -s -XGET "$URL/trigger_error"
done
