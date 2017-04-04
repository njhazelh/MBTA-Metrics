"""
The archiver module will perform the function of querying
the MBTA APIs that contain relevant data and archiving them
to our database.
"""

import os
import time
import requests

from mbtaalerts.logging import get_log
from mbtaalerts.config import directed_config as cfg
from mbtaalerts.database import database as db
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import DBAPIError
from datetime import datetime, timezone
from mbtaalerts.database.models \
    import Alert, AlertAffectedService, AlertEffectPeriod

LOG = get_log('archiver')

def buildAlertEntry(alert):
    """Build a database insertion from alert data"""
    stamp_created = datetime.fromtimestamp(int(alert['created_dt']),
                                           timezone.utc)
    stamp_modified = datetime.fromtimestamp(int(alert['last_modified_dt']),
                                            timezone.utc)
    return Alert(alert_id=str(alert['alert_id']),
                 effect_name=str(alert['effect_name']),
                 effect=str(alert['effect']),
                 cause=str(alert['cause']),
                 header_text=str(alert['header_text']),
                 short_header_text=str(alert['short_header_text']),
                 severity=str(alert['severity']),
                 created_dt=stamp_created,
                 last_modified_dt=stamp_modified,
                 service_effect_text=str(alert['service_effect_text']),
                 alert_lifecycle=str(alert['alert_lifecycle']))

def buildServicesEntry(alert_id, affected_service):
    """Build an affected services insertion"""
    route_id=str(affected_service.get('route_id'))
    trip_id=str(affected_service.get('trip_id', None))
    trip_name=str(affected_service.get('trip_name', None))
    return AlertAffectedService(alert_id=alert_id,
                                 route_id=route_id,
                                 trip_id=trip_id,
                                 trip_name=trip_name)

def buildEffectPeriodsEntry(alert_id, effectPeriod):
    """Build the insertion for an alert's effect period"""
    stamp_start = datetime.fromtimestamp(int(effectPeriod['effect_start']),
                                         timezone.utc)
    # The effect end time may be empty, which indicates an unknown end time.
    stamp_end = None \
        if len(effectPeriod['effect_end']) == 0 \
        else datetime.fromtimestamp(int(effectPeriod['effect_end']),
                                    timezone.utc)
    return AlertEffectPeriod(alert_id=alert_id,
                             effect_start=stamp_start,
                             effect_end=stamp_end)

class Archiver:
    """The archiver takes in raw alert data and stores it in the database."""

    def __init__(self):
        # Load the length of time (seconds) to wait between scans
        self.scan_frequency_sec = cfg.getint("Archiver", "scan_frequency_sec")
        # How often (every n scans) should we clear the known-alerts set
        self.cull_frequency = cfg.getint("Archiver", "cull_frequency")
        # How many cycles until the next cull?
        self.next_cull = self.cull_frequency
        # Record each version of published alerts we've seen,
        # as a set of (alert_id, last_modified_dt)
        self.known_id_lastmodified_pairs = set()
        self.alerts_params = {
            'api_key': cfg.get("API", "v2_api_key"),
            'include_access_alerts': cfg.get("Archiver", "include_access_alerts"),
            'include_service_alerts': cfg.get("Archiver", "include_service_alerts"),
            'format': 'json'
        }
        self.alerts_url = cfg.get("API", "alerts_url")

    def storeAlerts(self, alerts_info):
        """Convenience method for preparing and then executing the update operation."""
        alerts_ins, \
        affected_services_ins, \
        effect_periods_ins  = self.buildAlertInsertions(alerts_info)
        self.insertData(alerts_ins, affected_services_ins, effect_periods_ins)

    def buildAlertInsertions(self, alerts_info):
        """Top-level processing of raw alert data"""
        # These two batches of insertions may have entries from multiple alert_ids
        services_insert_batch = []
        periods_insert_batch = []
        alert_insertions = []

        for alert in alerts_info['alerts']:
            alert_id = str(alert['alert_id'])
            commuter = False
            # Record this alert's affected services in case we insert the alert later
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
            if commuter:
                self.processCommuterAlert(alert,
                                          alert_insertions,
                                          service_insertions,
                                          services_insert_batch,
                                          periods_insert_batch)
        return alert_insertions, services_insert_batch, periods_insert_batch

    def processCommuterAlert(self, alert,
                             alert_insertions, service_insertions,
                             services_insert_batch, periods_insert_batch):
        """Build and add the insertions for a single CR alert"""
        alert_id = str(alert['alert_id'])

        # Find existing alerts that match this ID
        last_modified = datetime\
            .fromtimestamp(int(alert['last_modified_dt']), timezone.utc)\
            .replace(tzinfo=None)

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
            LOG.info("Adding alert with ID %s", alert_id)
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

    def insertData(self, alert_insertions, service_insertions, effect_period_insertions):
        """Executes the insertions into the database"""
        new_alerts_num = len(alert_insertions)
        new_services_num = len(service_insertions)
        new_periods_num = len(effect_period_insertions)
        if new_alerts_num > 0:
            LOG.info("Inserting %d alerts.", new_alerts_num)
            db.DB_SESSION.add_all(alert_insertions)
        if new_services_num > 0:
            LOG.info("Inserting %d affected services.", new_services_num)
            db.DB_SESSION.add_all(service_insertions)
        if new_periods_num > 0:
            LOG.info("Inserting %d alert affect periods.", new_periods_num)
            db.DB_SESSION.add_all(effect_period_insertions)
        db.DB_SESSION.commit()

    def updateKnownAlerts(self, alerts_info):
        """Remove unpublished alerts from the known alert set"""
        if self.next_cull != 0:
            self.next_cull -= 1
            return

        self.next_cull = self.cull_frequency
        items_to_cull = []
        published_alerts = alerts_info['alerts']
        # Look through our currently-known alert versions
        for known_id_lastmodified in self.known_id_lastmodified_pairs:
            cull_known_pair = True
            # Save this pair if there's an active alert with its ID
            for published_alert in published_alerts:
                published_alert_id = str(published_alert['alert_id'])
                if known_id_lastmodified[0] == published_alert_id:
                    cull_known_pair = False
            if cull_known_pair:
                items_to_cull.append(known_id_lastmodified)
        # Remove the pairs from our set which have currently-published IDs
        for pair in items_to_cull:
            self.known_id_lastmodified_pairs.discard(pair)
        LOG.info("Purging %d unpublished alerts from known alert set", len(items_to_cull))

    def run(self):
        while True:
            LOG.info("Scanning for new alerts")
            try:
                response = requests.get(self.alerts_url, params=self.alerts_params)
                alerts_info = response.json()
                self.updateKnownAlerts(alerts_info)
                self.storeAlerts(alerts_info)
            except requests.ConnectionError:
                # This may just indicate a temporary API outage
                LOG.exception("Unable to retrieve alerts data from API")
            except KeyError:
                # Should only happen after problematic alerts are marked as known
                # so it's safe to continue scanning (we won't get stuck re-processing them).
                LOG.exception("Couldn't find required field in alerts response")
            except DBAPIError:
                # Should only happen after problematic alerts are marked as known
                # so it's safe to continue scanning (we won't get stuck re-processing them).
                LOG.exception("Encountered an error when performing database insertion")
            LOG.info("Finished scanning new alerts")
            time.sleep(self.scan_frequency_sec)

def main():

    """
    The entry point for the program
    """
    db.init_db()
    Archiver().run()

if __name__ == "__main__":
    main()
