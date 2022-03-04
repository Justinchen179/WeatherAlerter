#!/usr/bin/env python3
from linebot.models import (TextSendMessage)
from linebot import (LineBotApi, WebhookHandler)
from flask import Flask
import csv
app = Flask(__name__)

project_path = '<PROJECT_PATH>'
line_bot_api = LineBotApi('<CHENNEL_ACCESS_TOKEN>')
handler = WebhookHandler('<CHANNEL_SECRET>')
def reply():
    with open(project_path+"/today-line-message.txt", 'rb') as f:
        contents = f.read()
        contents = contents.decode("utf-8")
        lentp = len(contents)
        return [contents[:lentp-1],contents[lentp-1:]]

with open(project_path+'/linebot/line_id.csv', newline='') as csvfile:
    rows = csv.reader(csvfile)
    message = reply()
    if message[1] != '0':
        for row in rows:
            line_bot_api.push_message(row[0], TextSendMessage(text=message[0]))
