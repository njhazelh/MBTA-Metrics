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
from sqlalchemy import *
from datetime import datetime, timezone

connection = None

alertsTable = None
affectedServicesTable = None
effectPeriodsTable = None

SCAN_INTERVAL_SECONDS = 60

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%m/%d %H:%M:%S',
    level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

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

def buildAlertEntry(alert, version):

    stampCreated = datetime.fromtimestamp(int(alert['created_dt']), timezone.utc)
    stampModified = datetime.fromtimestamp(int(alert['last_modified_dt']), timezone.utc)

    entry = {
            'alert_id': str(alert['alert_id']),
            #'version': str(version),
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

def buildAffectedServicesEntry(alertId, affectedService):

    entry = {
            'alert_id': alertId,
            'route_id': str(affectedService.get('route_id')),
            'trip_id': str(affectedService.get('trip_id', None)),
            'trip_name': str(affectedService.get('trip_name', None)),
            }

    return entry


def buildEffectPeriodsEntry(alertId, effectPeriod):

    stampStart = str(datetime.fromtimestamp(int(effectPeriod['effect_start']), timezone.utc))

    # The effect end time may be empty, which
    # indicates an unknown end time.
    effectEnd = effectPeriod['effect_end']
    if (effectEnd == ''):
        stampEnd = None
    else:
        stampEnd = str(datetime.fromtimestamp(int(effectPeriod['effect_end']), timezone.utc))

    entry = {
            'alert_id': alertId,
            'effect_start': stampStart,
            'effect_end': stampEnd
            }

    return entry

def buildInsertions(alertsInfo):

    alertInsertions = []

    # These two batches of insertions may
    # have entries from multiple alertIDs
    affectedServiceInsertionBatch = []
    effectPeriodInsertionBatch = []

    for alert in alertsInfo['alerts']:
        alertId = str(alert['alert_id'])
        commuter = False

        # Record this alert's affected services
        # in case we insert the alert later
        affectedServiceInsertions = []
        
        # Check whether this alert affects any commuter rail services
        for affectedService in alert['affected_services']['services']:
            modeName = affectedService.get('mode_name')
            if (modeName == 'Commuter Rail'):
                commuter = True

                # A commuter rail alert may (rarely) not have a route_id
                if (affectedService.get('route_id')):
                    affectedServiceEntry = buildAffectedServicesEntry(alertId, affectedService)

                affectedServiceInsertions.append(affectedServiceEntry)

        # Only process commuter rail alerts
        if commuter:

            isUpdate = False
            isDuplicate = False

            # Find existing alerts that match this ID
            # TODO: only search a limited range of previous alerts/hours?
            s = select([alertsTable]).where(alertsTable.c.alert_id == alertId)

            idMatches = connection.execute(s)

            lastModDate = datetime.fromtimestamp(int(alert['last_modified_dt']), timezone.utc)
            lastModDate = lastModDate.replace(tzinfo=None)

            numMatches = 0

            # If there were ID matches, check whether this alert is an
            # update (newer modified date) or a duplicate (same modified date)
            for sameIdAlert in idMatches:
                numMatches += 1 
                if (str(sameIdAlert.last_modified_dt) == str(lastModDate)):
                    isDuplicate = True
                else:
                    isUpdate = True

            # Ignore duplicate alerts
            if (not isDuplicate):
                version = numMatches + 1

                if (isUpdate):
                    LOG.info("Found updated alert with ID " + alertId)
                    continue # TODO: allow insertion when version is implemented
                    # TODO: also update entries in affected services / effect periods tables?
                else:
                    LOG.info("Found new alert with ID " + alertId)

                alertEntry = buildAlertEntry(alert, version)
                alertInsertions.append(alertEntry)

                # Record this alert's associated effect periods
                for effectPeriod in alert['effect_periods']:
                    effectPeriodEntry = buildEffectPeriodsEntry(alertId, effectPeriod)
                    effectPeriodInsertionBatch.append(effectPeriodEntry)

                # Add all of the affected services we recorded earlier
                affectedServiceInsertionBatch.extend(affectedServiceInsertions)

    return alertInsertions, affectedServiceInsertionBatch, effectPeriodInsertionBatch

def performInsertions(alertInsertions, affectedServiceInsertions, effectPeriodInsertions):
    newAlertsNum = len(alertInsertions)
    newServicesNum = len(affectedServiceInsertions)
    newPeriodsNum = len(effectPeriodInsertions)
    
    if (newAlertsNum > 0):
        LOG.info("Inserting " + str(newAlertsNum) + " alerts.")
        alertIns = connection.execute(alertsTable.insert(), alertInsertions)
    if (newServicesNum > 0):
        LOG.info("Inserting " + str(newServicesNum) + " affected services.")
        serviceIns = connection.execute(affectedServicesTable.insert(), affectedServiceInsertions)
    if (newPeriodsNum > 0):
        LOG.info("Inserting " + str(newPeriodsNum) + " alert effect periods.")
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

    # TODO make this configurable
    requestUrl = "http://realtime.mbta.com/developer/api/v2/alerts?"
    requestUrl += "api_key=wX9NwuHnZU2ToO7GmGR9uw&"
    requestUrl += "include_access_alerts=false&"
    requestUrl += "include_service_alerts=true&"
    requestUrl += "format=json"

    while True:
        LOG.info("Scanning for new alerts")

        r = requests.get(requestUrl)
        alertsInfo = r.json()

        alertsIns, affectedServicesIns, effectPeriodsIns = buildInsertions(alertsInfo)
        performInsertions(alertsIns, affectedServicesIns, effectPeriodsIns)

        LOG.info("Finished scanning new alerts.")

        # Sleep for 1 minute
        time.sleep(SCAN_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
