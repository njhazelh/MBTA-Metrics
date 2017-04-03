import enum
import logging
from mbtaalerts.config import directed_config
from mbtaalerts.database import populate
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData, \
    ForeignKey, DateTime, Date, Time, Interval, Boolean, CheckConstraint, Enum

# enums
class Direction(enum.Enum):
    inbound = 0
    outbound = 1

class DelayAccuracy(enum.Enum):
    low = 0
    accurate = 1
    high = 2

def databaseConnect():
    """Load database config settings and connect"""

    # read settings through the configurator
    host = directed_config.get('Database', 'host')
    port = directed_config.get('Database', 'port')
    db = directed_config.get('Database', 'db')
    user = directed_config.get('Database', 'user')
    passwd = directed_config.get('Database', 'pass')

    engine = sqlalchemy.create_engine('postgresql://' + user + ':' + passwd + '@'
                                      + host + ':' + port + '/' + db)
    return engine

def main():

    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # create tables
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

    alert_affected_services = Table('alert_affected_services', metadata,
                                    Column('id', Integer, primary_key=True, autoincrement=True),
                                    Column('alert_id', None, ForeignKey("alerts.alert_id")),
                                    Column('route_id', None, ForeignKey("routes.id")),
                                    Column('trip_id', String(64)),
                                    Column('trip_name', String(64))
                                    )

    engine = databaseConnect()

    # create tables if they don't exist
    connection = engine.connect()
    metadata.create_all(engine)

    # populate routes table
    cr_routes = populate.routes()
    for item in cr_routes:
        values = {'id': item.get('route_id'), 'name': item.get('route_name')}
        insert_route = sqlalchemy.insert(routes, values=values)
        connection.execute(insert_route)

    connection.close()

if __name__ == "__main__":
    main()