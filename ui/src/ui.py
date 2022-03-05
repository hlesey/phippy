import json
import os

import requests
from flask import Flask, jsonify, render_template, request

from .__version__ import __version__

app = Flask(__name__)
api_url = f"http://{os.environ.get('API_HOST', 'localhost')}:{int(os.environ.get('API_PORT', 5000))}"


@app.route("/", methods=["GET", "POST"])
def hits():
    """Read or increase the number of hits"""

    if request.method == "POST":
        r = requests.post(f"{api_url}")

        if r.status_code != 201:
            message = "Error accessing the API."
            return render_template("index.html", picture="/static/images/not_ok.png", message=message), r.status_code

        data = json.loads(r.text)
        return f"{data['hits']}"
    else:
        r = requests.get(f"{api_url}")

        if r.status_code != 200:
            message = "Error accessing the API."
            return render_template("index.html", picture="/static/images/not_ok.png", message=message), r.status_code

        data = json.loads(r.text)
        hits = int(data["hits"])

        if hits % 5 == 0:
            message = "You can do better!"
            picture = "/static/images/do_it_better.jpeg"
            return render_template("index.html", picture=picture, message=message), r.status_code

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

        return render_template("index.html", picture=picture, message=message), r.status_code


@app.route("/version", methods=["GET"])
def version():
    """Get application running version for both ui and api"""

    r = requests.get(f"{api_url}/version")

    if r.status_code != 200:
        message = "Error accessing the API."
        return render_template("index.html", picture="/static/images/not_ok.png", message=message), r.status_code

    data = json.loads(r.text)
    return jsonify(api_version=data["version"], ui_version=__version__), 200
