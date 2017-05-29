from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mbtaalerts.config import config as cfg
from mbtaalerts.logging import get_log


LOG = get_log('database')
ENGINE = None


def setup_engine(url):
    global ENGINE
    ENGINE = create_engine(url)
    LOG.info('Creating new db engine: %s', ENGINE)


def reset_engine():
    global ENGINE
    ENGINE = None
    LOG.info('Resetting db engine: %s', ENGINE)


def get_db_session():
    if ENGINE is None:
        setup_engine(cfg.get('Database', 'database_url'))
    session = sessionmaker(autocommit=False,
                           autoflush=False,
                           bind=ENGINE)
    return scoped_session(session)


def init_db():
    from mbtaalerts.database.models import Base
    if ENGINE is None:
        setup_engine(cfg.get('Database', 'database_url'))
    Base.metadata.create_all(bind=ENGINE)
