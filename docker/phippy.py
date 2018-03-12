#! /usr/env/bin python3.6

from flask import Flask, request, render_template
import etcd
import os

app = Flask(__name__)
etcd_client = etcd.Client(host=os.environ.get('ETCD_HOST', 'etcd'), port=4001)
etcd_client.write('mykey', 0)


@app.route('/')
def hello():

    mykey = int(etcd_client.read('mykey').value)
    mykey += 1
    etcd_client.write('mykey', mykey)

    if mykey % 5 == 0:
        #return 'You can do better!'
        return render_template("index.html", poza="/static/images/not_ok.png", mesaj="You can do better!")

    #return 'You hit me %s times.' % mykey
    return render_template("index.html", poza="/static/images/ok.jpg", mesaj="You hit me %s times." % mykey)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)