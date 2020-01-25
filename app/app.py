import os
import platform
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, REGISTRY
from flask import Flask, Response, render_template
from redis import Redis
from app.__version__ import __version__
from app.monitoring import register_metrics, record_error_metric


app = Flask(__name__)
redis = Redis(host=os.environ.get('REDIS_HOST', 'redis'),  port=int(os.environ.get('REDIS_PORT', 6379)))
register_metrics(app, app_version=__version__)


@app.route('/', methods=['POST'])
def hits_post():
    redis.incr('hits')
    hits = int(redis.get('hits'))

    if hits % 5 == 0:
        return render_template("index.html", picture="/static/images/not_ok.png", message="You can do better!")
    return render_template("index.html", picture="/static/images/ok.jpg", message="You hit me %s times." % hits)


@app.route('/', methods=['GET'])
def hits_get():
    if not redis.exists('hits'):
        redis.set('hits', 0)
    hits = int(redis.get('hits'))
    return render_template("index.html", picture="/static/images/ok.jpg", message="You hit me %s times." % hits)


@app.route('/version')
def version():
    return "version=" + __version__


@app.route('/healthz')
def healthz():
    if redis.ping():
        return "healthy"
    else:
        return "unheathy"


@app.route('/node')
def node():
    return platform.node()
    

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/trigger_error')
def trigger_error():
    raise Exception("error triggered by operator")


@app.errorhandler(500)
def handle_500(error):
    record_error_metric(status=500)
    return str(error), 500