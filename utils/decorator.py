
from . import db_session


def session_commit(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        db_session.commit()

    return wrapper


def session_orm(func):
    def wrapper(cls, *args, **kwargs):
        response = func(cls, *args, **kwargs)
        db_session.commit()
        return response

    return wrapper
