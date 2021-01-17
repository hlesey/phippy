#!/usr/bin/env bash

API_URL="http://phippy-api.local:30080"

# Generating POST requests
echo "Generating POST requests"
echo "------------------------"
sleep 1;

for i in {0..500}; do
    echo "running: curl -s -XPOST $API_URL"
    curl -s -XPOST $API_URL
done

# Generating GET requests
echo "Generating GET requests"
echo "------------------------"
sleep 1;

for i in {0..1000}; do
    echo "running: curl -s -XGET $API_URL"
    curl -s -XGET $API_URL
done 

# Artificially generate errors in the app
echo "Artificially generate errors"
echo "------------------------"
sleep 1;

for i in {0..20}; do
    echo "running: curl -s -XGET "$API_URL/trigger_error""
    curl -s -XGET "$API_URL/trigger_error"
done
