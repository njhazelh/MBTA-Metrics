#!/usr/bin/env python

"""
This module contains a REST API, which makes data available
to the frontend dashboard contained in ../webapi
"""

from datetime import time, date

from flask import Flask, jsonify
from mbtaalerts.database.database import DB_SESSION, init_db
from mbtaalerts.database.models import AlertEvent
from mbtaalerts.logging import get_log

LOG = get_log('api')
APP = Flask(__name__)

@APP.teardown_appcontext
def shutdown_session(exception=None):
    DB_SESSION.remove()

@APP.route('/data/alert_events')
def get_alert_events():
    """
    This is a filler endpoint that can be used to test
    deployment
    """
    alert_events = AlertEvent.query.all()
    return jsonify([ae.serialize for ae in alert_events])

if __name__ == "__main__":
    init_db()
    APP.run(host="0.0.0.0")
