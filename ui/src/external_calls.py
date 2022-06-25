import requests
from py_zipkin.request_helpers import create_http_headers
from py_zipkin.zipkin import zipkin_client_span


@zipkin_client_span(service_name="ui", span_name="call_api")
def call_api(method: str, url: str) -> requests.Response:
    headers = create_http_headers()

    if method == "POST":
        resp = requests.post(f"{url}", headers=headers)
    else:
        resp = requests.get(f"{url}", headers=headers)

    return resp
