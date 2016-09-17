#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This file will contain the webui endpoints for the web Application
"""

from flask import Blueprint
from flask import jsonify

api = Blueprint('v1', __name__)
""" Create a versioned API. """

@api.route('/status')
def index():
    return jsonify(state='ok'), 200
