import os
import platform
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from flask import Flask, Response
from redis import Redis
from api.__version__ import __version__
from api.monitoring import register_metrics, record_error_metric
from flask import jsonify


app = Flask(__name__)
redis = Redis(host=os.environ.get('DB_HOST', 'phippy-db'), port=int(os.environ.get('DB_PORT', 6379)))
register_metrics(app, app_version=__version__)


@app.route('/', methods=['POST'])
def hits_post():
    redis.incr('hits')
    hits = int(redis.get('hits'))

    return jsonify(hits=hits), 201


@app.route('/', methods=['GET'])
def hits_get():

    if not redis.exists('hits'):
        redis.set('hits', 0)
    hits = int(redis.get('hits'))

    return jsonify(hits=hits), 200


@app.route('/version')
def version():
    return jsonify(version=__version__), 200


@app.route('/healthz')
def healthz():
    is_healthy = False

    if redis.ping():
        is_healthy = True

    return jsonify(healthy=is_healthy), 200


@app.route('/node')
def node():
    return jsonify(node=platform.node()), 200


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST), 200


@app.route('/trigger_error')
def trigger_error():
    raise Exception("error triggered by operator")


@app.errorhandler(500)
def handle_500(error):
    record_error_metric(status=500)
    return jsonify(error=str(error)), 500
