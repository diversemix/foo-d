#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module initialisation for the flask application.
"""
import json

from flask import Flask

from api import api
from geo_cache import GeoCache

CONFIG = '/data/config.json'

def create_app():
    _app = Flask(__name__)
    #_app.config.from_json(CONFIG)

    config = None
    with open(CONFIG) as data_file:
        config = json.load(data_file)
        _app.geocache = GeoCache(config)

    return _app

if __name__ == '__main__':
    app = create_app()
    app.run()
