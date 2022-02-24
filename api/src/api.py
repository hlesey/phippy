import logging
import os

from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from redis import Redis

from .__version__ import __version__
from .monitoring import record_error_metric, register_metrics

logger = logging.getLogger(__name__)


app = Flask(__name__)
redis = Redis(host=os.environ.get("DB_HOST", "localhost"), port=int(os.environ.get("DB_PORT", 6379)))
register_metrics(app, app_version=__version__)


@app.route("/", methods=["GET", "POST"])
def hits():
    """Read or increase the number of hits"""

    if request.method == "POST":
        redis.incr("hits")
        hits = int(redis.get("hits"))

        return jsonify(hits=hits), 201
    else:
        if not redis.exists("hits"):
            redis.set("hits", 0)
        hits = int(redis.get("hits"))

        return jsonify(hits=hits), 200


@app.route("/version", methods=["GET"])
def version():
    """Get application running version"""

    return jsonify(version=__version__), 200


@app.route("/readyz", methods=["GET"])
def readyz():
    """Check if the web server is healty"""

    is_ready = False

    if redis.ping():
        is_ready = True

    return jsonify(ready=is_ready), 200


@app.route("/livez", methods=["GET"])
def livez():
    """Check if the web server is running"""

    return jsonify(alive=True), 200


@app.route("/metrics", methods=["GET"])
def metrics():
    """Get metrics"""

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST), 200


@app.route("/trigger_error", methods=["POST"])
def trigger_error():
    """Trigger an error"""
    raise Exception("error triggered by operator")


@app.errorhandler(500)
def handle_500(error):

    record_error_metric(status=500)
    return jsonify(error=str(error)), 500


if __name__ == "__main__":
    app.run()
