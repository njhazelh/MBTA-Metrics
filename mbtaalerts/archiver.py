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
# from sqlalchemy.sql import table, column, select, update, insert
from sqlalchemy import *

connection = None

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%m/%d %H:%M:%S',
    level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

def buildAlertEntry(alert):
    entry = {
            'alert_id': str(alert['alert_id']),
            'effect_name': str(alert['effect_name']),
            'effect': str(alert['effect']),
            'cause': str(alert['cause']),
            'header_text': str(alert['header_text']),
            'short_header_text': str(alert['short_header_text']),
            'severity': str(alert['severity']),
            #'created_dt': str(alert['created_dt']),
            #'last_modified_dt': str(alert['last_modified_dt']),
            'service_effect_text': str(alert['service_effect_text']),
            'alert_lifecycle': str(alert['alert_lifecycle']),
            }

    return entry

def buildAffectedServcesEntry(alertId, affectedService):
    entry = {
            'alert_id': alertId,
            'route_id': str(affectedService.get('route_id', "")),
            'trip_id': str(affectedService.get('trip_id', "")),
            'trip_name': str(affectedService.get('trip_name', "")),
            }

    return entry


def buildEffectPeriodsEntry(alertId, effectPeriod):
    entry = {
            'alert_id': alertId,
            'effect_start': str(effectPeriod['effect_start']),
            'effect_end': str(effectPeriod['effect_end'])
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

def buildInsertions(alertsTable, alertsInfo):

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

            s = select([alertsTable]).where(alertsTable.c.alert_id == alertId)
            matches = connection.execute(s)
            numMatches = 0
            for row in matches:
                numMatches += 1

            # If this alert is new, insert it
            # Otherwise, update the existing alert
            if (numMatches == 0):
                alertInsertions.append(alertEntry)
            #else:
            #    alertUpdates.append(alertEntry)

            affectedServiceInsertionLists.append(affectedServiceInsertions)
            effectPeriodInsertionLists.append(effectPeriodInsertions)

    return alertInsertions, affectedServiceInsertionLists, effectPeriodInsertionLists

def main():
    """
    The entry point for the program
    """

    engine = databaseConnect()
    metadata = MetaData(bind=engine)

    global connection
    connection = engine.connect()

    # Load table information for alerts
    alertsTable = Table('alerts', metadata, autoload=True)
    affectedServicesTable = Table('alert_affected_services', metadata, autoload=True)
    effectPeriodsTable = Table('alert_effect_period', metadata, autoload=True)

    alertUpdates = []

    requestUrl = "http://realtime.mbta.com/developer/api/v2/alerts?api_key=wX9NwuHnZU2ToO7GmGR9uw&include_access_alerts=false&include_service_alerts=true&format=json"
    r = requests.get(requestUrl)
    alertsInfo = r.json()

    alertInsertions, affectedServiceInsertionLists, effectPeriodInsertionLists = buildInsertions(alertsTable, alertsInfo)
                 
    insResult = connection.execute(alertsTable.insert(), alertInsertions)
    print("Alert nsertions: " + str(insResult))

    # for affectedServiceInsertions in affectedServiceInsertionLists:
        
    #     insResult = connection.execute(affectedServicesTable.insert(), affectedServiceInsertions)
    #     print("Affected service insertions: " + str(insResult))

    #upResult = connection.execute(alertsTable.update(), alertUpdates)
    #print("Updates: " + str(upResult))

if __name__ == "__main__":
    main()
