from config import config
# import alchemyFunc

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

#config
line_bot_api = LineBotApi(config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['LINE_CHANNEL_SECRET'])
imageSaveDir = 'static/uploadImage/'

app = Flask(__name__)

#website
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
# Todo 留言板還沒做(HTML，SQL，Function)



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage="Usage: python " + __file__ + "[--port <port>] [--help]"
    )
    arg_parser.add_argument("-p", "--port", default=8000, help="port")
    arg_parser.add_argument("-d", "--debug", default=False, help="debug")
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)