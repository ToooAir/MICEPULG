from alchemyStart import DB_session
from alchemyModel import User


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


# addUser("lol","家豪","家豪的信箱","家豪的自我介紹","家豪的連結","家豪的照片")


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
        "name":user.name,
        "email":user.email,
        "intro":user.intro,
        "link":user.link
    }
    return profileJson
    
def getPicture(lineUserId):
    session = DB_session()
    user = session.query(User).filter(User.line_user_id == lineUserId).first()
    session.close()
    return str(user.picture)
