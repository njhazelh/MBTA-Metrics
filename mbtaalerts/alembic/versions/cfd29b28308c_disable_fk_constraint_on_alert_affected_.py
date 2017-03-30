"""disable fk constraint on alert_affected_services

Revision ID: cfd29b28308c
Revises: f7d3f75da1ad
Create Date: 2017-03-29 16:23:22.286355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd29b28308c'
down_revision = 'f7d3f75da1ad'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('alert_affected_services_alert_id_fkey', 'alert_affected_services', type_='foreignkey')
    op.drop_constraint('alert_effect_period_alert_id_fkey', 'alert_effect_period', type_='foreignkey')


def downgrade():
    op.create_foreign_key(
            "alert_effect_period_alert_id_fkey", "alert_effect_period",
            "alerts", ["alert_id"], ["id"])
    op.create_foreign_key(
            "alert_affected_services_alert_id_fkey", "alert_affected_services",
            "alerts", ["alert_id"], ["id"])
