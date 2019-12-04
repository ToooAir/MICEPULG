from config import config
import alchemyFunc

import os
import sys
import re

from argparse import ArgumentParser

from flask import Flask, request, abort, render_template, send_from_directory, make_response
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

# config
line_bot_api = LineBotApi(config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['LINE_CHANNEL_SECRET'])
imageSaveDir = 'static/uploadImage/'

app = Flask(__name__)

# website
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/edit", methods=["GET"])
def edit():
    return render_template()


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
        alchemyFunc.bindUser(bindId,lineUserId)
        resp = make_response(json.dumps(data))
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
    if(re.match("^[0-9]*$", event.message.text)):
        # todo 檢查不存在的號碼 檢查完才查詢
        userid = event.message.text
        # user = alchemyFunc.searchUser(userid)
        # flex = lineModel.flexmessage(user)
        line_bot_api.reply_message(
            event.reply_token, [
                # flex,
            ]
        )
    # elif(event.message.text == "我是誰"):

    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=event.message.text+"(VScode)"),
                TextSendMessage(text="(傳送的非數字無法查詢)")
            ]
        )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + "[--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
