from __future__ import unicode_literals
import os
import sys
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

from fsm import TocMachine
from utils import send_text_message

import random

load_dotenv()

app = Flask(__name__)

#from ta
machine = TocMachine(
    states=["user", "milkshop","louisa","dandan","mcalories","lcalories","change"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "milkshop",
            "conditions": "is_going_to_milkshop",
        },
        {
            "trigger": "advance",
            "source": "milkshop",
            "dest": "mcalories",
            "conditions": "is_going_to_mcalories",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "louisa",
            "conditions": "is_going_to_louisa",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "dandan",
            "conditions": "is_going_to_dandan",
        },
        {
            "trigger": "advance",
            "source": "louisa",
            "dest": "lcalories",
            "conditions": "is_going_to_lcalories",
        },
        {
            "trigger": "go_back", 
            "source": ["dandan","mcalories","lcalories","change"], 
            "dest": "user",
        },
        {
            "trigger":"advance",
            "source": ["milkshop","louisa"], 
            "dest": "change",
            "conditions": "is_going_to_change",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

machine.get_graph().draw("fsm.png", prog="dot", format="png")

# basic infromation
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers['X-Line-Signature']


    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK" 
    


# repeat
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    
    response = machine.advance(event)
    #response = False
    if response == False:
        s = "Not Entering any State"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="對不起，寫程式的那個人技術太差了，所以我不知道這是什麼意思。輸入迷客夏、路易莎或丹丹就可以知道我推薦給你的特製菜單。")
        )
        #send_text_message(event.reply_token, s)

if __name__ == "__main__":
    app.run(debug = True)
    