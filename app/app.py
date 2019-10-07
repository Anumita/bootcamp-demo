#!/usr/bin/env python

from random import randrange
from flask import Flask
from prometheus_client import start_http_server, Counter
import os
import sys

app = Flask('bootcamp-demo')
c = Counter('requests', 'Number of requests served, by custom_status', ['custom_status'])

@app.route('/')
def hello():
    if randrange(1, 100) > 40: # 90% of the requests are "good"
        c.labels(custom_status = 'bad').inc()
        print("bad request", file=sys.stderr)
        return "Internal Server Error\n", 500
    else:
        c.labels(custom_status = 'good').inc()
        print "good request"
        return "Hello World!\n", 200

start_http_server(8000)
app.run(host = '0.0.0.0', port = 8080)
