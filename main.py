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

# import alchemyFunc
from utils.decorator import add_logs, session_commit
from utils.cloudStorage import deleteImage, uploadImage
from account.models import User, UserDetail, Comment, Followers, Logs
from config import config

# config
line_bot_api = LineBotApi(config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])


def setPicture(profile):
    if profile["picture"] == "":
        return config["default_avater"]
    else:
        return profile["picture"]


def setResponse(data):
    resp = make_response(json_dumps(data))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@session_commit
def set_attribute(*args, **kwargs):
    for key, value in kwargs.items():
        setattr(*args, key, value)


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
        name = User.get(id=id).name
        output = Comment.get_dict_order_by_time(receiver=id)
        return render_template("comment.html", name=name, output=output, title="留言")


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


# AJAX
@app.route("/bind", methods=["POST"])
def bind():
    bindId = request.form["bindId"]
    lineUserId = request.form["lineUserId"]

    user = User.get(bind_id=bindId)

    if user == None:
        return "此驗證碼不存在，請確認你的驗證碼或洽詢現場工作人員。"
    elif user.line_user_id != None:
        return "此驗證碼已使用過，請確認你的驗證碼或洽詢現場工作人員。"

    set_attribute(user, line_user_id=lineUserId)

    resp = setResponse(request.form)

    line_bot_api.link_rich_menu_to_user(lineUserId, config["richmenu"]["menu"])

    Logs.format(line_user_id=lineUserId,comand="bind",create_time=g.startTime)

    return resp


@app.route("/register", methods=["POST"])
def register():
    form = request.form
    lineUserId = request.form["lineUserId"]
    name = request.form["name"]

    imageurl = config["default_avater"]
    if "image" in request.files:
        filename = str(uuid1()) + "." + request.files["image"].filename.split(".")[-1]
        imageurl = uploadImage(request.files["image"], filename)
    else:
        imageurl = config["default_avater"]

    User.add(
        line_user_id=form["lineUserId"],
        name=form["name"],
        email=form["email"],
        intro=form["intro"],
        link=form["link"],
        picture=imageurl,
    )
    UserDetail.add(
        user_id=User.get(line_user_id=lineUserId).id,
        field_a=form["job"],
        field_b=form["tag1"],
        field_c=form["tag2"],
        field_d=form["tag3"],
    )

    resp = setResponse(name)

    line_bot_api.link_rich_menu_to_user(lineUserId, config["richmenu"]["menu"])
    Logs.format(line_user_id=lineUserId,comand="register",create_time=g.startTime)

    return resp


@app.route("/editprofile", methods=["POST"])
def editprofile():
    form = request.form
    lineUserId = request.form["lineUserId"]
    name = request.form["name"]

    filename = str(User.get(line_user_id=lineUserId).picture)
    imageurl = ""

    if "image" in request.files:
        if filename != config["default_avater"]:
            deleteImage(filename)
        filename = str(uuid1()) + "." + request.files["image"].filename.split(".")[-1]
        imageurl = uploadImage(request.files["image"], filename)
    else:
        imageurl = filename

    user = User.get(line_user_id=lineUserId)
    set_attribute(
        user,
        name=form["name"],
        email=form["email"],
        intro=form["intro"],
        link=form["link"],
        picture=imageurl,
    )
    set_attribute(
        UserDetail.get(user_id=user.id),
        field_a=form["job"],
        field_b=form["tag1"],
        field_c=form["tag2"],
        field_d=form["tag3"],
    )

    resp = setResponse(name)

    Logs.format(line_user_id=lineUserId,comand="edit",create_time=g.startTime)
    return resp


@app.route("/getprofile", methods=["POST"])
def getprofile():
    lineUserId = request.form["lineUserId"]
    user = User.get(line_user_id=lineUserId)
    detail = UserDetail.get(user_id=user.id)

    profile = {
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

    resp = setResponse(profile)

    return resp


@app.route("/addcomment", methods=["POST"])
def addComment():
    lineUserId = request.form["lineUserId"]
    id = request.form["id"].split("#")[0]
    comment = request.form["comment"]
    ts = int(time())

    Comment.add(create_time=ts, sender=lineUserId, receiver=id, content=comment)

    Logs.format(line_user_id=lineUserId,comand="addcomment",create_time=g.startTime)

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
            id = text.split("#")[1]

            user = User.get(id=id)
            detail = UserDetail.get(user_id=user.id)

            profile = {
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

            picture = setPicture(profile)

            flex = json_load(
                render_template(
                    "Find.json",
                    user=profile,
                    picture=picture,
                    comment=config["liff"] + "?page=comment",
                ),
                strict=False,
            )
            line_bot_api.reply_message(
                event.reply_token, [FlexSendMessage(alt_text=text, contents=flex)]
            )
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
                    text=f"登入成功，請將您的個人專屬編號寫上號碼牌： #{User.get(line_user_id=lineUserId).id}"
                )
            ],
        )

    elif text == "修改成功":
        user = User.get(line_user_id=lineUserId)
        detail = UserDetail.get(user_id=user.id)

        profile = {
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
        picture = setPicture(profile)

        flex = json_load(
            render_template(
                "Me.json",
                user=profile,
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
                    text=f"註冊成功，請將您的個人專屬編號寫上號碼牌： #{User.get(line_user_id=lineUserId).id}"
                )
            ],
        )

    elif text == "/reset":
        user = User.get(line_user_id=lineUserId)

        if user != None:
            Comment.delete(sender=lineUserId)
            set_attribute(user, line_user_id=None)
            line_bot_api.unlink_rich_menu_from_user(lineUserId)
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text="已重置")])

    Logs.format(line_user_id=lineUserId,comand=text,create_time=g.startTime)


@handler.add(FollowEvent)
def handleFollow(event):
    lineUserId = event.source.user_id

    Followers.add(line_user_id=lineUserId, create_time=g.startTime)
    Logs.format(line_user_id=lineUserId,comand="follow",create_time=g.startTime)
    


@handler.add(PostbackEvent)
def handlePostback(event):
    lineUserId = event.source.user_id
    text = event.postback.data

    if text == "個人資料":

        user = User.get(line_user_id=lineUserId)
        detail = UserDetail.get(user_id=user.id)

        profile = {
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
        picture = setPicture(profile)

        flex = json_load(
            render_template(
                "Me.json",
                user=profile,
                picture=picture,
                edit=config["liff"] + "?page=edit",
                comment=config["liff"] + "?page=comment",
            ),
            strict=False,
        )
        line_bot_api.reply_message(
            event.reply_token, FlexSendMessage(alt_text=text, contents=flex)
        )

    elif text == "抽卡":

        user = User.rand()
        detail = UserDetail.get(user_id=user.id)

        profile = {
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

        picture = setPicture(profile)

        flex = json_load(
            render_template(
                "Find.json",
                user=profile,
                picture=picture,
                comment=config["liff"] + "?page=comment",
            ),
            strict=False,
        )
        line_bot_api.reply_message(
            event.reply_token, [FlexSendMessage(alt_text=text, contents=flex)]
        )

    elif text == "活動資訊":

        flex = json_load(render_template("Event.json"), strict=False)
        line_bot_api.reply_message(
            event.reply_token, [FlexSendMessage(alt_text=text, contents=flex)]
        )

    Logs.format(line_user_id=lineUserId,comand=text,create_time=g.startTime)


if __name__ == "__main__":
    app.run()
