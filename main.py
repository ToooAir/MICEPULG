import alchemyFunc
from cloudStorage import uploadImage, deleteImage
from config import config

from time import time
from datetime import datetime
from json import loads as json_load, dumps as json_dumps

from uuid import uuid1

from flask import Flask, request, abort, render_template, send_from_directory, make_response, g

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent, TextMessage, TextSendMessage, FlexSendMessage
)

# config
line_bot_api = LineBotApi(config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['LINE_CHANNEL_SECRET'])

def setPicture(user):
    if user['picture'] == "":
        return config['default_avater']
    else:
        return user["picture"]

def setResponse(data):
    resp = make_response(json_dumps(data))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"
    
    return resp

app = Flask(__name__)


@app.before_request
def before_req():
    g.startTime = time()
    g.uuid = str(uuid1())
    g.config = config

@app.context_processor
def utility_processor():
    def setuuid(static):
        return static+"?v="+g.uuid
    
    return {'setuuid': setuuid}

# website
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/edit", methods=["GET"])
def edit():
    return render_template("edit.html")


@app.route("/find", methods=["GET"])
def find():
    return render_template("find.html")


@app.route("/comment", methods=["GET"])
def comment():
    id = request.args.get('id')
    name = alchemyFunc.findSomeone(id)["name"]
    output = alchemyFunc.getComments(id)
    return render_template("comment.html", name=name, output=output)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

# AJAX
@app.route("/bind", methods=["POST"])
def bind():
    data = request.form
    bindId = data["bindId"]
    lineUserId = data["lineUserId"]

    if(alchemyFunc.checkNonExist(bindId)):
        return "此驗證碼不存在，請確認你的驗證碼或洽詢現場工作人員。"
    elif(alchemyFunc.checkRepeat(bindId)):
        return "此驗證碼已使用過，請確認你的驗證碼或洽詢現場工作人員。"
    
    alchemyFunc.bindUser(bindId, lineUserId)

    resp = setResponse(data)

    line_bot_api.link_rich_menu_to_user(lineUserId, config['richmenu']['menu'])

    alchemyFunc.addLogs(lineUserId, "bind", "", g.startTime)

    return resp


@app.route("/register", methods=["POST"])
def register():
    data = request.form
    lineUserId = data["lineUserId"]
    name = data["name"]
    email = data["email"]
    job = data["job"]
    intro = data["intro"]
    link = data["link"]
    tag1 = data["tag1"]
    tag2 = data["tag2"]
    tag3 = data["tag3"]

    imageurl = ""
    if "image" in request.files:
        filename = str(uuid1()) + "." + request.files["image"].filename.split(".")[-1]
        imageurl = uploadImage(request.files["image"],filename)
    else:
        imageurl = config['default_avater']

    alchemyFunc.addUser(lineUserId,name,email,job,intro,link,tag1,tag2,tag3,imageurl)

    resp = setResponse(name)

    line_bot_api.link_rich_menu_to_user(lineUserId, config['richmenu']['menu'])
    alchemyFunc.addLogs(lineUserId, "register", "", g.startTime)

    return resp


@app.route("/editprofile", methods=["POST"])
def editprofile():
    data = request.form
    lineUserId = data["lineUserId"]
    name = data["name"]
    email = data["email"]
    job = data["job"]
    intro = data["intro"]
    link = data["link"]
    tag1 = data["tag1"]
    tag2 = data["tag2"]
    tag3 = data["tag3"]

    filename = alchemyFunc.getPicture(lineUserId)
    imageurl = ""
    
    if "image" in request.files:
        if filename != config['default_avater']:
            deleteImage(filename)
        filename = str(uuid1()) + "." + request.files["image"].filename.split(".")[-1]
        imageurl = uploadImage(request.files["image"],filename)
    else:
        imageurl = filename

    alchemyFunc.editUser(lineUserId,name,email,job,intro,link,tag1,tag2,tag3,imageurl)
    
    resp = setResponse(name)

    alchemyFunc.addLogs(lineUserId, "edit", "", g.startTime)
    return resp


@app.route("/getprofile", methods=["POST"])
def getprofile():
    data = request.form
    lineUserId = data["lineUserId"]

    profile = alchemyFunc.getProfile(lineUserId)

    resp = setResponse(profile)

    return resp


@app.route("/addcomment", methods=["POST"])
def addComment():
    data = request.form
    lineUserId = data["lineUserId"]
    id = data["id"].split("#")[0]
    comment = data["comment"]
    ts = int(time())

    alchemyFunc.addComments(lineUserId, id, comment, ts)

    name = alchemyFunc.getName(lineUserId)
    sendTime = datetime.fromtimestamp(
        ts).strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "name": name,
        "time": sendTime
    }

    alchemyFunc.addLogs(lineUserId, "addcomment", "", g.startTime)

    resp = setResponse(id)

    return resp


# messaging API
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    lineUserId = event.source.user_id
    text = event.message.text

    # Find
    if(text.startswith("#") and text[1:].isdigit()):
        try:
            find = text.split("#")[1]

            user = alchemyFunc.findSomeone(find)       
            picture = setPicture(user)

            flex = json_load(render_template(
                'Find.json', user=user, picture=picture, comment=config['liff']['comment']), strict=False)
            line_bot_api.reply_message(
                event.reply_token, [
                    FlexSendMessage(alt_text=text, contents=flex)
                ]
            )
            alchemyFunc.addLogs(lineUserId, "find", "", g.startTime)
        except:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text="查無此人")
                ]
            )

    # Bind
    elif(text.startswith("#") and len(text[1:]) == 4):
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text="登入成功，請將您的個人專屬編號寫上號碼牌： #{}".format(alchemyFunc.getUser(lineUserId).id))
                ]
            )

    elif(text == "修改成功"):
        user = alchemyFunc.getProfile(lineUserId)
        picture = setPicture(user)

        flex = json_load(render_template(
            'Me.json', user=user, picture=picture, edit=config['liff']['edit'], comment=config['liff']['comment']), strict=False)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text=text, contents=flex)
        )

    elif(text == "我要註冊"):
        line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text="註冊成功，請將您的個人專屬編號寫上號碼牌： #{}".format(alchemyFunc.getUser(lineUserId).id))
                ]
            )


    elif(text == "/reset"):
        alchemyFunc.unbindUser(lineUserId)

        line_bot_api.unlink_rich_menu_from_user(lineUserId)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="已重置")
            ]
        )

        alchemyFunc.addLogs(lineUserId, "reset", "", g.startTime)

@handler.add(FollowEvent)
def handleFollow(event):
    lineUserId = event.source.user_id
    
    alchemyFunc.addFollow(lineUserId, g.startTime)
    alchemyFunc.addLogs(lineUserId, "follow", "", g.startTime)


@handler.add(PostbackEvent)
def handlePostback(event):
    lineUserId = event.source.user_id
    text = event.postback.data

    if(text == "個人資料"):

        user = alchemyFunc.getProfile(lineUserId)
        picture = setPicture(user)

        flex = json_load(render_template(
            'Me.json', user=user, picture=picture, edit=config['liff']['edit'], comment=config['liff']['comment']), strict=False)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text=text, contents=flex)
        )

        alchemyFunc.addLogs(lineUserId, text, "", g.startTime)

    elif(text == "抽卡"):

        user = alchemyFunc.drawCard()
        picture = setPicture(user)

        flex = json_load(render_template(
            'Find.json', user=user, picture=picture, comment=config['liff']['comment']), strict=False)
        line_bot_api.reply_message(
            event.reply_token, [
                FlexSendMessage(alt_text=text, contents=flex)
            ]
        )

        alchemyFunc.addLogs(lineUserId, text, "", g.startTime)

    elif(text == "活動資訊"):

        flex = json_load(render_template(
            'Event.json'), strict=False)
        line_bot_api.reply_message(
            event.reply_token, [
                FlexSendMessage(alt_text=text, contents=flex)
            ]
        )

        alchemyFunc.addLogs(lineUserId, text, "", g.startTime)

if __name__ == "__main__":
    app.run()
