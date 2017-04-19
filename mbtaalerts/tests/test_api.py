"""
This code will test the archiver module
"""

import unittest
import json
from datetime import date, time, datetime

from mbtaalerts.database.models import AlertEvent
from mbtaalerts.database.database import setup_engine, init_db, reset_engine, get_db_session


class ApiTest(unittest.TestCase):
    def setUp(self):
        setup_engine('sqlite://')
        import mbtaalerts.api as api
        api.APP.testing = True
        self.app = api.APP.test_client()
        self.db = get_db_session()
        init_db()


    def tearDown(self):
        reset_engine()


    def check_range(self, data, startTime, endTime, startDate, endDate):
        for item in data:
            self.assertTrue('time' in item)
            self.assertTrue('date' in item)
            tm = datetime.strptime(item['time'], '%H:%M:%S')
            dt = datetime.strptime(item['date'], '%Y-%m-%d')
            self.assertLessEqual(dt.date(), date(2017, 4, 28))
            self.assertGreaterEqual(dt.date(), date(2017, 4, 25))
            self.assertGreaterEqual(tm.time(), time(8))
            self.assertLessEqual(tm.time(), time(13))

    def get(self, url, params):
        pairs = []
        for key, val in params.items():
            pairs.append("%s=%s" % (key, val))
        if len(pairs) != 0:
            url = url + "?" + "&".join(pairs)
        try:
            response = self.app.get(url)
            data = json.loads(response.data.decode('utf-8'))
            return response, data
        except Exception as e:
            print(response.data)
            self.fail()


    def test_get_alert_events(self):
        self.db.add_all([
            AlertEvent(date=date(2017, 4, 25), time=time(9)),
            AlertEvent(date=date(2017, 4, 26), time=time(13)),
            AlertEvent(date=date(2017, 4, 27), time=time(8)),
            AlertEvent(date=date(2017, 4, 28), time=time(11)),
        ])
        self.db.commit()
        self.assertEqual(self.db.query(AlertEvent).count(), 4)

        _, data = self.get('/data/alert_events', {
            'startDate': '2017-04-25',
            'endDate': '2017-04-28',
            'startTime': '08:00:00',
            'endTime': '13:00:00',
        })
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 4)
        self.check_range(data['data'],
                         time(8), time(13),
                         date(2017, 4, 25), date(2017, 4, 28))

        _, data = self.get('/data/alert_events', {
            'startDate': '2017-04-25',
            'endDate': '2017-04-28',
            'startTime': '10:00:00',
            'endTime': '13:00:00',
        })
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 2)
        self.check_range(data['data'],
                         time(10), time(13),
                         date(2017, 4, 25), date(2017, 4, 28))

        _, data = self.get('/data/alert_events', {
            'startDate': '2017-04-25',
            'endDate': '2017-04-28',
            'startTime': '08:00:00',
            'endTime': '10:00:00',
        })
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 2)
        self.check_range(data['data'],
                         time(8), time(10),
                         date(2017, 4, 25), date(2017, 4, 28))

        _, data = self.get('/data/alert_events', {
            'startDate': '2017-04-27',
            'endDate': '2017-04-28',
            'startTime': '08:00:00',
            'endTime': '13:00:00',
        })
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 2)
        self.check_range(data['data'],
                         time(8), time(13),
                         date(2017, 4, 27), date(2017, 4, 28))


        _, data = self.get('/data/alert_events', {
            'startDate': '2017-04-25',
            'endDate': '2017-04-26',
            'startTime': '08:00:00',
            'endTime': '13:00:00',
        })
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 2)
        self.check_range(data['data'],
                         time(8), time(13),
                         date(2017, 4, 25), date(2017, 4, 26))

        _, data = self.get('/data/alert_events', {
            'startDate': '2017-04-25',
            'endDate': '2017-04-26',
            'startTime': '08:00:00',
            'endTime': '10:00:00',
        })
        self.assertTrue('data' in data)
        self.assertEqual(len(data['data']), 1)
        self.check_range(data['data'],
                         time(8), time(10),
                         date(2017, 4, 25), date(2017, 4, 26))
