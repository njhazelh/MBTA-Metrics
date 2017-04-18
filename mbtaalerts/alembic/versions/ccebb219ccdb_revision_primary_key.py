"""revision primary key

Revision ID: ccebb219ccdb
Revises: cfd29b28308c
Create Date: 2017-04-05 16:01:21.066873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence


# revision identifiers, used by Alembic.
revision = 'ccebb219ccdb'
down_revision = 'cfd29b28308c'
branch_labels = None
depends_on = None


def upgrade():
    # move distinct rows to tmp table and rename
    op.drop_constraint('alerts_pkey', 'alerts', type_='primary')
    op.execute("CREATE TABLE alerts_tmp as (SELECT DISTINCT on (\"alert_id\", \"last_modified_dt\") * FROM alerts " +
               "WHERE alert_id IS NOT NULL AND last_modified_dt IS NOT NULL);")
    op.drop_table('alerts')
    op.rename_table('alerts_tmp', 'alerts')

    # recreate autoincrement behavior for id
    op.execute(CreateSequence(Sequence('alerts_id_seq')))
    op.execute("SELECT setval('alerts_id_seq', (SELECT max(id) from alerts) + 1, false);")
    op.alter_column("alerts", "id", nullable=False, server_default=sa.text("nextval('alerts_id_seq'::regclass)"))

    # primary key on alert_id and last_modified_dt
    op.create_primary_key('alerts_pkey', 'alerts', ['alert_id', 'last_modified_dt'])


def downgrade():
    op.drop_constraint('alerts_pkey', 'alerts', type_='primary')
    op.alter_column('alerts', 'alert_id', nullable=True)
    op.alter_column('alerts', 'last_modified_dt', nullable=True)
    # recreate id autoincrement primary key
    op.execute("SELECT setval('alerts_id_seq', (SELECT max(id) from alerts) + 1, false);")
    op.alter_column("alerts", "id", nullable=False, server_default=sa.text("nextval('alerts_id_seq'::regclass)"))
    op.create_primary_key('alerts_pkey', 'alerts', ['id'])
