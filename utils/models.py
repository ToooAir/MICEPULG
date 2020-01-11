from sqlalchemy.ext.declarative import declarative_base

from . import db_session, engine


def session_orm(func):
    def wrapper(cls, *args, **kwargs):
        response = func(cls, *args, **kwargs)
        db_session.commit()
        return response

    return wrapper


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
