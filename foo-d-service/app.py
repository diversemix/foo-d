#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module initialisation for the flask application.
"""
import json
import redis
import logging

from flask import Flask, Blueprint, jsonify, current_app, request

from geo_cache import GeoCache
from logger import initLogger

CONFIG = '/data/config.json'
initLogger()

# Bit icky - could do with an enum
HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

def create_app():
    """ Function that initialises the application from the config. """
    _app = Flask(__name__)
    #_app.config.from_json(CONFIG)

    config = None
    with open(CONFIG) as data_file:
        config = json.load(data_file)
        _app.geocache = GeoCache(config)

    # These values should really be in the config file.
    _app.pool = redis.ConnectionPool(host='redis', port=6379, db=0)
    _app.redis_client = redis.Redis(connection_pool=_app.pool)
    _app.geocache.populate(_app.redis_client)

    return _app

# ----- Section for the API endpoints

v1api = Blueprint('v1', 'v1api') # Create a versioned API

@v1api.route('/status')
def app_status():
    gc = current_app.geocache
    return jsonify(state='ok',
                   num_postcodes=gc.num_postcodes,
                   num_pubs=gc.num_pubs,
                   ), HTTP_200_OK

@v1api.route('/query', methods=['POST'])
def query():
    if not request.data:
        logging.error("No data in request")
        return jsonify({}), HTTP_400_BAD_REQUEST

    data = request.data.decode('ascii')

    logging.info("Params %s : %s", type(data), data)

    params = json.loads(data)
    if 'postcode' not in params:
        error = "No posstcode in request"
        logging.error(error)
        return jsonify({ "error" : error}), HTTP_400_BAD_REQUEST

    if 'radius' not in params:
        logging.error("No radius in request")
        return jsonify({ "error" : error}), HTTP_400_BAD_REQUEST

    postcode = params['postcode']
    radius = params['radius']
    try:
        results = current_app.geocache.get_pubs_here(current_app.redis_client,
                postcode,
                radius)
        code = HTTP_200_OK
    except redis.exceptions.ResponseError as err:
        return jsonify({ "error" : str(err)}), HTTP_400_BAD_REQUEST

    return jsonify(results=results), code

# ----- Main function that runs the application

if __name__ == '__main__':
    app = create_app() # Create the application
    app.register_blueprint(v1api, url_prefix='/v1')
    app.run(host="0.0.0.0", port=5000)
