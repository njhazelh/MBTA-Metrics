"""Create tables

Revision ID: 8d5948f78300
Revises: 
Create Date: 2017-03-29 01:54:49.414020

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ENUM

# revision identifiers, used by Alembic.
revision = '8d5948f78300'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    direction_enum = ENUM('inbound', 'outbound', name='direction', create_type=False)
    direction_enum.create(op.get_bind(), checkfirst=False)
    delay_accuracy_enum = ENUM('low', 'accurate', 'high', name='delayaccuracy', create_type=False)
    delay_accuracy_enum.create(op.get_bind(), checkfirst=False)

    op.create_table('test',
                    sa.Column('id', sa.INTEGER(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='test_pkey')
                    )
    op.create_table('routes',
                    sa.Column('id', sa.VARCHAR(length=32), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='routes_pkey')
                    )
    op.create_table('stops',
                    sa.Column('id', sa.VARCHAR(length=32), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=32), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='stops_pkey')
                    )
    op.create_table('alerts',
                    sa.Column('alert_id', sa.INTEGER(), unique=True, nullable=False),
                    sa.Column('effect_name', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
                    sa.Column('effect', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
                    sa.Column('cause', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
                    sa.Column('header_text', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
                    sa.Column('short_header_text', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
                    sa.Column('severity', sa.VARCHAR(length=16), autoincrement=False, nullable=True),
                    sa.Column('created_dt', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('last_modified_dt', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('service_effect_text', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
                    sa.Column('alert_lifecycle', sa.VARCHAR(length=16), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('alert_id', name='alerts_pkey')
                    )
    op.create_table('alert_effect_period',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('alert_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('effect_start', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('effect_end', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['alert_id'], ['alerts.alert_id'],
                                            name='alert_effect_period_alert_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='alert_effect_period_pkey')
                    )
    op.create_table('alert_affected_services',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('alert_id', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('route_id', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
                    sa.Column('trip_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
                    sa.Column('trip_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], name='alert_affected_services_route_id_fkey'),
                    sa.ForeignKeyConstraint(['alert_id'], ['alerts.alert_id'],
                                            name='alert_affected_services_alert_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='alert_affected_services_pkey')
                    )
    op.create_table('alert_events',
                    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
                    sa.Column('trip_id', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
                    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
                    sa.Column('time', sa.TIME(), autoincrement=False, nullable=True),
                    sa.Column('day', sa.INTEGER(), autoincrement=False, nullable=True),
                    sa.Column('route', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
                    sa.Column('stop', sa.VARCHAR(length=32), autoincrement=False, nullable=True),
                    sa.Column('direction', direction_enum, nullable=False),
                    sa.Column('short_name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
                    sa.Column('scheduled_departure', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('actual_departure', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
                    sa.Column('delay', sa.Interval(), autoincrement=False, nullable=True),
                    sa.Column('alert_issued', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('deserves_alert', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('alert_delay', sa.Interval(), autoincrement=False, nullable=True),
                    sa.Column('alert_timely', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('alert_text', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
                    sa.Column('predicted_delay', sa.Interval(), autoincrement=False, nullable=True),
                    sa.Column('delay_accuracy', delay_accuracy_enum, nullable=True),
                    sa.CheckConstraint('day >= 0 AND day <= 6', name='alert_events_day_check'),
                    sa.ForeignKeyConstraint(['route'], ['routes.id'], name='alert_events_routes_fkey'),
                    sa.PrimaryKeyConstraint('id', name='alert_events_pkey')
                    )


def downgrade():
    op.drop_constraint('alert_affected_services_alert_id_fkey', 'alert_affected_services', type_='foreignkey')
    op.drop_constraint('alert_affected_services_route_id_fkey', 'alert_affected_services', type_='foreignkey')
    op.drop_constraint('alert_effect_period_alert_id_fkey', 'alert_effect_period', type_='foreignkey')
    op.drop_constraint('alert_events_routes_fkey', 'alert_events', type_='foreignkey')
    op.drop_constraint('alert_events_day_check', 'alert_events', type_='check')

    op.drop_table('alert_events')
    op.drop_table('alert_affected_services')
    op.drop_table('alert_effect_period')
    op.drop_table('alerts')
    op.drop_table('stops')
    op.drop_table('routes')
    op.drop_table('test')

    ENUM(name="delayaccuracy").drop(op.get_bind(), checkfirst=False)
    ENUM(name="direction").drop(op.get_bind(), checkfirst=False)
