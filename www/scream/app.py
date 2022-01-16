from typing import Pattern
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import FlexSendMessage

from content import start
from content import FSM 
#有限狀態機FSM 用來處理所有的狀態

import configparser

import db

import re
import json
import action

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    user = event.source.user_id
    user_id = db.get_user_id(user)
    reply_all = []

    pattern_move = re.compile('向(.+)移動')
    
    if text.isdigit():
        reply_all.append(TextSendMessage(text= "目前不支援判別數字，請輸入中文唷！"))

    elif text == "restart":
        restart = json.load(open('flex_file/restart.json','r',encoding='utf-8'))
        reply_all.append(FlexSendMessage(alt_text='restart', contents=restart))

    elif text=="restart:Yes":
        #此處初始化玩家位置及State及等級
        db.alter_user_state(user,1)
        db.alter_user_level(user,1)
        db.alter_user_skill(user,1)
        db.alter_hp(user, 3, 20)
        # start = json.load(open('flex_file/restart.json','r',encoding='utf-8'))
        # reply_all.append(FlexSendMessage(alt_text='start', contents=start))
        
        reply_all = start.get_response(user)
        
    
    elif pattern_move.findall(text):
        token = pattern_move.findall(text)
        move = token[0]

        reply_all = action.user_move(event, move)

    #玩家按"玩家指引"後進來這個區域
    elif text == "玩家指引":

        u_id = event.source.user_id
        player_level = db.get_user_level(u_id)
        current_location = db.get_player_location(u_id)
        cool_skills = db.get_user_skill(u_id)
        user_entity = db.find_user(u_id)
        i = db.get_skill_name(cool_skills)
        reply_all.append(TextSendMessage(text= "您目前等級：" + str(player_level) + "\n您目前位置：" + str(current_location) + "\n您目前技能：【" + i + "】" + 
        "\n您目前血量：" + user_entity.player_hp*"❤️" + "\n野豬目前血量：" + user_entity.pig_hp//5*"❤️"))


    elif text == "早安":
        # 隨機產出無意義對話跟玩家聊天
        reply_all.append(TextSendMessage(text= "早安您好！你又虛度一天光陰囉~"))

    elif text == "午安":
        # 隨機產出無意義對話跟玩家聊天
        reply_all.append(TextSendMessage(text= "午安您好！你又虛度一天光陰囉~"))

    elif text == "晚安":
        # 隨機產出無意義對話跟玩家聊天
        reply_all.append(TextSendMessage(text= "晚安您好！你又虛度一天光陰囉~"))

    # elif text.rstrip().upper() == "BERT":
        
    #     reply_all,response_str = FSM.get_text(event,"BERT")
    #     db.insert_questionlog(user_id, response_str)

    elif "BERT" in text.rstrip().upper():
        
        reply_all,response_str = FSM.get_text(event,"BERT")
        db.insert_questionlog(user_id, response_str)

    else:
        #除了固定的回覆之外，都進到FSM處理狀態
        text = action.predict_tag(event)
        reply_all,response_str = FSM.get_text(event,text)
        db.insert_questionlog(user_id, response_str)
    
    # 回覆文字訊息
    line_bot_api.reply_message(event.reply_token, reply_all)


if __name__ == "__main__":
    app.run(debug=True)
