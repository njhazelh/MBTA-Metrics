from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Interval, Boolean, ForeignKey, CheckConstraint, \
    Enum
import enum


# enums
class Direction(enum.Enum):
    inbound = 0
    outbound = 1


class DelayAccuracy(enum.Enum):
    low = 0
    accurate = 1
    high = 2


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)


class Routes(Base):
    __tablename__ = 'routes'
    id = Column(String(32), primary_key=True, unique=True)
    name = Column(String(32), nullable=False)

    alert_affected_services = relationship("AlertAffectedServices", backref="routes",
                                           order_by="AlertAffectedServices.id")
    alert_events = relationship("AlertEvents", backref="routes", order_by="AlertEvents.id")


class Stops(Base):
    __tablename__ = 'stops'

    id = Column(String(32), primary_key=True, unique=True)
    name = Column(String(32), nullable=False)


class Alerts(Base):
    __tablename__ = 'alerts'

    alert_id = Column(Integer)
    effect_name = Column(String(32))
    effect = Column(String(32))
    cause = Column(String(64))
    header_text = Column(String(256))
    short_header_text = Column(String(256))
    severity = Column(String(16))
    created_dt = Column(DateTime)
    last_modified_dt = Column(DateTime)
    service_effect_text = Column(String(256))
    alert_lifecycle = Column(String(16))

    alert_effect_periods = relationship("AlertEffectPeriod", backref="alerts", order_by="AlertEffectPeriod.id")
    alert_affected_services = relationship("AlertAffectedServices", backref="alerts",
                                           order_by="AlertAffectedServices.id")


class AlertEffectPeriod(Base):
    __tablename__ = 'alert_effect_period'
    alert_id = Column(Integer)
    effect_start = Column(DateTime)
    effect_end = Column(DateTime)


class AlertAffectedServices(Base):
    __tablename__ = 'alert_affected_services'
    alert_id = Column(Integer)
    route_id = Column(String(32))
    trip_id = Column(String(64))
    trip_name = Column(String(64))


class AlertEvents(Base):
    __tablename__ = 'alert_events'
    trip_id = Column(String(64))
    date = Column(Date)
    time = Column(Time)
    day = Column(Integer, CheckConstraint('day >= 0 AND day <= 6'))
    route = Column(String(32))
    stop = Column(String(32))
    direction = Column(Enum(Direction))
    short_name = Column(String(64))
    scheduled_departure = Column(DateTime)
    actual_departure = Column(DateTime)
    delay = Column(Interval)
    alert_issued = Column(Boolean)
    deserves_alert = Column(Boolean)
    alert_delay = Column(Interval)
    alert_timely = Column(Boolean)
    alert_text = Column(String(300))
    predicted_delay = Column(Interval)
    delay_accuracy = Column(Enum(DelayAccuracy))
