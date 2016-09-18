#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module initialisation for the flask application.
"""
import requests

from flask import Flask, render_template, Blueprint, request, current_app
from flask_bootstrap import Bootstrap
from geo_cache_client import GeoCacheClient

def create_app():
    _app = Flask(__name__)
    Bootstrap(_app)
    _app.client = GeoCacheClient({
                        "host" : "foo-d-service",
                        "port" : "5000"
                        })

    return _app

frontend = Blueprint('frontend', __name__)

@frontend.route('/', methods=['POST', 'GET'])
def index():
    status = current_app.client.status()
    results = {}
    error = ""
    if request.method == 'POST':
        postcode = request.form['postcode']
        radius = request.form['radius']
        results = current_app.client.query(postcode, radius)
        if isinstance(results, str):
            error = results
            results = None


    return render_template('home.html', status=status, results=results, error=error)

app = create_app()

if __name__ == '__main__':
    app.register_blueprint(frontend)
    app.run(host="0.0.0.0", port=8080)
