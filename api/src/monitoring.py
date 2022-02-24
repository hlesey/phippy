import logging
from timeit import default_timer

from flask import request
from prometheus_client import Counter, Histogram, Info

logger = logging.getLogger(__name__)

APP_NAME = "phippy_api"
APP_INFO = Info("api_version", "API Version")
ERRORS_COUNT = Counter("errors_total", "Number of errors", ["app", "verb", "endpoint", "status"])
REQUESTS_COUNT = Counter("request_total", "Request duration in seconds", ["app", "verb", "endpoint", "status"])
REQUEST_DURATION_HISTOGRAM = Histogram(
    "request_duration_seconds", "Request duration in seconds", ["app", "verb", "endpoint", "status"]
)


def register_metrics(app, app_version=None, app_config=None):
    """Register metrics middlewares"""

    app.before_request(before_request)
    app.after_request(after_request)


def record_error_metric(status=None):
    """Record errors"""

    ERRORS_COUNT.labels(
        APP_NAME,
        request.method,
        request.endpoint,
        status,
    ).inc()


def before_request():
    """Set start time of a request"""

    request._prometheus_metrics_request_start_time = default_timer()


def after_request(response):
    """Record requests count and latency after each request"""

    # do not record metrics endpoint
    if request.endpoint == "metrics":
        return response

    if hasattr(request, "_prometheus_metrics_request_start_time"):
        request_latency = max(default_timer() - request._prometheus_metrics_request_start_time, 0)
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
