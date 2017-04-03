"""
The archiver module will perform the function of querying
the MBTA APIs that contain relevant data and archiving them
to our database.
"""

import os
import logging
import time
import requests

from mbtaalerts.config import directed_config
from mbtaalerts.database import database
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import DBAPIError
from datetime import datetime, timezone

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%m/%d %H:%M:%S',
    level=os.environ.get("LOGLEVEL", "INFO"))
LOG = logging.getLogger("archive")

def buildAlertEntry(alert):
    """Build a database insertion from alert data"""

    stamp_created = datetime.fromtimestamp(int(alert['created_dt']), timezone.utc)
    stamp_modified = datetime.fromtimestamp(int(alert['last_modified_dt']), timezone.utc)

    entry = {
        'alert_id': str(alert['alert_id']),
        'effect_name': str(alert['effect_name']),
        'effect': str(alert['effect']),
        'cause': str(alert['cause']),
        'header_text': str(alert['header_text']),
        'short_header_text': str(alert['short_header_text']),
        'severity': str(alert['severity']),
        'created_dt': str(stamp_created),
        'last_modified_dt': str(stamp_modified),
        'service_effect_text': str(alert['service_effect_text']),
        'alert_lifecycle': str(alert['alert_lifecycle']),
    }

    return entry

def buildServicesEntry(alert_id, affected_service):
    """Build an affected services insertion"""

    entry = {
        'alert_id': alert_id,
        'route_id': str(affected_service.get('route_id')),
        'trip_id': str(affected_service.get('trip_id', None)),
        'trip_name': str(affected_service.get('trip_name', None)),
    }

    return entry

def buildEffectPeriodsEntry(alert_id, effectPeriod):
    """Build the insertion for an alert's effect period"""

    stamp_start = str(datetime.fromtimestamp(int(effectPeriod['effect_start']), timezone.utc))

    # The effect end time may be empty, which
    # indicates an unknown end time.
    effect_end = effectPeriod['effect_end']
    if effect_end == '':
        stamp_end = None
    else:
        stamp_end = str(datetime.fromtimestamp(int(effectPeriod['effect_end']), timezone.utc))

    entry = {
        'alert_id': alert_id,
        'effect_start': stamp_start,
        'effect_end': stamp_end
    }

    return entry

class Archiver:
    """The archiver takes in raw alert data and stores it in the database."""

    def __init__(self):

        # Load the length of time (seconds) to wait between scans
        self.scan_frequency_sec = directed_config.getint("Archiver", "scan_frequency_sec")

        # Record each version of published alerts we've seen,
        # as a set of (alert_id, last_modified_dt)
        self.known_id_lastmodified_pairs = set()

        # The sqlalchemy connection to our postgres database
        self.connection = None

        # Table metadata loaded from the database schema
        self.alerts_table = None
        self.affected_services_table = None
        self.effect_periods_table = None

    def initializeTableMetadata(self):
        """Load the table schemas and store them for later.."""
        engine = database.databaseConnect()
        metadata = MetaData(bind=engine)

        self.connection = engine.connect()

        # Load table information for alerts
        self.alerts_table = Table('alerts', metadata, autoload=True)
        self.affected_services_table = Table('alert_affected_services', metadata, autoload=True)
        self.effect_periods_table = Table('alert_effect_period', metadata, autoload=True)

    def doUpdateAlerts(self, alerts_info):
        """Convenience method for preparing and then executing the update operation."""
        alerts_ins, affected_services_ins, effect_periods_ins = self.buildAlertInsertions(alerts_info)
        self.performInsertions(alerts_ins, affected_services_ins, effect_periods_ins)

    def buildAlertInsertions(self, alerts_info):
        """Top-level processing of raw alert data"""

        alert_insertions = []

        # These two batches of insertions may
        # have entries from multiple alert_ids
        services_insert_batch = []
        periods_insert_batch = []

        for alert in alerts_info['alerts']:
            alert_id = str(alert['alert_id'])
            commuter = False

            # Record this alert's affected services
            # in case we insert the alert later
            service_insertions = []

            # Check whether this alert affects any commuter rail services
            for affected_service in alert['affected_services']['services']:
                mode_name = affected_service.get('mode_name')

                if mode_name == 'Commuter Rail':
                    commuter = True

                    # A CR affected service entry may (rarely) not have a route_id,
                    # for example during severe-weather broadcast alerts.
                    # Store the alert anyways, but only store the affected services with a route_id.
                    if affected_service.get('route_id'):
                        service_entry = buildServicesEntry(alert_id, affected_service)
                        service_insertions.append(service_entry)

            # Only process commuter rail alerts
            if commuter:
                self.processCommuterAlert(alert, alert_insertions, service_insertions,  \
                    services_insert_batch, periods_insert_batch)

        return alert_insertions, services_insert_batch, periods_insert_batch

    def processCommuterAlert(self, alert, alert_insertions,                             \
        service_insertions, services_insert_batch, periods_insert_batch):
        """Build and add the insertions for a single CR alert"""
        alert_id = str(alert['alert_id'])
        
        # Find existing alerts that match this ID
        last_modified = datetime.fromtimestamp(int(alert['last_modified_dt']), timezone.utc)
        last_modified = last_modified.replace(tzinfo=None)

        id_exists = False
        is_duplicate = False

        # If there were ID matches, check whether this alert is an
        # update (newer modified date) or a duplicate (same modified date)
        for known_id_lastmodified in self.known_id_lastmodified_pairs:

            known_id = known_id_lastmodified[0]
            known_lastmodified = known_id_lastmodified[1]

            if known_id == alert_id:
                id_exists = True

                if known_lastmodified == last_modified:
                    is_duplicate = True

        # Ignore duplicate alerts
        if not is_duplicate:

            LOG.info("Adding alert with ID " + alert_id)

            # Mark this alert version as 'seen' before processing it,
            # so we don't get stuck re-processing it if it fails
            self.known_id_lastmodified_pairs.add((alert_id, last_modified))
            alert_entry = buildAlertEntry(alert)
            alert_insertions.append(alert_entry)

            if not id_exists:
                # This is a brand new alert

                # Record this alert's associated effect periods
                for effect_period in alert['effect_periods']:
                    effect_period_entry = buildEffectPeriodsEntry(alert_id, effect_period)
                    periods_insert_batch.append(effect_period_entry)

                # Add all of the affected services we recorded earlier
                services_insert_batch.extend(service_insertions)

    def performInsertions(self, alert_insertions, service_insertions, effect_period_insertions):
        """Executes the insertions into the database"""
        new_alerts_num = len(alert_insertions)
        new_services_num = len(service_insertions)
        new_periods_num = len(effect_period_insertions)

        if new_alerts_num > 0:
            LOG.info("Inserting %d alerts.", new_alerts_num)
            self.connection.execute(self.alerts_table.insert(), alert_insertions)
        if new_services_num > 0:
            LOG.info("Inserting %d affected services.", new_services_num)
            self.connection.execute(self.affected_services_table.insert(), service_insertions)
        if new_periods_num > 0:
            LOG.info("Inserting %d alert affect periods.", new_periods_num)
            self.connection.execute(self.effect_periods_table.insert(), effect_period_insertions)

def main():

    """
    The entry point for the program
    """
    archiver = Archiver()
    archiver.initializeTableMetadata()

    while True:
        LOG.info("Scanning for new alerts")

        alerts_url = directed_config.get("API", "alerts_url")

        # Build parameters for the alerts API call
        alerts_params = {
            'api_key': directed_config.get("API", "v2_api_key"),
            'include_access_alerts': directed_config.get("Archiver", "include_access_alerts"),
            'include_service_alerts': directed_config.get("Archiver", "include_service_alerts"),
            'format': 'json'
        }

        try:
            response = requests.get(alerts_url, params=alerts_params)
            alerts_info = response.json()
            archiver.doUpdateAlerts(alerts_info)

        # We should continue scanning, since this may
        # just indicate a temporary API outage
        except requests.ConnectionError:
            logging.exception("Unable to retrieve alerts data from API")

        # The below two exceptions should only occur after the
        # problematic alerts are marked as "known", so it's safe
        # to continue scanning (we won't get stuck re-processing them)
        except KeyError:
            logging.exception("Couldn't find required field in alerts response")
        except DBAPIError:
            logging.exception("Encountered an error when performing database insertion")

        LOG.info("Finished scanning new alerts.")

        # Sleep until the next scan
        time.sleep(archiver.scan_frequency_sec)

if __name__ == "__main__":
    main()
