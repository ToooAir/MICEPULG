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

#config
line_bot_api = LineBotApi(config['LINE_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['LINE_CHANNEL_SECRET'])
imageSaveDir = 'static/uploadImage/'

