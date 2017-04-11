import os

from sqlalchemy import create_engine, Column, Integer, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from mbtaalerts.config import config as cfg

ENGINE = create_engine(cfg.get('Database', 'database_url'))
DB_SESSION = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=ENGINE))

@as_declarative()
class Base(object):
    query = DB_SESSION.query_property()
    id = Column(Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


def init_db():
    import mbtaalerts.database.models
    Base.metadata.create_all(bind=ENGINE)
