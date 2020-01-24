from flask import Flask, render_template
from redis import Redis
import os
import platform
from app.__version__ import __version__


app = Flask(__name__)
redis = Redis(host=os.environ.get('REDIS_HOST', 'redis'),  port=int(os.environ.get('REDIS_PORT', 6379)))
redis.set('hits', 0)


@app.route('/', methods=['POST'])
def hits_post():
    redis.incr('hits')
    hits = int(redis.get('hits'))

    if hits % 5 == 0:
        return render_template("index.html", picture="/static/images/not_ok.png", message="You can do better!")
    return render_template("index.html", picture="/static/images/ok.jpg", message="You hit me %s times." % hits)


@app.route('/', methods=['GET'])
def hits_get():
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
