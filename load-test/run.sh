#!/usr/bin/env bash

UI_URL="http://phippy.clusterx.qedzone.ro:30080"
API_URL="http://phippy-api.clusterx.qedzone.ro:30080"


# Generating POST requests
echo "Generating POST requests"
echo "------------------------"
hey -n 1000 -m POST $UI_URL

# Generating GET requests
echo "Generating GET requests"
echo "------------------------"
hey -n 1000 -m POST $UI_URL

# Generating GET requests
echo "Generating GET requests for version endpoint"
echo "------------------------"
hey -n 1000 -m POST $UI_URL/version

# Generating GET requests
echo "Generating GET requests just for api readyz endpoint"
echo "------------------------"
hey -n 1000 -m POST $API_URL/readyz

# Generating GET requests
echo "Generating GET requests just for api livez endpoint"
echo "------------------------"
hey -n 1000 -m POST $API_URL/livez

# Artificially generate errors in the app
echo "Artificially generate errors"
echo "------------------------"
hey -n 1000 -m GET "$API_URL/trigger_error"
