from random import random
from linebot.models import TextSendMessage, FlexSendMessage
from content import icon_map
from bs4 import BeautifulSoup
import numpy as np
import db
import json
import action
import requests


#需要改成DATABASE的模式
nomeaning = [
    
    "莎士比亞說一千個人眼中有一千個哈姆雷特，你怎麼看？",
    "聽說最近物價飛漲，也許該找新的打工了......",
    "晨間快報：「知名YouTuber Travis陳明心竟然早上9點準時到校上課，此舉驚呆了教室所有人......」",
    "莎士比亞也愛喝沙士嗎，我常常在想這個問題......",
    "授人以魚不如授人以漁，教孩子寫程式不如讓他成為富二代......",
    "我聽說咖啡是一種豆漿、茶葉是一種蔬菜湯，也許他們才是對的！",
    "趕緊訂閱YouTuber【Travis陳明心】並按讚，快快快！"
    
    ]

doing = [

    "親愛的玩家您好，遇到困難了嗎？利用移動選單到處走走吧~",
    "你知道選單當中有「玩家指引」嗎？快去試試看吧！",
    "黑色的格子代表著您還沒有探索過的區域，試著往黑色區域前進吧！",
    "眼角餘光似乎發現房間角落有一道微弱的光芒，也許那邊有線索..."
]

running_text = [

    "逃的了一時逃不了一世，腳踏實地面對眼前的困境吧！",
    "您的處境猶如「甕中捉鱉」，你無法逃離這個房間(小雞持續尖叫...)",
    "俗話說「泥菩薩過江，自身難保！」，您還是趕緊找找方法逃離這裡吧...",
    "你現在沒有辦法離開這裡，就像哈姆雷特說： 「一隻雀子的死生，都是命運預先註定的」"
]




#初步分類text
def get_text(event, text):
    u_id = event.source.user_id
    player_level = db.get_user_level(u_id)
    current_state = db.get_user_state(u_id)
    current_location = db.get_player_location(u_id)

    if text == "聊天" :
        # 隨機產出無意義對話跟玩家聊天
        return talk_nomeaning()
    
    elif text == "可以幹嘛" :
        # 隨機產出無意義對話跟玩家聊天
        # return help_doing()
        responses = list()
        response_str = "為了\"逃離這個房間\"您可以執行以下行動：\n1. 使用\"移動選單\"探索房間\n2. 使用\"文字輸入\"進行互動\n3. 選單中的\"玩家指引\"可以\n" + " 　確認您目前的狀態喔"
        responses.append(TextSendMessage(text = response_str))
        return responses, response_str

    elif text == "逃走" :
        # 隨機產出無意義對話跟玩家聊天
        return running()

    elif text == "自殺" :
        responses = list()
        response_str = "※ 自殺，不能解決難題\n※ 求助，才是最好的路\n※ 求救請打1995 ( 要救救我 )！"
        responses.append(TextSendMessage(text = response_str))
        return responses, response_str

    elif text == "莎士比亞" :
        return get_shakespeare()

    else:
        if(current_state==1):   return state_01(text, u_id, player_level, current_state, current_location)
        elif(current_state==2):   return state_02(text, u_id, player_level, current_state, current_location)
        elif(current_state==3):   return state_03(text, u_id, player_level, current_state, current_location)
        elif(current_state==4):   return state_04(text, u_id, player_level, current_state, current_location)
        elif(current_state==5):   return state_05(text, u_id, player_level, current_state, current_location)

        else:
            responses = list()
            response_str = "暫時無法分類您的輸入唷！"
            responses.append(TextSendMessage(text = response_str))
            return responses,response_str


def running():
    i = np.random.randint(low=0,high=4,size=1)
    responses = list()
    response_str = running_text[i[0]]
    responses.append(TextSendMessage(text = response_str))
    return responses,response_str


def help_doing():
    i = np.random.randint(low=0,high=4,size=1)
    responses = list()
    response_str = doing[i[0]]
    return response_str

def get_shakespeare():
    random = np.random.randint(low=2,high=80,size=1)
    r = requests.get("https://arielhsu.tw/shakespeare-words/")
    soup = BeautifulSoup(r.text, "html.parser")
    sel = soup.select('.desc p span')
    ans = []

    for i in sel:
        saying = i.text
        ans.append(saying)
    
    responses = list()
    response_str = "你似乎提到了莎士比亞，\n這是在網路上找到的名言：\n" + ans[random[0]]
    responses.append(TextSendMessage(text = response_str))
    return responses,response_str


# 回覆聊天的function
def talk_nomeaning():
    i = np.random.randint(low=0,high=7,size=1)
    responses = list()
    response_str = nomeaning[i[0]]
    responses.append(TextSendMessage(text = response_str))
    return responses,response_str

# 產生隨機技能的function
def random_skill(u_id):
    i = np.random.randint(low=1,high=21,size=1)
    ii = db.get_skill_name(int(i[0]))
    
    responses = list()
    responses.append(TextSendMessage(text="學會了新招式【"+ ii + "】")) 
    #把隨機產生的ID塞入database
    db.alter_user_skill(u_id, int(i[0]))
    return responses

# state_01 玩家初始位置，只有移動到指定位置可以到下一關state_02
def state_01(text, u_id, player_level, current_state, current_location):
    
    responses = list()
    #responses.append(TextSendMessage(text="這是state_01的歡迎訊息！"))
    #responses.append(TextSendMessage(text = "你與身旁的尖叫小雞距離很近！"))

    if text == "吃雞":
        map_str = db.get_user_location(u_id)
        if "P" not in map_str:  
            ending = json.load(open('flex_file/ending.json','r',encoding='utf-8'))
            response_str = "贏了"
            responses.append(FlexSendMessage(alt_text='ending', contents=ending))
            restart = json.load(open('flex_file/restart.json','r',encoding='utf-8'))
            responses.append(FlexSendMessage(alt_text='restart', contents=restart))
            return responses,response_str
        else:
            response_str = "兇猛的野豬使你不敢靠近，您現在不可以吃小雞(小雞持續尖叫中)！"
            
    elif text == "殺雞":
        map_str = db.get_user_location(u_id)
        if "P" not in map_str:
            ending = json.load(open('flex_file/ending.json','r',encoding='utf-8'))
            response_str = "贏了"
            responses.append(FlexSendMessage(alt_text='ending', contents=ending))
            restart = json.load(open('flex_file/restart.json','r',encoding='utf-8'))
            responses.append(FlexSendMessage(alt_text='restart', contents=restart))
            return responses,response_str
        else:
            response_str = "兇猛的野豬使你不敢靠近，您現在不可以攻擊小雞(小雞持續尖叫中)！"

    elif text == "殺野豬":
        
        attack = json.load(open('flex_file/attack.json','r',encoding='utf-8'))
        responses.append(FlexSendMessage(alt_text='attack', contents=attack))
        response_str = action.attack(u_id)
        # state_05(text, u_id, player_level, current_state, current_location)
        # 攻擊力 = player_level * randint(1,6)
        # return = 文字
        user_entity = db.find_user(u_id)

        if(user_entity.pig_hp <= 0):
                response_str = "恭喜你打敗了野豬！"
                responses.append(action.killed_pig(u_id))
                state_05(text, u_id, player_level, current_state, current_location)
        else:
            if(user_entity.player_hp <= 0):
                response_str = "你死了！"
                responses.append(TextSendMessage(text = response_str)) 
                restart = json.load(open('flex_file/restart.json','r',encoding='utf-8'))
                responses.append(FlexSendMessage(alt_text='restart', contents=restart))
                return responses,response_str

    elif text == "小雞餵豬" :
        responses = list()
        response_str = "小雞持續尖叫中，您不可以把小雞餵給豬吃！(也許可以從野豬下手...)"
        responses.append(TextSendMessage(text = response_str))
        return responses, response_str

    elif text == "無意義":
        response_str = help_doing()
    else:
        # response_str = "出事囉，快Debug!!!!!!
        response_str = "不好意思，我無法理解您的意思～請重新輸入！"
        
    responses.append(TextSendMessage(text = response_str)) 
    return responses,response_str

# 此state_02為探索畫框專用
def state_02(text, u_id, player_level, current_state, current_location):
    
    responses = list()
    # responses.append(TextSendMessage(text="這是state_02的歡迎訊息！"))

    if text == "探索畫框正面":
        painting_front = json.load(open('flex_file/painting_front.json','r',encoding='utf-8'))
        responses.append(FlexSendMessage(alt_text='painting_front', contents = painting_front))
        response_str = "畫框正面上有許多灰塵，也許這是3、40年前的老骨董了吧！"
        return responses,response_str


    elif text == "探索畫框背面":
        painting_back = json.load(open('flex_file/painting_back.json','r',encoding='utf-8'))
        responses.append(FlexSendMessage(alt_text='painting_back', contents = painting_back))
        response_str = "painting_back"
        #發現畫框背面後進入到state_03
        db.alter_user_state(u_id, 3)
        return responses,response_str

    #無意義的回覆就會進到這裡
    else:
        response_str = help_doing()
        responses.append(TextSendMessage(text = response_str))
        return responses,response_str

# state_03 解謎關卡
def state_03(text, u_id, player_level, current_state, current_location):
    
    responses = list()
    # responses.append(TextSendMessage(text="這是state_03的歡迎訊息！"))
    if text.rstrip().upper() == "BERT":
        responses = random_skill(u_id)
        response_str = "你成功破解畫中玄機了，等級得到了提升！"
        # player_level = 2
        db.alter_user_level(u_id, 2)
        # current_state = 2   
        db.alter_user_state(u_id, 2)

    else:
        response_str = "看來你尚未參透這些謎題，再加把勁吧~"
        # current_state = 2   
        db.alter_user_state(u_id, 2)

    responses.append(TextSendMessage(text = response_str)) 
    return responses,response_str

# state_04 寶箱關卡
def state_04(text, u_id, player_level, current_state, current_location):
    
    responses = list()
    # responses.append(TextSendMessage(text="這是state_04的歡迎訊息！"))

    if text == "打開寶箱":

        if(player_level == 2):

            treasure = json.load(open('flex_file/treasure.json','r',encoding='utf-8'))
            response_str = "贏了"
            responses.append(FlexSendMessage(alt_text='treasure', contents=treasure))
            # player_level = 3
            db.alter_user_level(u_id, 3)
            # current_state = 4   
            db.alter_user_state(u_id, 4)
            return responses,response_str

        else:
            response_str = "寶箱的縫連一張A4紙都過不去，也許該試試看其他方法？"

    #無意義的回覆就會進到這裡
    else:
        response_str = help_doing()
    
    responses.append(TextSendMessage(text = response_str))
    return responses,response_str

# state_05 空白地區&閒逛狀態
def state_05(text, u_id, player_level, current_state, current_location):

    responses = list()
    response_str = help_doing()
    # responses.append(TextSendMessage(text = "早安，Wish you a happy 2022!"))
    # response_str = "可以到處走走看看，有沒有新奇的發現呢？"
    responses.append(TextSendMessage(text = response_str)) 
    return responses,response_str
