from json import loads as json_load
from flask import render_template, Flask

from config import config

app = Flask(__name__)


def test1(func):
    def wrapper(*args, **kwargs):
        print("test1 start!")
        func(*args, **kwargs)
        print("test1 end!")

    return wrapper


def test2(func):
    def wrapper(*args, **kwargs):
        print("test2 start!")
        func(*args, **kwargs)
        print("test2 end!")

    return wrapper


@test1
@test2
def test3(name):
    print(name)


# test4 = test3("GG")

flex = json_load(
    render_template(
        "Me.json",
        user="123",
        picture="456",
        edit=config["liff"] + "?page=edit",
        comment=config["liff"] + "?page=comment",
    ),
    strict=False,
)
print(flex)
# line_bot_api.reply_message(
#     event.reply_token, FlexSendMessage(alt_text=text, contents=flex)
# )
