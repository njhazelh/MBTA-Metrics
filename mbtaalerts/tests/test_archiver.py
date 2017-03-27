"""
This code will test the archiver module
"""

import unittest
import mbtaalerts.archiver
import ast

class ArchiverTest(unittest.TestCase):
    """
    This code will do tests
    """

    testArchiver = None

    @classmethod
    def setUpClass(self):
        self.testArchiver = mbtaalerts.archiver.Archiver()
        self.testArchiver.initializeTableMetadata()

    @classmethod
    def tearDownClass(self):
        pass
        # Break database connection

    def getNumInsertions(self, insertionBatch):
        return sum(1 for e in insertionBatch)

    #f = "{'alerts': [{'severity': 'Minor', 'timeframe_text': 'ongoing', 'effect_periods': [{'effect_end': '', 'effect_start': '1451727000'}], 'last_modified_dt': '1482495340', 'cause': 'CONSTRUCTION', 'description_text': 'If exiting, return to the fare lobby to use North Station Elevator 912 (lobby to Causeway Street) or pass through the fare gates, walk the full length of the Green Line platform to use North Station Elevator 909 (lobby to Valenti Way). If boarding, cross Causeway Street to use North Station Elevator 912 (lobby to street) or travel one-tenth of a mile down Haverhill Street to the entrance located at the intersection of Haverhill Street and Valenti Way.', 'affected_services': {'elevators': [{'elev_id': '941', 'stops': [{'parent_station': 'place-north', 'stop_id': '70026', 'stop_name': 'North Station - Orange Line Inbound', 'parent_station_name': 'North Station'}, {'parent_station': 'place-north', 'stop_id': '70027', 'stop_name': 'North Station - Orange Line Outbound', 'parent_station_name': 'North Station'}, {'parent_station': 'place-north', 'stop_id': '70205', 'stop_name': 'North Station - Green Line Outbound', 'parent_station_name': 'North Station'}, {'parent_station': 'place-north', 'stop_id': '70206', 'stop_name': 'North Station - Green Line Inbound', 'parent_station_name': 'North Station'}], 'elev_name': 'NORTH STATION - Lobby to Commuter Rail and Boston Garden', 'elev_type': 'Elevator'}], 'services': []}, 'created_dt': '1448467469', 'effect': 'OTHER_EFFECT', 'effect_name': 'Access Issue', 'service_effect_text': 'elevator unavailable', 'alert_lifecycle': 'Ongoing', 'header_text': 'Elevator 941 NORTH STATION - Lobby to the Commuter Rail and Boston Garden will remain closed until further notice due to construction of the Boston Garden Development.', 'cause_name': 'construction', 'alert_id': 105025, 'short_header_text': 'Elev. 941 N Station - Lobby to the Commuter Rail & Boston Garden will remain closed until further notice due to construction of the Boston G'}, {'severity': 'Minor', 'timeframe_text': 'through April 8', 'effect_periods': [{'effect_end': '1491719400', 'effect_start': '1457256600'}], 'last_modified_dt': '1486736527', 'cause': 'CONSTRUCTION', 'description_text': 'Due to Copley Place construction being performed by the Simon Company, the Dartmouth Street underpass  leading to and from the west side of Dartmouth Street at Back Bay Station will be temporarily closed until April 8, 2017.\\r\\n\\r\\nCustomers are encouraged to use the stations main entrance on the east side of Dartmouth Street during the underpass closure. \\r\\n\\r\\nAffected routes:\\r\\nOrange Line\\r\\nFramingham/Worcester Line\\r\\nNeedham Line\\r\\nFranklin Line\\r\\nProvidence/Stoughton Line', 'affected_services': {'elevators': [], 'services': [{'stop_name': 'Back Bay - Outbound', 'mode_name': 'Subway', 'route_name': 'Orange Line', 'stop_id': '70014', 'route_type': '1', 'route_id': 'Orange'}, {'stop_name': 'Back Bay - Inbound', 'mode_name': 'Subway', 'route_name': 'Orange Line', 'stop_id': '70015', 'route_type': '1', 'route_id': 'Orange'}, {'stop_name': 'Back Bay', 'mode_name': 'Commuter Rail', 'route_name': 'Franklin Line', 'stop_id': 'Back Bay', 'route_type': '2', 'route_id': 'CR-Franklin'}, {'stop_name': 'Back Bay', 'mode_name': 'Commuter Rail', 'route_name': 'Needham Line', 'stop_id': 'Back Bay', 'route_type': '2', 'route_id': 'CR-Needham'}, {'stop_name': 'Back Bay', 'mode_name': 'Commuter Rail', 'route_name': 'Providence/Stoughton Line', 'stop_id': 'Back Bay', 'route_type': '2', 'route_id': 'CR-Providence'}, {'stop_name': 'Back Bay', 'mode_name': 'Commuter Rail', 'route_name': 'Framingham/Worcester Line', 'stop_id': 'Back Bay', 'route_type': '2', 'route_id': 'CR-Worcester'}]}, 'created_dt': '1456324215', 'effect': 'UNKNOWN_EFFECT', 'effect_name': 'Station Issue', 'service_effect_text': 'Change at Back Bay', 'alert_lifecycle': 'Ongoing', 'header_text': \"Due to the Simon Company's Copley Place construction, Back Bay Stations Dartmouth Street underpass will remain closed until April 8, 2017.\", 'cause_name': 'construction', 'alert_id': 116064, 'short_header_text': \"Due to the Simon Company's Copley Place construction, Back Bay Stations Dartmouth Street underpass will remain closed until April 8, 2017.\"}, {'severity': 'Minor', 'timeframe_text': 'through June 1', 'effect_periods': [{'effect_end': '1496385000', 'effect_start': '1465979400'}], 'last_modified_dt': '1488303951', 'description_text': 'If entering the station, cross Tremont Street to the Boston Common and use Park Street Elevator 978 to the Green Line westbound platform. Red Line platform access is available via the elevator beyond the fare gates. If exiting the station, please travel down the Winter Street Concourse toward Downtown Crossing Station, exit through the fare gates, and take Downtown Crossing Elevator 892 to the street level.', 'affected_services': {'elevators': [{'elev_id': '804', 'stops': [{'parent_station': 'place-pktrm', 'stop_id': '70075', 'stop_name': 'Park Street - to Ashmont/Braintree', 'parent_station_name': 'Park Street'}, {'parent_station': 'place-pktrm', 'stop_id': '70076', 'stop_name': 'Park Street - to Alewife', 'parent_station_name': 'Park Street'}, {'parent_station': 'place-pktrm', 'stop_id': '70196', 'stop_name': 'Park Street - Green Line - B Branch Berth', 'parent_station_name': 'Park Street'}, {'parent_station': 'place-pktrm', 'stop_id': '70197', 'stop_name': 'Park Street - Green Line - C Branch Berth', 'parent_station_name': 'Park Street'}, {'parent_station': 'place-pktrm', 'stop_id': '70198', 'stop_name': 'Park Street - Green Line - D Branch Berth', 'parent_station_name': 'Park Street'}, {'parent_station': 'place-pktrm', 'stop_id': '70199', 'stop_name': 'Park Street - Green Line - E Branch Berth', 'parent_station_name': 'Park Street'}, {'parent_station': 'place-pktrm', 'stop_id': '70200', 'stop_name': 'Park Street - Green Line Eastbound', 'parent_station_name': 'Park Street'}], 'elev_name': 'PARK STREET - Lechmere Platform & Lobby to Tremont & Winter Sts', 'elev_type': 'Elevator'}], 'services': []}, 'created_dt': '1465496334', 'effect': 'OTHER_EFFECT', 'effect_name': 'Access Issue', 'service_effect_text': 'elevator unavailable', 'alert_lifecycle': 'Ongoing', 'header_text': 'Elevator 804 PARK STREET - Tremont Street to the Lobby will be reconstructed and will be out of service through June 2017.', 'cause': 'UNKNOWN_CAUSE', 'alert_id': 131196, 'short_header_text': 'Elevator 804 PARK STREET - Tremont Street to the Lobby will be reconstructed and will be out of service through June 2017.'}, {'severity': 'Minor', 'timeframe_text': 'until July', 'effect_periods': [{'effect_end': '1500532200', 'effect_start': '1469120386'}], 'last_modified_dt': '1475575597', 'cause': 'CONSTRUCTION', 'description_text': 'Affected routes:\\n69', 'affected_services': {'elevators': [], 'services': [{'stop_name': 'Cambridge St @ Berkshire St', 'mode_name': 'Bus', 'route_name': '69', 'stop_id': '1409', 'route_type': '3', 'route_id': '69'}]}, 'created_dt': '1469120392', 'effect': 'STOP_MOVED', 'effect_name': 'Stop Move', 'service_effect_text': 'Cambridge St @ Berkshire St moved', 'alert_lifecycle': 'Ongoing', 'header_text': 'Due to construction, Cambridge Street @ Berkshire Street (inbound) moved approximately one block to the far side of Berkshire Street until July 2017.', 'cause_name': 'construction', 'alert_id': 137774, 'short_header_text': 'Due to construction, Cambridge St @ Berkshire St (inbound) moved approximately one block to the far side of Berkshire St until July 2017'}, {'severity': 'Minor', 'timeframe_text': 'ongoing', 'effect_periods': [{'effect_end': '', 'effect_start': '1473271880'}], 'last_modified_dt': '1486721038', 'description_text': 'Due to the Merrimack River Bridge project, trains that operate between Bradford and Haverhill will only use the inbound track. Trains that are bused between Haverhill and Bradford will board on the outbound platform at Bradford for service into Boston. Note: Train 216 (1:35 pm from Haverhill) and Train 222 (6:09 pm from Haverhill) are bused from Haverhill Station to Bradford Station. The outbound platform at Bradford may be accessed via the crossing that is south (to the right when facing the tracks from the parking lot) of the mini-high platforms. Alternatively, the outbound platform can also be accessed via the sidewalk from Laurel Avenue.\\r\\n\\r\\n\\r\\nAffected stops:\\r\\nBradford\\r\\nHaverhill', 'affected_services': {'elevators': [], 'services': [{'stop_name': 'Bradford', 'mode_name': 'Commuter Rail', 'route_name': 'Haverhill Line', 'stop_id': 'Bradford', 'route_type': '2', 'route_id': 'CR-Haverhill'}, {'stop_name': 'Haverhill', 'mode_name': 'Commuter Rail', 'route_name': 'Haverhill Line', 'stop_id': 'Haverhill', 'route_type': '2', 'route_id': 'CR-Haverhill'}]}, 'created_dt': '1473271895', 'effect': 'OTHER_EFFECT', 'effect_name': 'Track Change', 'service_effect_text': 'Haverhill Line track change', 'alert_lifecycle': 'Ongoing', 'header_text': 'Please board all trains on the inbound platforms at Haverhill and Bradford except Trains 216 (1:35 pm from Haverhill) and 222 (6:09 pm from Haverhill).', 'cause': 'UNKNOWN_CAUSE', 'alert_id': 144368, 'short_header_text': 'Please board all trains on the inbound platforms at Haverhill & Bradford except Trains 216 & 222'}, {'severity': 'Minor', 'timeframe_text': 'ongoing', 'url': 'http://www.mbta.com/uploadedfiles/Schedules_and_Maps/Bus/161021_North%20Station%20Boston%20Garden%20Advisory.pdf', 'last_modified_dt': '1488807832', 'cause': 'CONSTRUCTION', 'description_text': 'The new path of travel will be along a protected path along Legends Way and across Causeway Street to the station entrances along Haverhill Street. The path will include a barrier and kick-plate for blind and low vision passengers.', 'affected_services': {'elevators': [], 'services': [{'route_name': 'Green Line B', 'route_type': '0', 'route_id': 'Green-B', 'mode_name': 'Subway'}, 

    def testAcceptSingleCommuterRail(self):

        sampleAlerts = """{"alerts":
        [{"alert_id":173753,
        "effect_name":"Delay",
        "effect":"OTHER_EFFECT",
        "cause":"UNKNOWN_CAUSE",
        "header_text":"Fitchburg Train 415 (3:30 pm from N. Station) has departed N. Station & is operating 10-20 minutes late en route to Wachusett due to an earlier mechanical issue.",
        "short_header_text":"Fitchburg Train 415 (3:30pm from N Station) has departed N Station & is operating 10-20 minutes late en route to Wachusett","description_text":"Affected direction: Outbound",
        "severity":"Moderate",
        "created_dt":"1489693393",
        "last_modified_dt":"1489693996",
        "service_effect_text":"Fitchburg Line delay",
        "alert_lifecycle":"New",
        "effect_periods":
            [{"effect_start":"1489693384",
            "effect_end":"1489702080"}],
        "affected_services":
            {"services":
                [{"route_type":"2",
                "mode_name":"Commuter Rail",
                "route_id":"CR-Fitchburg",
                "route_name":"Fitchburg Line",
                "direction_id":"0",
                "direction_name":"Outbound",
                "trip_id":"CR-Weekday-Fall-16-415",
                "trip_name":"415 (3:30 pm from North Station)"}],
            "elevators":
                []
        }}]}"""

        sampleAlertsDict = ast.literal_eval(sampleAlerts)
        alertsIns, affectedServicesIns, effectPeriodsIns = self.testArchiver.buildAlertInsertions(sampleAlertsDict)
        self.assertEqual(self.getNumInsertions(alertsIns), 1)

    def testAcceptMixedServiceAlert(self):
        sampleAlerts = """{"alerts":
        [{"alert_id":173753,
        "effect_name":"Delay",
        "effect":"OTHER_EFFECT",
        "cause":"UNKNOWN_CAUSE",
        "header_text":"Fitchburg Train 415 (3:30 pm from N. Station) has departed N. Station & is operating 10-20 minutes late en route to Wachusett due to an earlier mechanical issue.",
        "short_header_text":"Fitchburg Train 415 (3:30pm from N Station) has departed N Station & is operating 10-20 minutes late en route to Wachusett","description_text":"Affected direction: Outbound",
        "severity":"Moderate",
        "created_dt":"1489693393",
        "last_modified_dt":"1489693996",
        "service_effect_text":"Fitchburg Line delay",
        "alert_lifecycle":"New",
        "effect_periods":
            [{"effect_start":"1489693384",
            "effect_end":"1489702080"}],
        "affected_services":
            {"services":
                [{"route_type":"2",
                "mode_name":"Commuter Rail",
                "route_id":"CR-Fitchburg",
                "route_name":"Fitchburg Line",
                "direction_id":"0",
                "direction_name":"Outbound",
                "trip_id":"CR-Weekday-Fall-16-415",
                "trip_name":"415 (3:30 pm from North Station)"}],
            "elevators":
                []
        }}]}"""

        sampleAlertsDict = ast.literal_eval(sampleAlerts)
        alertsIns, affectedServicesIns, effectPeriodsIns = self.testArchiver.buildAlertInsertions(sampleAlertsDict)
        self.assertEqual(self.getNumInsertions(alertsIns), 1)

    def testIgnoreNonCommuterRail(self):
        pass

    def testAddManyAffectedServices(self):
        pass

    def testIndefiniteEffectPeriod(self):
        pass

    def test_example2(self):
        pass
        """
        Check that we can access the archiver module
        """
        #self.assertEqual(1, mbtaalerts.archiver.helper_function())
