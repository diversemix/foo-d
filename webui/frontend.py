#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This file will contain the webui endpoints for the web Application
"""

from flask import (Blueprint, render_template, flash, redirect, url_for)

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('home.html')
