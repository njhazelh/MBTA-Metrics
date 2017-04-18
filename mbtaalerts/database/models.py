from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, \
    Date, Time, DateTime, Interval, \
    Boolean, ForeignKey, CheckConstraint, Enum
import enum

from mbtaalerts.database.database import Base


class Direction(enum.Enum):
    inbound = 0
    outbound = 1


class DelayAccuracy(enum.Enum):
    low = 0
    accurate = 1
    high = 2


class Route(Base):
    __tablename__ = 'routes'
    id = Column(String(32), primary_key=True, unique=True)
    name = Column(String(32), nullable=False)
    # alert_affected_services = relationship("AlertAffectedServices",
    #                                        backref="routes",
    #                                        order_by="AlertAffectedServices.id")
    # alert_events = relationship("AlertEvents",
    #                             backref="routes",
    #                             order_by="AlertEvents.id")


class Stop(Base):
    __tablename__ = 'stops'
    id = Column(String(32), primary_key=True, unique=True)
    name = Column(String(32), nullable=False)


class Alert(Base):
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
    # There are issues with these relationships
    # alert_effect_periods = \
    #     relationship("AlertEffectPeriod",
    #                  backref="alerts",
    #                  order_by="AlertEffectPeriod.id")
    # alert_affected_services = \
    #     relationship("AlertAffectedServices",
    #                  backref="alerts",
    #                  order_by="AlertAffectedServices.id")


class AlertEffectPeriod(Base):
    __tablename__ = 'alert_effect_period'
    alert_id = Column(Integer)
    effect_start = Column(DateTime)
    effect_end = Column(DateTime)


class AlertAffectedService(Base):
    __tablename__ = 'alert_affected_services'
    alert_id = Column(Integer)
    route_id = Column(String(32))
    trip_id = Column(String(64))
    trip_name = Column(String(64))


class AlertEvent(Base):
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
    predicted_delay = Column(String(32))
    delay_accuracy = Column(Enum(DelayAccuracy))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'date': None if self.date is None else self.date.isoformat(),
            'time': None if self.time is None else self.time.isoformat(),
            'day': self.day,
            'route': self.route,
            'stop': self.stop,
            'direction': None\
                if self.direction is None\
                else self.direction.name,
            'short_name': self.short_name,
            'scheduled_departure': None \
                if self.scheduled_departure is None \
                else self.scheduled_departure.isoformat(),
            'actual_departure': None \
                if self.actual_departure is None \
                else  self.actual_departure.isoformat(),
            'delay': None\
                if self.delay is None\
                else self.delay.total_seconds() / 60.0,
            'alert_issued': self.alert_issued,
            'deserves_alert': self.deserves_alert,
            'alert_delay': None\
                if self.alert_delay is None\
                else self.alert_delay.total_seconds() / 60.0,
            'alert_timely': self.alert_timely,
            'alert_text': self.alert_text,
            'predicted_delay': self.predicted_delay,
            'delay_accuracy': None\
                if self.delay_accuracy is None\
                else self.delay_accuracy.name
        }
