#!/usr/bin/env python

"""
evaluator.py is a job that should be run once every 24 hours via cron.

It takes the previous day of alert information and aggregates it into
alert_metrics, which it stores in the database.

It can also be targeted to a specific date if it needs to be run on historic
data.  See command-line help information.
"""

import time as _time
from datetime import datetime, date, time, timedelta, timezone
import calendar
from collections import defaultdict, namedtuple
import argparse

import requests
from sqlalchemy.exc import SQLAlchemyError
import psycopg2

from mbtaalerts.logging import get_log
from mbtaalerts.config import config as cfg
# TODO Remove init_db. Since the db should already be setup it's not needed outside
# testing on an in-memory database.
from mbtaalerts.database.database import get_db_session, init_db
from mbtaalerts.database.models import (AlertAffectedService,
                                        Alert,
                                        AlertEvent,
                                        Direction,
                                        DelayAccuracy)


# "Four Corners/Geneva Ave" API Call  returns empty?
# TODO Perhaps it's worth pulling these from the API each time.
FAIRMOUNT_LINE = [
    "Readville", "Fairmount", "Morton Street", "Talbot Avenue",
    "Four Corners / Geneva", "Uphams Corner", "Newmarket", "South Station"]
FITCHBURG_LINE = [
    "wachusett", "Fitchburg", "North Leominster", "Shirley", "Ayer",
    "Littleton / Rte 495", "South Acton", "West Concord", "Concord", "Lincoln",
    "Silver Hill", "Hastings", "Kendal Green", "Brandeis/ Roberts", "Waltham",
    "Waverley", "Belmont", "Porter Square", "North Station"]
FRAMINGHAM_WORCESTER_LINE = [
    "Worcester", "Grafton", "Westborough", "Southborough", "Ashland",
    "Framingham", "West Natick", "Natick Center", "Wellesley Square",
    "Wellesley Hills", "Wellesley Farms", "Auburndale", "West Newton",
    "Newtonville", "Yawkey", "Back Bay", "South Station"]
FRANKLIN_LINE = [
    "Forge Park / 495", "Franklin", "Norfolk", "Walpole", "Plimptonville",
    "Windsor Gardens", "Norwood Central", "Norwood Depot", "Islington",
    "Dedham Corp Center", "Endicott", "Readville", "Ruggles", "Back Bay",
    "South Station"]
GREENBUSH_LINE = [
    "Greenbush", "North Scituate", "Cohasset", "Nantasket Junction",
    "West Hingham", "East Weymouth", "Weymouth Landing/ East Braintree",
    "Quincy Center", "JFK/UMass", "South Station"]
HAVERHILL_LINE = [
    "Haverhill", "Bradford", "Lawrence", "Andover", "Ballardvale",
    "North Wilmington", "Reading", "Wakefield", "Greenwood",
    "Melrose Highlands", "Melrose Cedar Park", "Wyoming Hill", "Malden Center",
    "North Station"]
KINGSTON_PLYMOUTH_LINE = [
    "Kingston", "Plymouth", "Halifax", "Hanson", "Whitman", "Abington",
    "South Weymouth", "Braintree", "JFK/UMass", "South Station"]
LOWELL_LINE = [
    "Lowell", "North Billerica", "Wilmington", "Anderson/ Woburn", "Mishawum",
    "Winchester Center", "Wedgemere", "West Medford", "North Station"]
MIDDLEBOROUGH_LAKEVILLE_LINE = [
    "Middleborough/ Lakeville", "Bridgewater", "Campello", "Brockton",
    "Montello", "Holbrook/ Randolph", "Braintree", "Quincy Center",
    "JFK/UMASS", "South Station"]
NEEDHAM_LINE = [
    "Needham Heights", "Needham Center", "Needham Junction", "Hersey",
    "West Roxbury", "Highland", "Bellevue", "Roslindale Village",
    "Forest Hills", "Ruggles", "Back Bay", "South Station"]
NEWBURY_ROCKPORT_LINE = [
    "Rockport", "Gloucester", "West Gloucester", "Manchester", "Beverly Farms",
    "Prides Crossing", "Montserrat", "Newburyport", "Rowley", "Ipswich",
    "Hamilton/ Wenham", "North Beverly", "Beverly", "Salem", "Swampscott",
    "Lynn", "River Works / GE Employees Only", "Chelsea", "North Station"]
PROVIDENCE_STOUGHTON_LINE = [
    "Wickford Junction", "TF Green Airport", "Providence", "South Attleboro",
    "Attleboro", "Mansfield", "Sharon", "Stoughton", "Canton Center",
    "Canton Junction", "Route 128", "Hyde Park", "Ruggles", "Back Bay",
    "South Station"]
COMMUTER_RAIL = FAIRMOUNT_LINE + FITCHBURG_LINE + FRAMINGHAM_WORCESTER_LINE + \
    FRANKLIN_LINE + GREENBUSH_LINE + HAVERHILL_LINE + KINGSTON_PLYMOUTH_LINE + \
    LOWELL_LINE + MIDDLEBOROUGH_LAKEVILLE_LINE + NEEDHAM_LINE + \
    NEWBURY_ROCKPORT_LINE + PROVIDENCE_STOUGHTON_LINE
UNIQUE_STATIONS = list(set(COMMUTER_RAIL))

Trip = namedtuple('Trip', [
    'trip_id',
    'route_id',
    'direction',
    'scheduled_departure',
    'actual_departure',
    'delay_sec',
    'station'
])


def utc_to_gmt(utc):
    """
    Convert UTC to GMT timeZone
    :param utc: The original time in UTC time.
    :returns: The time in GMT time.
    """
    if utc is None:
        return None
    return utc.replace(tzinfo=timezone.utc).astimezone(tz=None)


def was_alert_issued(trip_alerts, trip_id):
    """
    Determine wheter there is an alert issued with the given trioID
    :param trip_alerts: Dict of trip_id to alerts associated with that trip.
    :returns: True if there were any alerts for the trip with `trip_id`
    """
    return trip_id in trip_alerts and len(trip_alerts[trip_id]) > 0


def deserves_alert(delay):
    """
    determine wheter a given trip_id deserves alert
    :param delay: The number of seconds between scheduled_departure and actual_departure
    :return: True if delay is more than 10 minutes.
    """
    return delay >= 600


def get_alert(trip_alerts, trip_id, scheduled_departure):
    """
    Get the last alert that was sent before the scheduled_departure of the train.
    Note: The scheduled_departure is specific to each station, so this will/may
    return different alerts for different stations in a trip.  This makes
    sense, because the people looking to use the commuter rail are expected to
    be following the alerts prior to arriving/leaving for the station.  The
    last alert that was sent will be the one that we want to use.

    :param trip_alerts: The dict of trip_ids to alerts on each trip.
    :param trip_id: The unique ID of the trip.
    :param scheduled_departure: The datetime of the scheduled_departure of the train
        from a specific station on a specific trip.
    :returns: The last alert that was sent before the scheduled_departure of the train
    """
    if not was_alert_issued(trip_alerts, trip_id):
        return None
    first_alert = trip_alerts[trip_id][0]
    if first_alert.last_modified_dt >= scheduled_departure:
        return first_alert
    return max(
        filter(lambda alert: alert.last_modified_dt >= scheduled_departure,
               trip_alerts[trip_id]),
        key=lambda alert: alert.last_modified_dt)


def get_alert_message(trip_alerts, trip_id, scheduled_departure):
    """
    :param trip_alerts: The dict of trip_ids to alerts on each trip.
    :param trip_id: The unique ID of the trip.
    :param scheduled_departure: The datetime of the scheduled_departure of the train
        from a specific station on a specific trip.
    :returns: The message of the last alert send before the scheduled_departure
        of the train.
    """
    alert = get_alert(trip_alerts, trip_id, scheduled_departure)
    return alert.short_header_text if alert is not None else None


def alert_delay(trip_alerts, trip_id, scheduled_departure):
    """
    compute the alert deplay time, return the delay time
    :param trip_alerts: The dict of trip_ids to alerts on each trip.
    :param trip_id: The unique ID of the trip.
    :param scheduled_departure: The datetime of the scheduled_departure of the train
        from a specific station on a specific trip.
    :returns: The timedelta between the last alert before scheduled_departure
        (or first alert if sent after) and the scheduled_departure.
    """
    first_alert = min(trip_alerts.get(trip_id, []),
                      default=None,
                      key=lambda alert: alert.last_modified_dt)
    if first_alert is None:
        return None
    return first_alert.last_modified_dt - scheduled_departure


def alert_timely(trip_alerts, trip_id, scheduled_departure):
    """
    Compute the timeliness of alert, return the bracket of  alert's timeliness
    If the alert sent out less than 5 mins later of train's scheduled depature, then it's timely,
    otherwise it's not timely
    Go for the first alert for each trip_id !!!
    :param trip_alerts: The dict of trip_ids to alerts on each trip.
    :param trip_id: The unique ID of the trip.
    :param scheduled_departure: The datetime of the scheduled_departure of the train
        from a specific station on a specific trip.
    :returns: True if the last alert arrived within 5 minutes before the scheduled_departure.
    """
    delay = alert_delay(trip_alerts, trip_id, scheduled_departure)
    return delay is not None and delay <= timedelta(seconds=300)


def get_last_modified_dt(trip_alert, trip_id, scheduled_departure):
    """
    get the last modified day of alert to fill in time entry in
    alert_event table in database
    """
    alert = get_alert(trip_alert, trip_id, scheduled_departure)
    return alert.last_modified_dt if alert is not None else None


def get_predicted_delay(trip_alert, trip_id, scheduled_departure):
    """
    parse the alet_message and get the predicted delay
    check the word "minutes", "m", or "min", and grab the time range before these words
    """
    alert = get_alert(trip_alert, trip_id, scheduled_departure)
    if alert is None or alert.short_header_text is None:
        return None
    last = None
    for val in alert.short_header_text.split():
        if val not in {"minutes", "min", "m"}:
            return last
        else:
            last = val
    return None


def delay_accuracy(delay, trip_alert, trip_id, scheduled_departure):
    """
    measure the accuracy of the alert
    if the delaytime is in the predicted-delay time range, then it is accurate.
    if delay is less time lower bound of time range, then it is high,
    if delay is more than upper bound of time range, then it is low
    if no predicted-delay, then no estimate
    """
    predicted_delay = get_predicted_delay(trip_alert, trip_id, scheduled_departure)
    if predicted_delay is None or len(predicted_delay) == 0:
        return None

    timebound = predicted_delay.split('-')
    delay = int(delay)
    lower_bound = int(timebound[0])
    # This helps us handle the exact and timerange cases at the same time
    # because `x <= y <= z` is the same as `x == y == z` if x == z.
    upper_bound = lower_bound if len(timebound) < 2 else int(timebound[1])
    lower_bound *= 60
    upper_bound *= 60
    if lower_bound <= delay <= upper_bound:
        return DelayAccuracy.accurate
    elif delay < lower_bound:
        return DelayAccuracy.high
    elif delay > upper_bound:
        return DelayAccuracy.low


def alert_id_to_trip_id(data):
    """
    :param data:
    :returns: dict of alert_id to trip_id
    """
    alert_to_trip = defaultdict(set)
    for effected_services in data:
        trip_ids = alert_to_trip[effected_services.alert_id]
        trip_ids.add(effected_services.trip_id)
    return alert_to_trip


def alert_time(trip_id_to_alert_ids, trip_id, scheduled_departure):
    """
    :returns: The time that the last alert (prior to scheduled_departure) was
        sent out.  If the first alert sent was after scheduled_departure then
        this function returns the time that the first alert was sent.
    """
    tyme = get_last_modified_dt(trip_id_to_alert_ids, trip_id, scheduled_departure)
    return scheduled_departure if tyme is None else utc_to_gmt(tyme)


class AlertEvaluator:
    """
    AlertEvaluator collects schedule-adherence information from the
    schedule-adherence API and compares it with alerts collected over the day.
    From this information it generates AlertEvent metrics about the accuracy,
    existence, and timeliness of the alerts.
    """

    def __init__(self, target_date):
        self.start_time = datetime.combine(target_date, time(hour=3))
        self.end_time = self.start_time + timedelta(days=1)
        self.db_session = get_db_session()
        self.log = get_log('AlertEvaluator')
        self.schedule_adherence_api = cfg.get('Evaluator', 'schedule_adherence_api')
        self.api_key = cfg.get('Evaluator', 'api_key')

    def read_schedule_adherence(self):
        """
        Collect schedule-adherence information from the schedule-adherence API
        for every station in the commuter-rail system for the target date.
        :returns: A list of Trips containing adherence information
        """
        schedule_adherence = []
        start_time_fmt = int(self.start_time.timestamp())
        end_time_fmt = int(self.end_time.timestamp())
        for station in UNIQUE_STATIONS:
            self.log.info(
                'Getting schedule adherence for %s\t\t%s -> %s',
                station,
                self.start_time,
                self.end_time
            )
            response = requests.get(self.schedule_adherence_api, params={
                'api_key': self.api_key,
                'format': 'json',
                'stop': station,
                'from_datetime': start_time_fmt,
                'to_datetime': end_time_fmt,
            })
            data = response.json()
            schedule_adherences = data.get("schedule_adherences", [])
            for adherence in schedule_adherences:
                try:
                    schedule_adherence.append(Trip(
                        trip_id=adherence['trip_id'],
                        route_id=adherence['route_id'],
                        direction=int(adherence['direction']),
                        scheduled_departure=datetime.fromtimestamp(float(adherence['sch_dt'])),
                        actual_departure=datetime.fromtimestamp(float(adherence['act_dt'])),
                        delay_sec=int(adherence['delay_sec']),
                        station=station
                    ))
                except KeyError as err:
                    self.log.error(
                        'Schedule Adherence datapoint did not contain expected field: %s', err)
        self.log.info('Finished getting schedule-adherence data from API')
        return schedule_adherence

    def trip_id_to_alert_ids(self):
        """
        :returns: dict of trip_id to list of associated alert_ids
        """
        trip_to_alert = defaultdict(list)
        alert_affected_services = self.db_session.query(AlertAffectedService)\
            .filter(AlertAffectedService.trip_id != 'None')
        alerts = self.db_session.query(Alert)\
            .filter(Alert.last_modified_dt >= self.start_time)\
            .filter(Alert.last_modified_dt <= self.end_time)\
            .filter(Alert.effect_name == 'Delay')\
            .all()
        self.log.info("%d delay alerts found in database for time-range", len(alerts))
        data_dictionary = alert_id_to_trip_id(alert_affected_services)
        for i, j in data_dictionary.items():
            for alert in alerts:
                if i == alert.alert_id:
                    for trip in j:
                        trip_to_alert[trip].append(alert)
        return trip_to_alert

    def create_alert_events(self):
        """
        Create AlertEvents based on the previous day of alerts and
            schedule-adherence
        """
        scheduleadherence = self.read_schedule_adherence()
        trip_id_to_alert_ids = self.trip_id_to_alert_ids()
        return map(
            lambda trip: AlertEvent(
                trip_id=trip.trip_id,
                date=self.start_time.date(),
                time=alert_time(
                    trip_id_to_alert_ids, trip.trip_id, trip.scheduled_departure
                ),
                day=calendar.day_name[self.start_time.weekday()],
                route=trip.route_id,
                stop=trip.station,
                direction=Direction(trip.direction),
                short_name="%s Train %s" % (trip.route_id[3:], trip.trip_id[19:]),
                scheduled_departure=trip.scheduled_departure,
                actual_departure=trip.actual_departure,
                delay=timedelta(seconds=trip.delay_sec),
                alert_issued=was_alert_issued(trip_id_to_alert_ids, trip.trip_id),
                deserves_alert=deserves_alert(trip.delay_sec),
                alert_delay=alert_delay(
                    trip_id_to_alert_ids, trip.trip_id, trip.scheduled_departure
                ),
                alert_timely=alert_timely(
                    trip_id_to_alert_ids, trip.trip_id, trip.scheduled_departure
                ),
                alert_text=get_alert_message(
                    trip_id_to_alert_ids, trip.trip_id, trip.scheduled_departure
                ),
                predicted_delay=get_predicted_delay(
                    trip_id_to_alert_ids, trip.trip_id, trip.scheduled_departure
                ),
                delay_accuracy=delay_accuracy(
                    trip.delay_sec, trip_id_to_alert_ids, trip.trip_id, trip.scheduled_departure
                )
            ),
            filter(
                lambda trip: was_alert_issued(trip_id_to_alert_ids, trip.trip_id)
                or deserves_alert(trip.delay_sec),
                scheduleadherence
            )
        )

    def run(self):
        """
        Run the Evaluator
        """
        self.log.info("Running AlertEvaluator for %s to %s", self.start_time, self.end_time)
        metrics = self.create_alert_events()
        for m in metrics:
            try:
                self.db_session.add(m)
                self.db_session.commit()
            except (SQLAlchemyError, psycopg2.Error, psycopg2.Warning):
                self.log.exception("Encountered an error when performing database insertion")
                self.db_session.rollback()


def date_parser(string):
    """
    Converts the input cmd-line argument of form YYY-MM-DD to a date object.
    :param string: The command line argument that should be a date.
    :returns: A date object representing the string.
    """
    d_struct = _time.strptime(string, '%Y-%m-%d')
    return date(year=d_struct.tm_year, month=d_struct.tm_mon, day=d_struct.tm_mday)


def main():
    """
    write result to alert_events table
    """
    parser = argparse.ArgumentParser(
        description="""
        Alert Evaluator looks at the alerts/schedule-adherence for the target
        date and generates a metrics about the alerts that did/should-have
        existed.
        """)
    parser.add_argument(
        '--target_date',
        type=date_parser,
        default=date.today() - timedelta(days=1))
    args = parser.parse_args()
    init_db()
    AlertEvaluator(args.target_date).run()


if __name__ == "__main__":
    main()
