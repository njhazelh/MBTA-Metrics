"""predicted delay and day to string

Revision ID: 6771d5f0054d
Revises: ccebb219ccdb
Create Date: 2017-04-16 23:21:14.129317

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision = '6771d5f0054d'
down_revision = 'ccebb219ccdb'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("alert_events_day_check", "alert_events")
    op.execute("CREATE TYPE day AS ENUM('Sunday', 'Monday', 'Tuesday', "
               "'Wednesday', 'Thursday', 'Friday', 'Saturday');")
    op.execute("ALTER TABLE alert_events ALTER COLUMN day TYPE day USING ( "
               "CASE day::integer "
               "WHEN 0 then 'Sunday' "
               "WHEN 1 then 'Monday' "
               "WHEN 2 then 'Tuesday' "
               "WHEN 3 then 'Wednesday' "
               "WHEN 4 then 'Thursday' "
               "WHEN 5 then 'Friday' "
               "WHEN 6 then 'Saturday' "
               "ELSE null "
               "END)::day")
    op.execute("ALTER TABLE alert_events ALTER COLUMN predicted_delay TYPE varchar(32);")


def downgrade():
    op.execute("UPDATE alert_events SET predicted_delay = null;")
    op.execute("ALTER TABLE alert_events ALTER COLUMN predicted_delay TYPE integer "
               "USING predicted_delay::integer;")
    op.execute("ALTER TABLE alert_events ALTER COLUMN day TYPE integer USING ( "
               "CASE day::day "
               "WHEN 'Sunday' then '0' "
               "WHEN 'Monday' then '1' "
               "WHEN 'Tuesday' then '2' "
               "WHEN 'Wednesday' then '3' "
               "WHEN 'Thursday' then '4' "
               "WHEN 'Friday' then '5' "
               "WHEN 'Saturday' then '6' "
               "ELSE null "
               "END)::integer")
    op.create_check_constraint(
    "alert_events_day_check", "alert_events", 'day >= 0 AND day <= 6')
    ENUM(name="day").drop(op.get_bind(), checkfirst=False)


