import configparser
import enum
import logging
import requests
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, \
    ForeignKey, ARRAY, DateTime, Date, Time, Interval, Boolean, CheckConstraint, Enum

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# read from settings file
config = configparser.ConfigParser()
config.read("settings.cfg")
host = config.get('Database', 'host')
port = config.get('Database', 'port')
db = config.get('Database', 'db')
user = config.get('Database', 'user')
passwd = config.get('Database', 'pass')

# enums
class Direction(enum.Enum):
    inbound = 0
    outbound = 1

class DelayAccuracy(enum.Enum):
    low = 0
    accurate = 1
    high = 2

# tables
metadata = MetaData()

routes = Table('routes', metadata,
               Column('id', String(32), primary_key=True, unique=True),
               Column('name', String(32), nullable=False))

stops = Table('stops', metadata,
               Column('id', String(32), primary_key=True, unique=True),
               Column('name', String(32), nullable=False))

alert_events = Table('alert_events', metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('trip_id', String(100)),
                     Column('date', Date),
                     Column('time', Time),
                     Column('day', Integer, CheckConstraint('day >= 0 AND day <= 6')),
                     Column('route', None, ForeignKey("routes.id")),
                     Column('stop', String(32)),
                     Column('direction', Enum(Direction)),
                     Column('short_name', String(64)),
                     Column('scheduled_departure', DateTime),
                     Column('actual_departure', DateTime),
                     Column('delay', Interval),
                     Column('alert_issued', Boolean),
                     Column('time', Time),
                     Column('deserves_alert', Boolean),
                     Column('alert_delay', Interval),
                     Column('alert_timely', Boolean),
                     Column('alert_text', String(300)),
                     Column('predicted_delay', Interval),
                     Column('delay_accuracy', Enum(DelayAccuracy))
                     )

alerts = Table('alerts', metadata,
               Column('alert_id', Integer, primary_key=True),
               Column('effect_name', String(32)),
               Column('effect', String(32)),
               Column('cause', String(64)),
               Column('header_text', String(256)),
               Column('short_header_text', String(256)),
               Column('severity', String(16)),
               Column('created_dt', DateTime),
               Column('last_modified_dt', DateTime),
               Column('service_effect_text', String(256)),
               Column('alert_lifecycle', String(16))
               )

alert_effect_period = Table('alert_effect_period', metadata,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('alert_id', None, ForeignKey("alerts.alert_id")),
                            Column('effect_start', DateTime),
                            Column('effect_end', DateTime)
                            )

alert_affected_services = Table('alert_effect_period', metadata,
                                Column('id', Integer, primary_key=True, autoincrement=True),
                                Column('alert_id', None, ForeignKey("alerts.alert_id")),
                                Column('route_id', None, ForeignKey("routes.route_id")),
                                Column('trip_id', String(64)),
                                Column('trip_name', String(64))
                                )

# populate routes and stops tables, commuter rail only



# create tables if they don't exist
engine = sqlalchemy.create_engine('postgresql://' + user + ':' + passwd + '@'
                                  + host + ':' + port + '/' + db)
connection = engine.connect()
metadata.create_all(engine)
connection.close()




