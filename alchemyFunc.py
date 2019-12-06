from alchemyStart import DB_session
from alchemyModel import User, Followers, Logs, Comment
from time import time


def addUser(lineUserId, name, email, intro, link, picture):
    session = DB_session()
    user = User(line_user_id=lineUserId, name=name, email=email,
                intro=intro, link=link, picture=picture)
    session.add(user)
    session.commit()
    session.close()


def editUser(lineUserId, name, email, intro, link, picture):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    user.name = name
    user.email = email
    user.intro = intro
    user.link = link
    user.picture = picture
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
    session.close()
    profileJson = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "intro": user.intro,
        "link": user.link
    }
    return profileJson


def findSomeone(id):
    session = DB_session()
    user = session.query(User).filter(User.id == id).first()
    session.close()
    profileJson = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "intro": user.intro,
        "link": user.link,
        "picture": user.picture
    }
    return profileJson


def getPicture(lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    session.close()
    return str(user.picture)


def getComments(lineUserId):
    session = DB_session()
    comment = session.query(Comment).filter(Comment.receiver == lineUserId).all()
    for c in comment :
        print(c.sender,c.content,c.user.name)
    session.close()

getComments("lol")


def addComments(sender, receiver, content):
    session = DB_session()
    ts = time()
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
