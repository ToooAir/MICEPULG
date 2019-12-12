#!/usr/bin/python3
import sys
import logging

from os import environ

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/tgif.momoka.tw/")

environ['GOOGLE_APPLICATION_CREDENTIALS']='/var/www/tgif.momoka.tw/boky-chatbot-360b51ab7c2b.json'

from main import app as application

