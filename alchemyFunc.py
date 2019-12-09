from alchemyStart import DB_session
from alchemyModel import User, UserDetail, Tags, Comment, Followers, Logs
from sqlalchemy.sql.expression import func
from time import time
from datetime import datetime
from random import random


def addUser(lineUserId, name, email, job, intro, link, tag1, tag2, tag3, picture):
    session = DB_session()
    addUser = User(line_user_id=lineUserId, name=name, email=email,
                   intro=intro, link=link, picture=picture)
    session.add(addUser)
    session.commit()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    id = user.id
    detail = UserDetail(user_id=id, field_a=job,
                        field_b=tag1, field_c=tag2, field_d=tag3)
    session.add(detail)
    session.commit()
    session.close()


def importUser(bindId, name, email, job, intro, link, tag1, tag2, tag3, picture, ticket, qrcode=None):
    session = DB_session()
    addUser = User(bind_id=bindId, name=name, email=email,
                   intro=intro, link=link, picture=picture, qrcode=qrcode)
    session.add(addUser)
    session.commit()
    user = session.query(User).filter(User.bind_id == bindId).first()
    id = user.id
    detail = UserDetail(user_id=id, field_a=job,
                        field_b=tag1, field_c=tag2, field_d=tag3)
    tags = Tags(user_id=id, tag_name="ticket", tag_value=ticket)
    session.add(detail)
    session.add(tags)
    session.commit()
    session.close()

# importUser("5487","真C折","karl@lin.com","大Boss","木木卡有限","https://google.com.tw","老闆","沒有頭髮","戴眼鏡","https://storage.googleapis.com/tgif.momoka.tw/avatar/00.jpg","超級大佬","201911041604381349845222")


def editUser(lineUserId, name, email, job, intro, link, tag1, tag2, tag3, picture):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    user.name = name
    user.email = email
    user.job = job
    user.intro = intro
    user.link = link
    user.picture = picture
    detail = session.query(UserDetail).filter(
        UserDetail.user_id == user.id).first()
    detail.tag1 = tag1
    detail.tag2 = tag2
    detail.tag3 = tag3
    session.commit()
    session.close()
    

def deleteUser(lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    session.delete(user)
    session.commit()
    session.close()


def bindUser(bindId, lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.bind_id == bindId).first()
    user.line_user_id = lineUserId
    session.commit()
    session.close()


def checkRepeat(bindId):
    session = DB_session()
    user = session.query(User).filter(User.bind_id == bindId).first()
    session.close()
    if(user.line_user_id != None):
        return True
    else:
        return False


def checkNonExist(bindId):
    session = DB_session()
    user = session.query(User).filter(User.bind_id == bindId).first()
    session.close()
    if(user == None):
        return True
    else:
        return False


def getProfile(lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    detail = session.query(UserDetail).filter(
        UserDetail.user_id == user.id).first()
    session.close()
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
        "qrcode": user.qrcode
    }
    return profileJson


def findSomeone(id):
    session = DB_session()
    user = session.query(User).filter(User.id == id).first()
    detail = session.query(UserDetail).filter(
        UserDetail.user_id == user.id).first()
    session.close()
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
        "tag3": detail.field_d
    }
    return profileJson


def getPicture(lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    session.close()
    return str(user.picture)


def getName(lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    session.close()
    return str(user.name)


def getComments(id):
    session = DB_session()
    user = session.query(User).filter(User.id == id).first()
    lineUserId = user.line_user_id
    comments = session.query(Comment).filter(
        Comment.receiver == lineUserId).all()
    output = []
    for c in comments:
        time = datetime.fromtimestamp(
            c.create_time).strftime('%Y-%m-%d %H:%M:%S')
        output.append(
            {"name": c.user.name, "time": time, "content": c.content})
        print(c.create_time)
    session.close()
    return output


def addComments(sender, receiver_id, content, ts):
    session = DB_session()
    user = session.query(User).filter(User.id == receiver_id).first()
    receiver = user.line_user_id
    comment = Comment(create_time=ts, sender=sender,
                      receiver=receiver, content=content)
    session.add(comment)
    session.commit()
    session.close()


def addFollow(lineUserId, followTs):
    session = DB_session()
    follow = Followers(line_user_id=lineUserId, create_time=followTs)
    session.add(follow)
    session.commit()
    session.close()


def addLogs(lineUserId, comand, content, callTs, ip):
    session = DB_session()
    spend = round((time() - callTs)*1000)
    log = Logs(line_user_id=lineUserId, comand=comand,
               content=content, create_time=callTs, ip=ip, spend_ms=spend)
    session.add(log)
    session.commit()
    session.close()


def drawCard():
    session = DB_session()
    user = session.query(User).order_by(func.rand()).first()
    detail = session.query(UserDetail).filter(
        UserDetail.user_id == user.id).first()
    session.close()
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
        "tag3": detail.field_d
    }
    return profileJson
