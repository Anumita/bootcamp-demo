#!/usr/bin/env python

from random import randrange
from flask import Flask
from datadog import initialize
from datadog import api
from datadog import statsd
import os
import datetime

options = {
    'api_key':'b18988cfea6d6f52dc82532ccaedd1c6',
    'app_key':'4d54ff31bfbb572d9988f037664b5e977b75221b'
}

initialize(**options)

app = Flask('doggopy-demo')
appVersion = os.getenv('APP_VERSION', "1")
tags = ['appVersion:{}'.format(appVersion)]

@app.route('/')
def hello():
    if randrange(1, 100) > 40: # 90% of the requests are "good"
        api.Metric.send(metric="app.custom_status", points=[datetime.datetime.utcnow().timestamp(), 1], host=os.getenv('COMPUTERNAME'), tags=tags, type="count")
        return "Internal Server Error\n", 500
    else:
        api.Metric.send(metric="app.custom_status", points=[datetime.datetime.utcnow().timestamp(), 0], host=os.getenv('COMPUTERNAME'), tags=tags, type="count")
        return "Hello World!\n", 200

app.run(host = '0.0.0.0', port = 8080)
