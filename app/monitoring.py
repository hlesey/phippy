import logging
from flask import request
from prometheus_client import Counter, Histogram, Info
from timeit import default_timer

logger = logging.getLogger(__name__)

APP_NAME = "phippy"
APP_INFO = Info("app_version", "Aplication Version")

ERROROS_COUNT = Counter(
    "errors_total",
    "Number of errors",
    ["app", "verb", "endpont", "status"]
)
REQUESTS_COUNT = Counter(
    "request_total",
    "Request duration in seconds",
    ["app", "verb", "endpoint", "status"]
)
REQUEST_DURATION_HISTOGRAM = Histogram(
    "request_duration_seconds",
    "Request duration in seconds",
    ["app", "verb", "endpoint", "status"]
)



def before_request():
    """
    Get start time of a request
    """
    request._prometheus_metrics_request_start_time = default_timer()


def after_request(response):
    """
    Register Prometheus metrics after each request
    """
    if hasattr(request, "_prometheus_metrics_request_start_time"):
        request_latency = max(
            default_timer() - request._prometheus_metrics_request_start_time, 0
        )
        REQUEST_DURATION_HISTOGRAM.labels(
            APP_NAME,
            request.method,
            request.endpoint,
            response.status_code,
        ).observe(request_latency)
    REQUESTS_COUNT.labels(
        APP_NAME,
        request.method,
        request.endpoint,
        response.status_code,
    ).inc()
    return response


def register_metrics(app, app_version=None, app_config=None):
    """
    Register metrics middlewares
    Flask application can register more than one before_request/after_request.
    Beware! Before/after request callback stored internally in a dictionary.
    Before CPython 3.6 dictionaries didn't guarantee keys order, so callbacks
    could be executed in arbitrary order.
    """

    app.before_request(before_request)
    app.after_request(after_request)
    # APP_INFO.info({"version": app_version, "config": app_config})

