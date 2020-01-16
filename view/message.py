from json import loads as json_load
from time import time

from flask import Blueprint, abort, g, render_template, request
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

from account.models import Comment, Followers, Logs, User, UserDetail
from config import config
from utils.models import set_attribute

message = Blueprint("message", __name__)

# config
line_bot_api = LineBotApi(config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])


def setPicture(profile):
    if profile["picture"] == "":
        return config["default_avater"]
    else:
        return profile["picture"]


@message.before_request
def before_req():
    g.startTime = time()
    g.config = config


# messaging API
@message.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    # message.logger.info("Request body: " + body)

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

    Logs.format(line_user_id=lineUserId, comand=text, create_time=g.startTime)


@handler.add(FollowEvent)
def handleFollow(event):
    lineUserId = event.source.user_id

    Followers.add(line_user_id=lineUserId, create_time=g.startTime)
    Logs.format(line_user_id=lineUserId, comand="follow", create_time=g.startTime)


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

    Logs.format(line_user_id=lineUserId, comand=text, create_time=g.startTime)
