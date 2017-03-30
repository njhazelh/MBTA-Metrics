"""populate routes table

Revision ID: f7d3f75da1ad
Revises: a9710c2a76d1
Create Date: 2017-03-29 13:32:20.844322

"""
from alembic import op
import sqlalchemy as sa
from mbtaalerts.database import populate
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


# revision identifiers, used by Alembic.
revision = 'f7d3f75da1ad'
down_revision = 'a9710c2a76d1'
branch_labels = None
depends_on = None

routes_table = table('routes',
    column('id', Integer),
    column('name', String)
)


def upgrade():
    cr_routes = populate.routes()
    values = [{'id': item.get('route_id'), 'name': item.get('route_name')} for item in cr_routes]
    op.bulk_insert(routes_table, values)


def downgrade():
    op.execute("DELETE FROM routes")

