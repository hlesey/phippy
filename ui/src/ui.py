import json
import logging
import os

from flask import Flask, Response, jsonify, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from py_zipkin.encoding import Encoding
from py_zipkin.zipkin import zipkin_span

from .__version__ import __version__
from .external_calls import call_api
from .monitoring import register_metrics
from .tracing import default_handler

loggeresp = logging.getLogger(__name__)
app = Flask(__name__)


API_HOST = os.environ.get("API_HOST", "localhost")
API_PORT = os.environ.get("API_PORT", 5000)
API_URL = f"http://{API_HOST}:{int(API_PORT)}"


register_metrics(app, app_version=__version__)


@app.route("/", methods=["GET", "POST"])
def hits():
    """Read or increase the number of hits"""

    with zipkin_span(
        service_name="ui",
        span_name="hits_ui",
        transport_handler=default_handler,
        port=5000,
        sample_rate=100,
        encoding=Encoding.V2_JSON,
    ):

        try:
            resp = call_api(request.method, API_URL)
            resp.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            message = f"Error accessing the API."
            return render_template("index.html", picture="/static/images/not_ok.png", message=message), 500

        if resp.status_code > 400:
            message = "Error accessing the API."
            return render_template("index.html", picture="/static/images/not_ok.png", message=message), resp.status_code

        data = json.loads(resp.text)
        hits = int(data["hits"])

        if request.method == "POST":
            return f"{hits}", resp.status_code

        if hits % 5 == 0:
            message = "You can do better!"
            picture = "/static/images/do_it_betteresp.jpeg"
            return render_template("index.html", picture=picture, message=message), resp.status_code

        message = "You hit me {0} times.".format(hits)

        if hits >= 0 and hits < 10:
            picture = "/static/images/level_0.jpg"
        elif hits >= 10 and hits < 20:
            picture = "/static/images/level_10.jpg"
        elif hits >= 10 and hits < 20:
            picture = "/static/images/level_10.jpg"
        elif hits >= 20 and hits < 50:
            picture = "/static/images/level_20.png"
        elif hits >= 50 and hits < 100:
            picture = "/static/images/level_50.png"
        elif hits >= 100 and hits < 500:
            picture = "/static/images/level_100.png"
        elif hits >= 500 and hits < 1000:
            picture = "/static/images/level_500.jpeg"
        elif hits >= 1000:
            picture = "/static/images/level_1000.png"

        return render_template("index.html", picture=picture, message=message), resp.status_code


@app.route("/version", methods=["GET"])
def version():
    """Get application running version for both ui and api"""
    with zipkin_span(
        service_name="ui",
        span_name="version_ui",
        transport_handler=default_handler,
        port=5000,
        sample_rate=100,
        encoding=Encoding.V2_JSON,
    ):

        try:
            resp = call_api(request.method, f"{API_URL}/version")
            resp.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            message = f"Error accessing the API."
            return render_template("index.html", picture="/static/images/not_ok.png", message=message), 500

        if resp.status_code != 200:
            message = "Error accessing the API."
            return render_template("index.html", picture="/static/images/not_ok.png", message=message), resp.status_code

        data = json.loads(resp.text)
        return jsonify(api_version=data["version"], ui_version=__version__), 200


@app.route("/readyz", methods=["GET"])
def readyz():
    """Check if the web server is healty"""

    with zipkin_span(
        service_name="ui",
        span_name="readyz_ui",
        transport_handler=default_handler,
        port=5000,
        sample_rate=100,
        encoding=Encoding.V2_JSON,
    ):

        is_ready = False

        try:
            resp = call_api(request.method, f"{API_URL}/ready")
            resp.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            return jsonify(ready=is_ready), 500

        if resp.status_code == 200:
            is_ready = True

        return jsonify(ready=is_ready), resp.status_code


@app.route("/livez", methods=["GET"])
def livez():
    """Check if the web server is running"""

    return jsonify(alive=True), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    """Get metrics"""

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST), 200


if __name__ == "__main__":
    app.run()
