from sqlalchemy.ext.declarative import declarative_base

from utils.decorator import session_commit, session_orm

from . import db_session, engine


@session_commit
def set_attribute(*args, **kwargs):
    for key, value in kwargs.items():
        setattr(*args, key, value)


class BaseOrm(object):
    @classmethod
    @session_orm
    def add(cls, **kwargs):
        return db_session.add(cls(**kwargs))

    @classmethod
    @session_orm
    def delete(cls, **kwargs):
        return cls.query.filter_by(**kwargs).delete()

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()


class Base(object):
    query = db_session.query_property()


Base = declarative_base(cls=Base)
