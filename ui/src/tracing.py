import logging
import os

import requests

ZIPKIN_HOST = os.environ.get("ZIPKIN_HOST", "localhost")
ZIPKIN_PORT = os.environ.get("ZIPKIN_PORT", 9411)
ZIPKIN_URL = f"http://{ZIPKIN_HOST}:{int(ZIPKIN_PORT)}/api/v2/spans"

logger = logging.getLogger(__name__)


def default_handler(encoded_span):
    body = encoded_span
    logger.debug("body %s", body)

    return requests.post(
        ZIPKIN_URL,
        data=body,
        headers={"Content-Type": "application/json"},
    )
