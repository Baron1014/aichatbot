from linebot.models import TextSendMessage
from content import icon_map
from db import User
import db
from linebot.models import FlexSendMessage
import json

def get_response(user_id):
    responses = list()
    # responses.append(TextSendMessage(text="這是一個發生在地球上的故事。\n你是一位無能的廢材研究生，在這個世界裡拓展自己的一片天。你英檢一直考不過，最後賠光積蓄。無處可去的你，意外的進到這個廢棄的空房間裡..."))
    # responses.append(TextSendMessage(text="\"碰的一聲巨響！！\"你發現門突然關上，在伸手不見五指的房間中，你隱約看見正前方有一隻兇猛的野豬，在他旁邊是隻看起來美味可口的尖叫小雞...."))
    
    # map reply & save
    init_map, mapstr = icon_map.get_map()
    # 若使用者出現於資料庫則進行更新
    if db.find_user(user_id) != None:
        db.alter_user_map(user_id, mapstr)
    # responses.append(init_map) 
    # responses.append(TextSendMessage(text="\"框啷框啷....\" 你試圖推開上鎖的大門，冷冽的金屬撞擊聲在絕望的漆黑房間中迴盪，現在你只有兩個選擇，一是在這饑寒交迫而死，二是想辦法利用房間裡的資源逃出這裡，你要如何抉擇呢？(請告訴我你想做什麼？)"))
   
    db.insert_questionlog(db.get_user_id(user_id), "無計可施的你該怎麼討出生天呢？")
    start = json.load(open('flex_file/start.json','r',encoding='utf-8'))

    
    return [FlexSendMessage(alt_text='start', contents=start)]