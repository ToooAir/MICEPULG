from datetime import datetime
from json import dumps as json_dumps
from json import loads as json_load
from time import time
from uuid import uuid1

from flask import (
    Flask,
    abort,
    g,
    make_response,
    render_template,
    request,
    send_from_directory,
)
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FlexSendMessage,
    FollowEvent,
    MessageEvent,
    PostbackEvent,
    TextMessage,
    TextSendMessage,
)

import alchemyFunc
from cloudStorage import deleteImage, uploadImage
from config import config

# config
line_bot_api = LineBotApi(config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])


def setPicture(user):
    if user["picture"] == "":
        return config["default_avater"]
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
        return static + "?v=" + g.uuid

    return {"setuuid": setuuid}


# website
@app.route("/", methods=["GET"])
def index():
    page = request.args.get("page")
    if page == "login":
        return render_template("login.html", title="登入")
    elif page == "signup":
        return render_template("signup.html", title="註冊")
    elif page == "edit":
        return render_template("edit.html", title="個人資料")
    elif page == "find":
        return render_template("find.html", title="找人")
    elif page == "comment":
        id = request.args.get("id")
        name = alchemyFunc.find_someone(id)["name"]
        output = alchemyFunc.get_comments(id)
        return render_template("comment.html", name=name, output=output, title="留言")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


# AJAX
@app.route("/bind", methods=["POST"])
def bind():
    bindId = request.form["bindId"]
    lineUserId = request.form["lineUserId"]

    if alchemyFunc.check_nonexist(bindId):
        return "此驗證碼不存在，請確認你的驗證碼或洽詢現場工作人員。"
    elif alchemyFunc.check_repeat(bindId):
        return "此驗證碼已使用過，請確認你的驗證碼或洽詢現場工作人員。"

    alchemyFunc.bind_user(bindId, lineUserId)

    resp = setResponse(request.form)

    line_bot_api.link_rich_menu_to_user(lineUserId, config["richmenu"]["menu"])

    alchemyFunc.add_logs(lineUserId, "bind", "", g.startTime)

    return resp


@app.route("/register", methods=["POST"])
def register():
    lineUserId = request.form["lineUserId"]
    name = request.form["name"]

    imageurl = config["default_avater"]
    if "image" in request.files:
        filename = str(uuid1()) + "." + request.files["image"].filename.split(".")[-1]
        imageurl = uploadImage(request.files["image"], filename)
    else:
        imageurl = config["default_avater"]

    alchemyFunc.add_user(**request.form, picture=imageurl)

    resp = setResponse(name)

    line_bot_api.link_rich_menu_to_user(lineUserId, config["richmenu"]["menu"])
    alchemyFunc.add_logs(lineUserId, "register", "", g.startTime)

    return resp


@app.route("/editprofile", methods=["POST"])
def editprofile():
    lineUserId = request.form["lineUserId"]
    name = request.form["name"]

    filename = alchemyFunc.get_picture(lineUserId)
    imageurl = ""

    if "image" in request.files:
        if filename != config["default_avater"]:
            deleteImage(filename)
        filename = str(uuid1()) + "." + request.files["image"].filename.split(".")[-1]
        imageurl = uploadImage(request.files["image"], filename)
    else:
        imageurl = filename

    alchemyFunc.edit_user(**request.form, picture=imageurl)

    resp = setResponse(name)

    alchemyFunc.add_logs(lineUserId, "edit", "", g.startTime)
    return resp


@app.route("/getprofile", methods=["POST"])
def getprofile():
    lineUserId = request.form["lineUserId"]

    profile = alchemyFunc.get_profile(lineUserId)

    resp = setResponse(profile)

    return resp


@app.route("/addcomment", methods=["POST"])
def addComment():
    lineUserId = request.form["lineUserId"]
    id = request.form["id"].split("#")[0]
    comment = request.form["comment"]
    ts = int(time())

    alchemyFunc.add_comments(lineUserId, id, comment, ts)

    alchemyFunc.add_logs(lineUserId, "addcomment", "", g.startTime)

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
    if text.startswith("#") and text[1:].isdigit():
        try:
            find = text.split("#")[1]

            user = alchemyFunc.find_someone(find)
            picture = setPicture(user)

            flex = json_load(
                render_template(
                    "Find.json",
                    user=user,
                    picture=picture,
                    comment=config["liff"] + "?page=comment",
                ),
                strict=False,
            )
            line_bot_api.reply_message(
                event.reply_token, [FlexSendMessage(alt_text=text, contents=flex)]
            )
            alchemyFunc.add_logs(lineUserId, "find", "", g.startTime)
        except:
            line_bot_api.reply_message(
                event.reply_token, [TextSendMessage(text="查無此人")]
            )

    # Bind
    elif text.startswith("#") and len(text[1:]) == 4:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=f"登入成功，請將您的個人專屬編號寫上號碼牌： #{alchemyFunc.get_user(lineUserId).id}"
                )
            ],
        )

    elif text == "修改成功":
        user = alchemyFunc.get_profile(lineUserId)
        picture = setPicture(user)

        flex = json_load(
            render_template(
                "Me.json",
                user=user,
                picture=picture,
                edit=config["liff"] + "?page=edit",
                comment=config["liff"] + "?page=comment",
            ),
            strict=False,
        )
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage(alt_text=text, contents=flex)
        )

    elif text == "我要註冊":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=f"註冊成功，請將您的個人專屬編號寫上號碼牌： #{alchemyFunc.get_user(lineUserId).id}"
                )
            ],
        )

    elif text == "/reset":
        alchemyFunc.unbind_user(lineUserId)

        line_bot_api.unlink_rich_menu_from_user(lineUserId)
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="已重置")])

        alchemyFunc.add_logs(lineUserId, "reset", "", g.startTime)


@handler.add(FollowEvent)
def handleFollow(event):
    lineUserId = event.source.user_id

    alchemyFunc.add_follow(lineUserId, g.startTime)
    alchemyFunc.add_logs(lineUserId, "follow", "", g.startTime)


@handler.add(PostbackEvent)
def handlePostback(event):
    lineUserId = event.source.user_id
    text = event.postback.data

    if text == "個人資料":

        user = alchemyFunc.get_profile(lineUserId)
        picture = setPicture(user)

        flex = json_load(
            render_template(
                "Me.json",
                user=user,
                picture=picture,
                edit=config["liff"] + "?page=edit",
                comment=config["liff"] + "?page=comment",
            ),
            strict=False,
        )
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage(alt_text=text, contents=flex)
        )

        alchemyFunc.add_logs(lineUserId, text, "", g.startTime)

    elif text == "抽卡":

        user = alchemyFunc.draw_card()
        picture = setPicture(user)

        flex = json_load(
            render_template(
                "Find.json",
                user=user,
                picture=picture,
                comment=config["liff"] + "?page=comment",
            ),
            strict=False,
        )
        line_bot_api.reply_message(
            event.reply_token, [FlexSendMessage(alt_text=text, contents=flex)]
        )

        alchemyFunc.add_logs(lineUserId, text, "", g.startTime)

    elif text == "活動資訊":

        flex = json_load(render_template("Event.json"), strict=False)
        line_bot_api.reply_message(
            event.reply_token, [FlexSendMessage(alt_text=text, contents=flex)]
        )

        alchemyFunc.add_logs(lineUserId, text, "", g.startTime)


if __name__ == "__main__":
    app.run()
