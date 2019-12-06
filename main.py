import alchemyFunc
from config import config

from time import time
from argparse import ArgumentParser
from os import path as os_path, remove as os_remove
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
imageSaveDir = 'static/uploadImage/'

app = Flask(__name__)


@app.before_request
def before_req():
    g.startTime = time()

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
    return render_template()


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

# Todo 留言板還沒做(HTML，SQL，Function)

# AJAX
@app.route("/bind", methods=["POST"])
def bind():
    data = request.form
    bindId = data["bindId"]
    lineUserId = data["lineUserId"]

    if(alchemyFunc.checkNonExist(bindId)):
        resp = make_response("該序號並不存在")
    elif(alchemyFunc.checkRepeat(bindId)):
        resp = make_response("該序號已被使用")
    else:
        alchemyFunc.bindUser(bindId, lineUserId)
        resp = make_response(json_dumps(data))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"

    line_bot_api.link_rich_menu_to_user(lineUserId, config['richmenu']['main'])

    alchemyFunc.addLogs(lineUserId, "bind", "", g.startTime,
                        request.headers['X-Forwarded-For'])

    return resp


@app.route("/register", methods=["POST"])
def register():
    data = request.form
    lineUserId = data["lineUserId"]
    name = data["name"]
    email = data["email"]
    intro = data["intro"]
    link = data["link"]
    image = request.files["images"]

    if(image.filename != ""):
        filename = str(uuid1()) + "." + image.filename.split(".")[-1]
        image.save(os_path.join(imageSaveDir, filename))
    else:
        filename = "default.jpg"
    alchemyFunc.addUser(lineUserId, name, email, intro, link, filename)

    resp = make_response(json_dumps(data))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"

    line_bot_api.link_rich_menu_to_user(lineUserId, config['richmenu']['main'])
    alchemyFunc.addLogs(lineUserId, "register", "", g.startTime,
                        request.headers['X-Forwarded-For'])

    return resp


@app.route("/editprofile", methods=["POST"])
def editprofile():
    data = request.form
    lineUserId = data["lineUserId"]
    name = data["name"]
    email = data["email"]
    intro = data["intro"]
    link = data["link"]
    image = request.files["images"]

    filename = alchemyFunc.getPicture(lineUserId)
    if(image.filename != ""):
        if(os_path.isfile(imageSaveDir+filename)):
            os_remove(imageSaveDir+filename)
        filename = str(uuid1()) + "." + image.filename.split(".")[-1]
        image.save(os_path.join(imageSaveDir, filename))

    alchemyFunc.editUser(lineUserId, name, email, intro, link, filename)
    resp = make_response(json_dumps(name))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"
    alchemyFunc.addLogs(lineUserId, "edit", "", g.startTime,
                        request.headers['X-Forwarded-For'])
    return resp


@app.route("/getprofile", methods=["POST"])
def getprofile():
    data = request.form
    lineUserId = data["lineUserId"]

    profile = alchemyFunc.getProfile(lineUserId)

    resp = make_response(json_dumps(profile))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"

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

    if((text.index("要") == 1) and (text.index("#") == 3)):
        find = text.split("#")[1].split("號")

        user = alchemyFunc.findSomeone(find)
        picture = config['domain']+imageSaveDir+user["picture"]

        flex = json_load(render_template(
            'Find.json', user=user, picture=picture), strict=False)
        line_bot_api.reply_message(
            event.reply_token, [
                FlexSendMessage(alt_text=text, contents=flex)
            ]
        )

        alchemyFunc.addLogs(lineUserId, "find", "", g.startTime,
                        request.headers['X-Forwarded-For'])

    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=event.message.text+"(VScode)")
            ]
        )


@handler.add(FollowEvent)
def handleFollow(event):
    lineUserId = event.source.user_id
    alchemyFunc.addFollow(lineUserId, g.startTime)
    alchemyFunc.addLogs(lineUserId, "follow", "", g.startTime,
                        request.headers['X-Forwarded-For'])


@handler.add(PostbackEvent)
def handlePostback(event):
    lineUserId = event.source.user_id
    text = event.postback.data

    if(text == "我是誰"):
        user = alchemyFunc.getProfile(lineUserId)
        filename = alchemyFunc.getPicture(lineUserId)
        picture = config['domain']+imageSaveDir+filename

        flex = json_load(render_template(
            'Me.json', user=user, picture=picture), strict=False)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text=text, contents=flex)
        )
        
        alchemyFunc.addLogs(lineUserId, text, "", g.startTime,
                            request.headers['X-Forwarded-For'])


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + "[--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
