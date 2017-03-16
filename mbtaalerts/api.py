#!/usr/bin/env python

"""
This module contains a REST API, which makes data available
to the frontend dashboard contained in ../webapi
"""

from flask import Flask, jsonify
from datetime import time, date

APP = Flask(__name__)

def ae(_id, date, route, stop, direction,
    scheduled_departure, actual_departure, delay,
    alert_issued, alert_delay, alert_text, predicted_delay):
    return {
        'id': _id,
        'date': date,
        'route': route,
        'stop': stop,
        'direction': direction,
        'scheduled_departure': scheduled_departure,
        'actual_departure': actual_departure,
        'delay': delay,
        'alert_issued': alert_issued,
        'alert_delay': alert_delay,
        'alert_text': alert_text,
        'predicted_delay': predicted_delay
    }

@APP.route('/data/alert_events')
def alert_events():
    """
    This is a filler endpoint that can be used to test
    deployment
    """
    return jsonify([
        ae(
            1,
            date(2017, 10, 12).isoformat(),
            "Worcester",
            "Framingham",
            "Inbound",
            time(6, 10).isoformat(),
            time(6, 25).isoformat(),
            15,
            True,
            time(6, 15).isoformat(),
            "Worcester Train 505 ...",
            "10-15"),
        ae(
            1,
            date(2017, 10, 12).isoformat(),
            "Worcester",
            "Framingham",
            "Inbound",
            time(6, 10).isoformat(),
            time(6, 25).isoformat(),
            15,
            True,
            time(6, 15).isoformat(),
            "Worcester Train 505 ...",
            "10-15"),
        ae(
            1,
            date(2017, 10, 12).isoformat(),
            "Worcester",
            "Framingham",
            "Inbound",
            time(6, 10).isoformat(),
            time(6, 25).isoformat(),
            15,
            True,
            time(6, 15).isoformat(),
            "Worcester Train 505 ...",
            "10-15")
    ])

if __name__ == "__main__":
    APP.run(host="0.0.0.0")
