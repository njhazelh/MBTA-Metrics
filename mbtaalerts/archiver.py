"""
The archiver module will perform the function of querying
the MBTA APIs that contain relevant data and archiving them
to our database.
"""

import os
import logging
import time
import requests

import configparser
import sqlalchemy
import itertools
# from sqlalchemy.sql import table, column, select, update, insert
from sqlalchemy import *
from datetime import datetime, timezone

connection = None

alertsTable = None
affectedServicesTable = None
effectPeriodsTable = None

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%m/%d %H:%M:%S',
    level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

def buildAlertEntry(alert):

    stampCreated = datetime.fromtimestamp(int(alert['created_dt']), timezone.utc)
    stampModified = datetime.fromtimestamp(int(alert['last_modified_dt']), timezone.utc)

    entry = {
            'alert_id': str(alert['alert_id']),
            'effect_name': str(alert['effect_name']),
            'effect': str(alert['effect']),
            'cause': str(alert['cause']),
            'header_text': str(alert['header_text']),
            'short_header_text': str(alert['short_header_text']),
            'severity': str(alert['severity']),
            'created_dt': str(stampCreated),
            'last_modified_dt': str(stampModified),
            'service_effect_text': str(alert['service_effect_text']),
            'alert_lifecycle': str(alert['alert_lifecycle']),
            }

    return entry

def buildAffectedServcesEntry(alertId, affectedService):
    entry = {
            'alert_id': alertId,
            'route_id': str(affectedService.get('route_id', None)),
            'trip_id': str(affectedService.get('trip_id', "")),
            'trip_name': str(affectedService.get('trip_name', "")),
            }

    return entry


def buildEffectPeriodsEntry(alertId, effectPeriod):


    stampStart = str(datetime.fromtimestamp(int(effectPeriod['effect_start']), timezone.utc))

    # The effect end time may be empty if it's not known
    effectEnd = effectPeriod['effect_end']
    if (effectEnd != ''):
        stampEnd = str(datetime.fromtimestamp(int(effectPeriod['effect_end']), timezone.utc))
    else:
        stampEnd = None

    entry = {
            'alert_id': alertId,
            'effect_start': stampStart,
            'effect_end': stampEnd
            }

    return entry

def databaseConnect():

    config = configparser.ConfigParser()
    config.read("../settings.cfg")
    host = config.get('Database', 'host')
    port = config.get('Database', 'port')
    db = config.get('Database', 'db')
    user = config.get('Database', 'user')
    passwd = config.get('Database', 'pass')

    engine = sqlalchemy.create_engine('postgresql://' + user + ':' + passwd + '@'
                                      + host + ':' + port + '/' + db)

    return engine

def buildInsertions(alertsInfo):

    alertInsertions = []
    affectedServiceInsertionLists = []
    effectPeriodInsertionLists = []

    for alert in alertsInfo['alerts']:
        alertId = str(alert['alert_id'])
        commuter = False

        affectedServiceInsertions = []
        effectPeriodInsertions = []

        # If this alert affects a commuter rail service, it's relevant
        for affectedService in alert['affected_services']['services']:
            modeName = affectedService.get('mode_name')
            if (modeName == 'Commuter Rail'):
                commuter = True

                affectedServiceEntry = buildAffectedServcesEntry(alertId, affectedService)
                affectedServiceInsertions.append(affectedServiceEntry)

        for effectPeriod in alert['effect_periods']:

            effectPeriodEntry = buildEffectPeriodsEntry(alertId, effectPeriod)
            effectPeriodInsertions.append(effectPeriodEntry)

        if commuter:
            alertEntry = buildAlertEntry(alert)

            # Find existing alerts that match this ID
            # If there's a match and the timestamp is newer, add and increment 'version'
            s = select([alertsTable]).where(alertsTable.c.alert_id == alertId)
            matches = connection.execute(s)
            numMatches = 0

            # TODO if null here?
            lastModDate = datetime.fromtimestamp(int(alert['last_modified_dt']), timezone.utc)
            lastModDate = lastModDate.replace(tzinfo=None)

            shouldInsert = True
            numDuplicates = 0

            for row in matches:

                numDuplicates += 1

                if (str(row.last_modified_dt) == str(lastModDate)):
                    shouldInsert == False
                else:
                    numDuplicates
                # Otherwise, we found an alert ID match with new last-modified stamp
                # We should reinsert the alert as a duplicate but increment the 'version'

            # TODO don't re-insert affected services or effect periods for alert updates?
            if (numDuplicates == 0):
                alertInsertions.append(alertEntry)
                affectedServiceInsertionLists.append(affectedServiceInsertions)
                effectPeriodInsertionLists.append(effectPeriodInsertions)

            #else:
            #    alertUpdates.append(alertEntry)

    return alertInsertions, affectedServiceInsertionLists, effectPeriodInsertionLists

def performInsertions(alertInsertions, affectedServiceInsertionLists, effectPeriodInsertionLists):
    affectedServiceInsertions = []
    effectPeriodInsertions = []

    # Combine all of the alerts' affected services into a single batch
    # This lets us perform a single database update
    for affectedServiceInsertion in [item for sublist in affectedServiceInsertionLists for item in sublist]:
        affectedServiceInsertions.append(affectedServiceInsertion)

    for effectPeriodInsertion in [item for sublist in effectPeriodInsertionLists for item in sublist]:
        effectPeriodInsertions.append(effectPeriodInsertion)

    newAlertsNum = len(alertInsertions)
    newServicesNum = len(affectedServiceInsertions)
    newPeriodsNum = len(effectPeriodInsertions)
    
    if (newAlertsNum > 0):
        print("Inserting " + str(newAlertsNum) + " new alerts.")
        alertIns = connection.execute(alertsTable.insert(), alertInsertions)
    if (newServicesNum > 0):
        print("Inserting " + str(newServicesNum) + " new affected services.")
        serviceIns = connection.execute(affectedServicesTable.insert(), affectedServiceInsertions)
    if (newPeriodsNum > 0):
        print("Inserting " + str(newPeriodsNum) + " new alert effect periods.")
        periodIns = connection.execute(effectPeriodsTable.insert(), effectPeriodInsertions)

def main():
    """
    The entry point for the program
    """

    engine = databaseConnect()
    metadata = MetaData(bind=engine)

    global connection
    connection = engine.connect()

    # Load table information for alerts
    global alertsTable, affectedServicesTable, effectPeriodsTable
    alertsTable = Table('alerts', metadata, autoload=True)
    affectedServicesTable = Table('alert_affected_services', metadata, autoload=True)
    effectPeriodsTable = Table('alert_effect_period', metadata, autoload=True)

    requestUrl = "http://realtime.mbta.com/developer/api/v2/alerts?"
    requestUrl += "api_key=wX9NwuHnZU2ToO7GmGR9uw&"
    requestUrl += "include_access_alerts=false&"
    requestUrl += "include_service_alerts=true&"
    requestUrl += "format=json"

    r = requests.get(requestUrl)
    alertsInfo = r.json()

    alertInsertions, affectedServiceInsertionLists, effectPeriodInsertionLists = buildInsertions(alertsInfo)
    performInsertions(alertInsertions, affectedServiceInsertionLists, effectPeriodInsertionLists)

    print("Finished scanning for updates.")

if __name__ == "__main__":
    main()
