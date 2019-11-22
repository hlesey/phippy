#! /usr/env/bin python3.6

from flask import Flask, render_template
import etcd
import os
import platform

app = Flask(__name__)
etcd_client = etcd.Client(host=os.environ.get('ETCD_HOST', 'etcd'), port=int(os.environ.get('ETCD_PORT', 2379)))
etcd_client.write('mykey', 0)
ver = "1.0"


@app.route('/')
def hello():

    mykey = int(etcd_client.read('mykey').value)
    mykey += 1
    etcd_client.write('mykey', mykey)

    if mykey % 5 == 0:
        return render_template("index.html", poza="/static/images/not_ok.png", mesaj="You can do better!")
    return render_template("index.html", poza="/static/images/ok.jpg", mesaj="You hit me %s times." % mykey)


@app.route('/version')
def version():
    return "version = " + ver


@app.route('/healthz')
def healthz():
    return "healthy"


@app.route('/node')
def node():
    return platform.node()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
