from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from content import icon_map

import pandas as pd

app = Flask(__name__)

# MySql datebase
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./scream.db"
db = SQLAlchemy(app)

#################
# 紀錄每筆line log
#################
class Linelog(db.Model):
    __tablename__ = 'linelog'
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.pid'), nullable=False)
    user_input = db.Column(db.Integer, db.ForeignKey('user_input.pid'), nullable=False)
    robot_question = db.Column(db.Integer, db.ForeignKey('question_log.user_question_pid'), nullable=False)
    state = db.Column(db.Integer, db.ForeignKey('state.pid'), nullable=False)
    predict_tags = db.Column(db.Integer, db.ForeignKey('tags.pid'), nullable=False)
    predict_score = db.Column(db.Float, nullable=False)
    bert_tags = db.Column(db.String(30), default=None)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    db_log_train = db.relationship("Train", backref="linelog")

    def __init__(self, user_id, user_input, robot_question, state, tags, predict_score, bert_tags):
        self.user_id = user_id
        self.user_input = user_input
        self.robot_question = robot_question
        self.state = state
        self.predict_tags = tags
        self.predict_score = predict_score
        self.bert_tags = bert_tags

#################
# 訓練資料
#################
class Train(db.Model):
    __tablename__ = 'train_data'
    pid = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('linelog.pid'), nullable=False)
    training_tag = db.Column(db.Integer,default=-1,  nullable=False)

    def __init__(self, log_id):
        self.log_id = log_id

def get_all_training_data():
    sql = 'SELECT DISTINCT ui.user_input, td.training_tag from train_data td inner join linelog l, user_input ui on td.log_id = l.pid and l.user_input = ui.pid'
    return db.engine.execute(sql).fetchall()

def get_bert_training_data():
    sql = "SELECT s.state_name,ui.user_input , t.tag_name from train_data td inner join linelog l, user_input ui, state s, tags t on td.log_id = l.pid  and l.user_input =ui.pid and l.state =s.pid and td.training_tag = t.pid"
    return db.engine.execute(sql).fetchall()
    

#################
# 紀錄使用者狀態
#################
class User(db.Model):
    __tablename__ = 'user'
    pid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    current_state = db.Column(db.Integer, db.ForeignKey('state.pid'), nullable=False, default=1)
    _, init_map = icon_map.get_map()
    uimap = db.Column(db.String(200), nullable=False, default=init_map)
    level = db.Column(db.Integer, nullable=False, default=1)
    cool_skill = db.Column(db.Integer, db.ForeignKey('skills.pid'), nullable=False, default=1)
    player_hp = db.Column(db.Integer, nullable=False, default=3)
    pig_hp = db.Column(db.Integer, nullable=False, default=20)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    db_user_log = db.relationship("Linelog", backref="user")

    def __init__(self, user_name, uimap=None, level=None, current_state=None):
        self.user_name = user_name

        if uimap is not None:
            self.uimap = uimap
        if level is not None:
            self.level = level
        if current_state is not None:
            self.current_state = current_state
    
# 取得使用者得entity, 若使用者不存在則回傳None
def find_user(user):
    return User.query.filter_by(user_name=user).first()

# 輸入使用者Line ID回傳使用者編碼，若使用者不存在則進行新增
def get_user_id(user):
    if find_user(user)==None:
        new_user = User(user)
        insert(new_user)
    new_entity = find_user(user)
    return new_entity.pid

# 取得使用者current state
def get_user_state(user):
    if find_user(user)==None:
        new_user = User(user)
        insert(new_user)
    new_entity = find_user(user)
    return new_entity.current_state

# 取得使用者地圖資訊(非xy座標)
def get_user_location(user):
    entity = find_user(user)
    return entity.uimap

# 更新使用者地圖資訊
def alter_user_map(user, upmap):
    entity = find_user(user)
    entity.uimap = upmap
    db.session.commit()

# 取得玩家在地圖的(x,y)座標
def get_player_location(user):
    entity = find_user(user)
    location = entity.uimap.find("U")
    row = location // 9 
    col = location % 9

    return row, col

# 取得使用者目前level
def get_user_level(user):
    entity = find_user(user)
    return entity.level

# 更新使用者level
def alter_user_level(user, level):
    entity = find_user(user)
    entity.level = level
    db.session.commit()

# 更新使用者current state
def alter_user_state(user, state_id):
    if check_state_id(state_id):
        entity = find_user(user)
        entity.current_state = state_id
        db.session.commit()

# 更新玩家技能
def alter_user_skill(user, skill_id):
    if check_skill_id(skill_id):
        entity = find_user(user)
        entity.cool_skill = skill_id
        db.session.commit()

# 取得使用者目前技能
def get_user_skill(user):
    entity = find_user(user)
    return entity.cool_skill

# 更新玩家及野豬血量
def alter_hp(user, player_hp, pig_hp):
    entity = find_user(user)
    entity.player_hp = player_hp
    entity.pig_hp = pig_hp
    db.session.commit()

###############
# 使用者輸入
###############
class UserInput(db.Model):
    __tablename__ = 'user_input'
    pid = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(50), unique=True, nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    db_input_log = db.relationship("Linelog", backref="input")

    def __init__(self, user_input):
        self.user_input = user_input

# 取得使用者輸入，若不存在回傳None
def find_user_input(user_input):
    return UserInput.query.filter_by(user_input=user_input).first()

# 取得使用者輸入編碼數字
def get_user_input_id(user_input):
    if find_user_input(user_input)==None:
        new_user_input = UserInput(user_input)
        insert(new_user_input)
    new_entity = find_user_input(user_input)
    return new_entity.pid

##########################
# 記錄使用者前一個問題
##########################
class QuestionLog(db.Model):
    __tablename__ = 'question_log'
    pid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_question_pid = db.Column(db.Integer, db.ForeignKey('question.pid'), nullable=False, default=0)
    question_id = db.Column(db.Integer, nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    db_questionlog_log = db.relationship("Linelog", backref="questionlog")


    def __init__(self, user_id, question_id, user_question_pid=False):
        self.user_id = user_id
        self.question_id = question_id
        if user_question_pid is not False:
            self.user_question_pid = user_question_pid

# 取得QuestionLog entity, 若不存在則回傳None
def find_questionlog(user):
    q = QuestionLog.query
    return q.order_by(QuestionLog.user_question_pid.desc()).filter_by(user_id = user).first()

# 新增一筆question log 至資料庫
def insert_questionlog(user_pid, question):
    question_id = get_question_id(question)
    user_question_pid = get_user_max_questionid(user_pid)+1
    questionlog_entity = QuestionLog(user_pid, question_id, user_question_pid)
    insert(questionlog_entity)

# 取得使用者最後一筆問題
def get_user_max_questionid(user_pid):
    if find_questionlog(user_pid)==None:
        new_questionlog = QuestionLog(user_pid, question_id=1)
        insert(new_questionlog)
    new_entity = find_questionlog(user_pid)
    return new_entity.user_question_pid


##########################
# 記錄所有問題
##########################
class Question(db.Model):
    __tablename__ = 'question'
    pid = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(50), unique=True, nullable=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    db_question_log = db.relationship("QuestionLog", backref="question")
    

    def __init__(self, question):
        self.question = question
    
# 取得機器人問題entity, 若不存在則回傳None
def find_question(question):
    return Question.query.filter_by(question=question).first()

# 取得機器人問題編碼數字
def get_question_id(question):
    if find_question(question)==None:
        new_question = Question(question)
        insert(new_question)
    new_entity = find_question(question)
    return new_entity.pid


##########################
# 紀錄所有遊戲狀態種類
##########################
class GameState(db.Model):
    __tablename__ = 'state'
    pid = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(30), unique=True, nullable=False)

    db_state_log = db.relationship("User", backref="state")
    db_state_linelog = db.relationship("Linelog", backref="linestate")

    def __init__(self, state_name):
        self.state_name = state_name

# 取得state名稱
def get_state_name(state_id):
    q = GameState.query.filter_by(pid=state_id).first()
    if q is not None:
        return q.state_name
    else:
        return None

# 檢查state是否存在
def check_state_id(state_id):
    q = GameState.query.filter_by(pid=state_id).first()
    if q is not None:
        return True
    else:
        return False

#################
# 訓練標籤
#################
class Tags(db.Model):
    __tablename__ = 'tags'
    pid = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30), unique=True, nullable=False)
    des = db.Column(db.String(50), nullable=False)
    
    db_state_log = db.relationship("Linelog", backref="tag")

    def __init__(self, tag_name):
        self.tag_name = tag_name

# 取得state名稱
def get_tag_name(tag_id):
    q = Tags.query.filter_by(pid=tag_id).first()
    if q is not None:
        return q.tag_name
    else:
        return None

def get_all_labels():
    sql = "SELECT pid, tag_name from tags"
    return db.engine.execute(sql).fetchall()
#################
# 酷炫招式
#################
class Skills(db.Model):
    __tablename__ = 'skills'
    pid = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(30), unique=True, nullable=False)
    skill_reply = db.Column(db.String(50), nullable=False)

    db_skill_log = db.relationship("User", backref="skill")

    def __init__(self, tag_name):
        self.tag_name = tag_name

# 取得技能名稱
def get_skill_name(skill_id):
    q = Skills.query.filter_by(pid=skill_id).first()
    if q is not None:
        return q.skill_name
    else:
        return None

# 檢查技能是否已經存在於資料庫中
def check_skill_id(skill_id):
    q = Skills.query.filter_by(pid=skill_id).first()
    if q is not None:
        return True
    else:
        return False

# insert data entity to database
def insert(db_entity):
    db.session.add(db_entity)
    db.session.commit()


if __name__=="__main__":
    db.create_all()
    #user = User('123')
    #insert(user)
    # alter_user_skill('123', 20)
    # print(get_skill_name(20))
    #print(get_user_level("123"))
    #alter_user_level("123", 4)
