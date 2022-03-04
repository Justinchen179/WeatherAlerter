#!/usr/bin/env python3
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot import (
    LineBotApi, WebhookHandler
)
from flask import Flask, request, abort, render_template, redirect, url_for
import csv
import os

app = Flask(__name__)

project_path = os.path.dirname(os.path.abspath(__file__ + "/../"))
line_bot_api = LineBotApi('<CHENNEL_ACCESS_TOKEN>')
handler = WebhookHandler('<CHANNEL_SECRET>')
cmds = ["t", "today"]


def reply():
    with open(project_path+"/today-line-message.txt", 'rb') as f:
        contents = f.read()
        contents = contents.decode("utf-8")
        lentp = len(contents)
        return contents[:lentp-1]


@app.route("/send_message", methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        publishing_message = request.form.get('msg')
        with open(project_path + '/linebot/line_id.csv', newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                line_bot_api.push_message(row[0], TextSendMessage(text=publishing_message))
        return redirect(url_for('publish'))

    return render_template('index.html')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_id = event.source.user_id
    line_message = str(event.message.text.lower())
    with open(project_path + '/linebot/line_id.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        n = 0
        for row in rows:
            if row[0] == line_id:
                n = n+1
        if n != 1:
            with open(project_path + '/linebot/line_id.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([line_id])

    if os.path.isfile(project_path + '/linehistory/'+event.message.text+" .txt"):
        with open(project_path + '/linehistory/'+event.message.text+" .txt", 'rb') as f:
            contents = f.read()
            contents = contents.decode("utf-8")
            lentp = len(contents)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=contents[0:lentp-2]))

    elif line_message in cmds:
        message = reply()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='noData'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
