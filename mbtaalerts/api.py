#!/usr/bin/env python

"""
This module contains a REST API, which makes data available
to the frontend dashboard contained in ../webapi
"""

from datetime import time, date

from flask import Flask, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args

from mbtaalerts.database.database import DB_SESSION, init_db
from mbtaalerts.database.models import AlertEvent
from mbtaalerts.logging import get_log


LOG = get_log('api')
APP = Flask(__name__)
APP.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@APP.teardown_appcontext
def shutdown_session(exception=None):
    """
    This ties into sqlalchemy to make sure that each
    API session has an independent DB session.
    """
    DB_SESSION.remove()


@APP.route('/data/alert_events')
@use_args({
    'startDate': fields.Date(required=True),
    'endDate': fields.Date(required=True),
    'startTime': fields.Time(required=True),
    'endTime': fields.Time(required=True),
})
def get_alert_events(args):
    """
    This end point will respond with a list of alert events within the
    given range.

    Date and Time values are independent. For example,
    a query for all the events in the past year within the hours of
    7am and 7pm will not return an event at 8pm yesterday, but it
    will return an event at 6pm yesterday.

    :args: The dict from webargs containing the args above
        - startDate: The first day of events to look at (inclusive).
        - endDate: The last day of events to look at (inclusive).
        - startTime: Earliest time to look at (inclusive).
        - endTime: The latest time to look at (inclusive).
    :return: A list of alert_events within the given date/time ranges.
    """
    alert_events = AlertEvent.query \
        .filter(AlertEvent.date >= args['startDate']) \
        .filter(AlertEvent.date <= args['endDate']) \
        .filter(AlertEvent.time >= args['startTime']) \
        .filter(AlertEvent.time <= args['endTime']) \
        .all()
    return jsonify(data=[ae.serialize for ae in alert_events])


if __name__ == "__main__":
    init_db()
    APP.run(host="0.0.0.0")
