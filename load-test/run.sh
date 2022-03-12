#!/usr/bin/env bash

URL="http://phippy.clusterx.qedzone.ro:30080"

# Generating POST requests
echo "Generating POST requests"
echo "------------------------"

hey -n 1000 -m POST $URL


# Generating GET requests
echo "Generating GET requests"
echo "------------------------"

hey -n 1000 -m POST $URL


# Artificially generate errors in the app
echo "Artificially generate errors"
echo "------------------------"

hey -n 1000 -m GET "$URL/trigger_error"
