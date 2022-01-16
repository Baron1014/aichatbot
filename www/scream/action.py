from db import Linelog
from db import get_user_id, get_user_input_id, get_user_max_questionid, get_user_state, insert_questionlog, get_user_location 
import db

from content import icon_map
import similar
from random import randrange
from linebot.models import TextSendMessage
import pandas as pd
import predict

def user_move(event, orientation):
    # content
    user = event.source.user_id
    # user_input = event.message.text
    # get information from database
    user_id = get_user_id(user)
    # user_input_id = get_user_input_id(user_input)
    # robot_question = get_user_max_questionid(user_id)
    # linelog = Linelog(user_id, user_input_id, robot_question, tags=1)
    # db.insert(linelog)

    # update user table
    map_str = get_user_location(user)
    response, update_str, response_str = icon_map.update_player(map_str, orientation)
    db.alter_user_map(user, update_str)
    ###################################################
    ###################################################
    ###################################################
    # 更改current state
    user_x, user_y = db.get_player_location(user)
    
    if  2<= user_x <= 4 and 5 <= user_y <= 6:
        # state_02探索畫框
        db.alter_user_state(user, 2)
    
    elif 1 <= user_x <= 3 and 1 <= user_y <= 3:
        # state_04寶箱  
        db.alter_user_state(user, 4)

    elif 4 <= user_x <= 6 and 1 <= user_y <= 4:
        # state_01殺雞殺豬
        db.alter_user_state(user, 1)
    else:
        # 隨便逛
        db.alter_user_state(user, 5)
    ###################################################
    ###################################################
    ###################################################

    # update question table
    #db.insert_questionlog(user_id, response_str)

    return response 

def predict_tag(event):
    # content
    user = event.source.user_id
    user_input = event.message.text


    # get information from database
    user_id = get_user_id(user)
    user_input_id = get_user_input_id(user_input)
    robot_question = get_user_max_questionid(user_id)
    state = db.get_user_state(user)

    # 1. cosine similarity
    sim_entity, sim_score = similar.get_most_similar(user_input)
    sim_tag = sim_entity[1]
    bert_tag = "None"
    if sim_score < 0.6:
        # 2. Bert Model
        state_string = db.get_state_name(state)
        label_entity_list = db.get_all_labels()
        labels = {tag: t_id-1 for t_id, tag in label_entity_list}
        test_df = pd.DataFrame(data=[(state_string, user_input)], columns=["state", "user"])
        bert_tag = predict.state(test_df, "models/bert", labels, NUM_LABELS=14)
        

    linelog = Linelog(user_id, user_input_id, robot_question, state, tags=sim_tag, predict_score=sim_score, bert_tags=bert_tag)
    db.insert(linelog)

    return db.get_tag_name(sim_tag) if bert_tag == "None" else bert_tag

def attack(u_id):
    # information
    user = db.find_user(u_id)
    user_skill = db.get_skill_name(user.cool_skill)

    # randint
    seed = randrange(1, 6)
    power = seed*user.level

    # reply
    reply_dict = {
            1:f"你肚子非常餓，輕輕碰了一下野豬，野豬發狂向你衝撞，因為作用力與反作用力兩者都受到了一樣的傷害\n🐗【血量下降了1】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            2:f"你伸手拔了一根野豬的毛，但野豬太久沒洗澡使你受不了那味道\n🐗【血量下降了2】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            3:f"你騎上了野豬，使野豬撞擊牆壁，而你被野豬甩下至地面\n🐗【血量下降了3】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            4:f"你大力打斷了野豬的獠牙，你發現你的手也正在流血\n🐗【血量下降了4】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            5:f"你攻擊野豬鼻子，因此重擊了野豬，野豬也發了狂的向你咬了一口\n🐗【血量下降了5】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            6:f"你從野豬背後給他一擊重擊，然而野豬對你咬了一口\n🐗【血量下降了6】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            8:f"你使用了剛剛學到的{user_skill}，而野豬也不甘示弱朝你咆嘯\n🐗【血量下降了8】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            9:f"寶箱的珠光寶氣光芒萬丈使你{user_skill}能量大增，你毫不猶豫揮向野豬時攻擊到了野豬的豬蹄\n🐗【血量下降了9】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            10:f"你對野豬使用{user_skill}，雖然沒有直接擊中，但產生的霸氣足以使野豬受到重擊，而你因為對技能操作不熟悉也受到了傷害\n🐗【血量下降了10】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            12: f"你對野豬使用{user_skill}產生爆擊，野豬不甘示弱地朝你衝撞過來\n🐗【血量下降了12】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            15: f"從寶箱吸收到的能量使你更加領悟{user_skill}的奧妙，直接使野豬造成重傷，此能量過於強大使你也受了傷害\n🐗【血量下降了15】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】",
            18: f"利用自己的生命使{user_skill}得到終極強化，野豬受到爆擊後產生奄奄一息的狀態...\n🐗【血量下降了18】\n🐗【目前血量：{(user.pig_hp-power)//5*'❤️'}】\n🤠【生命值扣1】\n🤠【目前血量：{(user.player_hp-1)*'❤️'}】"}

    # alter database
    db.alter_hp(u_id, player_hp=user.player_hp-1, pig_hp=user.pig_hp-power)

    return reply_dict[power]

def killed_pig(user):
    map_str = db.get_user_location(user)
    map_str = map_str.replace("P", "M")
    db.alter_user_map(user, map_str)

    return TextSendMessage(text=icon_map.set_icon(map_str))


if __name__=="__main__":
    #db.alter_user_state("123", 2)
    print(attack("123"))

