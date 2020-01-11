from time import time

from account.models import Logs

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


def add_logs(**logs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            spend = round((time() - int(logs["create_time"])) * 1000)
            Logs.add(**logs, spend_ms=spend)

        return wrapper

    return decorator
