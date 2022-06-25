import logging
import os

import requests
from flask import request
from py_zipkin.zipkin import ZipkinAttrs

logger = logging.getLogger(__name__)

ZIPKIN_HOST = os.environ.get("ZIPKIN_HOST", "localhost")
ZIPKIN_PORT = os.environ.get("ZIPKIN_PORT", 9411)
ZIPKIN_URL = f"http://{ZIPKIN_HOST}:{int(ZIPKIN_PORT)}/api/v2/spans"


def default_handler(encoded_span):
    body = encoded_span
    logger.debug("body %s", body)

    return requests.post(
        ZIPKIN_URL,
        data=body,
        headers={"Content-Type": "application/json"},
    )


def get_zipkin_attrs():
    zipkin_attrs = None

    try:
        zipkin_attrs = ZipkinAttrs(
            trace_id=request.headers["X-B3-TraceID"],
            span_id=request.headers["X-B3-SpanID"],
            parent_span_id=request.headers["X-B3-ParentSpanID"],
            flags=request.headers["X-B3-Flags"],
            is_sampled=request.headers["X-B3-Sampled"],
        )
    except Exception:
        pass
    return zipkin_attrs
