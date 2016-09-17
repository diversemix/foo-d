#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module initialisation for the flask application.
"""

from flask import Flask
from flask_bootstrap import Bootstrap

from .frontend import frontend

def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app
