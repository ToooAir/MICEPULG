from json import dumps as json_dumps
from time import time
from uuid import uuid1

from flask import (
    Blueprint,
    g,
    make_response,
    render_template,
    request,
    send_from_directory,
)

from account.models import Comment, Logs, User, UserDetail
from config import config
from utils.cloudStorage import deleteImage, uploadImage
from utils.models import set_attribute
from view.message import line_bot_api

liff = Blueprint("liff", __name__)


def setResponse(data):
    resp = make_response(json_dumps(data))
    resp.status_code = 200
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@liff.before_request
def before_req():
    g.startTime = time()
    g.uuid = str(uuid1())
    g.config = config


@liff.context_processor
def utility_processor():
    def setuuid(static):
        return static + "?v=" + g.uuid

    return {"setuuid": setuuid}


# website
@liff.route("/", methods=["GET"])
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
    elif page == "liff":
        return render_template("liff.html", title="liff login")


@liff.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


# AJAX
@liff.route("/bind", methods=["POST"])
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

    Logs.format(line_user_id=lineUserId, comand="bind", create_time=g.startTime)

    return resp


@liff.route("/register", methods=["POST"])
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
    Logs.format(line_user_id=lineUserId, comand="register", create_time=g.startTime)

    return resp


@liff.route("/editprofile", methods=["POST"])
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

    Logs.format(line_user_id=lineUserId, comand="edit", create_time=g.startTime)
    return resp


@liff.route("/getprofile", methods=["POST"])
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


@liff.route("/addcomment", methods=["POST"])
def addComment():
    lineUserId = request.form["lineUserId"]
    id = request.form["id"].split("#")[0]
    comment = request.form["comment"]
    ts = int(time())

    Comment.add(create_time=ts, sender=lineUserId, receiver=id, content=comment)

    Logs.format(line_user_id=lineUserId, comand="addcomment", create_time=g.startTime)

    resp = setResponse(id)

    return resp
