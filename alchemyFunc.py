from datetime import datetime
from random import random
from time import time

from sqlalchemy import desc, null
from sqlalchemy.sql.expression import func

from alchemyModel import Comment, Followers, Logs, Tags, User, UserDetail
from alchemyStart import db_session


def session_commit(func):
    def wrapper(*args, **kwarg):
        func(*args, **kwarg)
        db_session.commit()

    return wrapper


def get_user(line_user_id):
    user = db_session.query(User).filter(User.line_user_id == line_user_id).one()

    return user


def add_user(lineUserId, name, email, job, intro, link, tag1, tag2, tag3, picture):
    User.add(
        line_user_id=lineUserId,
        name=name,
        email=email,
        intro=intro,
        link=link,
        picture=picture,
    )

    user = db_session.query(User).filter(User.line_user_id == lineUserId).first()

    UserDetail.add(
        user_id=user.id, field_a=job, field_b=tag1, field_c=tag2, field_d=tag3
    )


def import_user(
    bindId,
    name,
    id,
    email,
    job,
    intro,
    link,
    tag1,
    tag2,
    tag3,
    picture,
    ticket,
    qrcode=None,
):
    User.add(
        bind_id=bindId,
        name=name,
        id=id,
        email=email,
        intro=intro,
        link=link,
        picture=picture,
        qrcode=qrcode,
    )

    UserDetail.add(user_id=id, field_a=job, field_b=tag1, field_c=tag2, field_d=tag3)

    Tags.add(user_id=id, tag_name="ticket", tag_value=ticket)


# importUser("3A2B","真C折", 16,"karl@lin.com","大Boss","木木卡有限","https://google.com.tw","老闆","沒有頭髮","戴眼鏡","https://storage.googleapis.com/tgif.momoka.tw/avatar/00.jpg","超級大佬","201911041604381349845222")


@session_commit
def edit_user(lineUserId, name, email, job, intro, link, tag1, tag2, tag3, picture):
    id = db_session.query(User).filter(User.line_user_id == lineUserId).first().id

    user = db_session.query(User).filter(User.id == id)
    user.update(
        {"name": name, "email": email, "intro": intro, "link": link, "picture": picture}
    )

    detail = db_session.query(UserDetail).filter(UserDetail.user_id == id)
    detail.update({"field_a": job, "field_b": tag1, "field_c": tag2, "field_d": tag3})


@session_commit
def unbind_user(lineUserId):
    user = db_session.query(User).filter(User.line_user_id == lineUserId).first()

    if user is None:
        return False
    else:
        comments = db_session.query(Comment).filter(Comment.sender == lineUserId).all()

        for comment in comments:
            db_session.delete(comment)

        db_session.commit()

        user.line_user_id = null()

        return True


@session_commit
def bind_user(bindId, lineUserId):
    user = db_session.query(User).filter(User.bind_id == bindId)
    user.update({"line_user_id": lineUserId})


def check_repeat(bindId):
    user = db_session.query(User).filter(User.bind_id == bindId).first()

    if user.line_user_id != None:
        return True
    else:
        return False


def check_nonexist(bindId):
    user = db_session.query(User).filter(User.bind_id == bindId).first()

    if user == None:
        return True
    else:
        return False


def get_profile(lineUserId):
    user = db_session.query(User).filter(User.line_user_id == lineUserId).first()
    detail = db_session.query(UserDetail).filter(UserDetail.user_id == user.id).first()
    profileJson = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "job": detail.field_a,
        "intro": user.intro,
        "link": user.link,
        "picture": user.picture,
        "tag1": detail.field_b,
        "tag2": detail.field_c,
        "tag3": detail.field_d,
        "qrcode": user.qrcode,
    }
    return profileJson


def find_someone(id):
    user = db_session.query(User).filter(User.id == id).first()
    detail = db_session.query(UserDetail).filter(UserDetail.user_id == user.id).first()
    profileJson = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "job": detail.field_a,
        "intro": user.intro,
        "link": user.link,
        "picture": user.picture,
        "tag1": detail.field_b,
        "tag2": detail.field_c,
        "tag3": detail.field_d,
    }
    return profileJson


def get_picture(lineUserId):
    user = db_session.query(User).filter(User.line_user_id == lineUserId).first()
    return str(user.picture)


def get_name(lineUserId):
    user = db_session.query(User).filter(User.line_user_id == lineUserId).first()
    return str(user.name)


def get_comments(user_id):
    comments = (
        db_session.query(Comment)
        .filter(Comment.receiver == user_id)
        .order_by(desc(Comment.create_time))
        .all()
    )
    output = []

    for comment in comments:
        time = datetime.fromtimestamp(comment.create_time).strftime("%Y-%m-%d %H:%M")
        output.append(
            {"name": comment.user.name, "time": time, "content": comment.content}
        )

    return output


def add_comments(sender, receiver, content, ts):
    Comment.add(create_time=ts, sender=sender, receiver=receiver, content=content)


def add_follow(lineUserId, followTs):
    Followers.add(line_user_id=lineUserId, create_time=followTs)


def add_logs(lineUserId, comand, content, callTs):
    spend = round((time() - callTs) * 1000)
    Logs.add(
        line_user_id=lineUserId,
        comand=comand,
        content=content,
        create_time=callTs,
        spend_ms=spend,
    )


def draw_card():
    user = db_session.query(User).order_by(func.rand()).first()
    detail = db_session.query(UserDetail).filter(UserDetail.user_id == user.id).first()
    profileJson = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "job": detail.field_a,
        "intro": user.intro,
        "link": user.link,
        "picture": user.picture,
        "tag1": detail.field_b,
        "tag2": detail.field_c,
        "tag3": detail.field_d,
    }
    return profileJson
