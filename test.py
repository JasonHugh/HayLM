import os
from util.schemas import UserRequest, UserResponse
from db.repositories import *
from db.models import *
from sqlalchemy.orm import Session
from db.database import DatabaseUtil
from sqlalchemy import text


db: Session = DatabaseUtil.get_session()
# db.execute(text("drop table AI_ROLE"))
# db.execute(text('''CREATE TABLE IF NOT EXISTS AI_ROLE
#         (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
#         AI_NAME      TEXT,
#         ROLE_NAME    TEXT,
#         CONTEXT      TEXT,
#         PROFILE      TEXT,
#         TIMBRE       TEXT,
#         TTS_MODEL    TEXT,
#         AUDIO_PATH   TEXT,
#         AVATAR_PATH  TEXT,
#         CREATE_TIME  DATETIME,
#         UPDATE_TIME  DATETIME);'''))
# # insert test data
# db.execute(text("INSERT INTO AI_ROLE (AI_NAME,ROLE_NAME,CONTEXT,PROFILE,TIMBRE,TTS_MODEL,AUDIO_PATH,AVATAR_PATH,CREATE_TIME,UPDATE_TIME) VALUES ('胡迪', '胡迪', '《玩具总动员》', '胡迪是玩具总动员系列电影中的一个怀旧的缝线牛仔玩偶，也是一名牛仔警长。他是安迪（Andy）自小最喜欢的玩具，在安迪（Andy）的床上有一块领地，而且是众玩具之首领。直到巴斯光年的到来。巴斯光年是一次Andy生日会得到的新玩具，当安迪（Andy）得到巴斯的时候，高兴得把其他玩具都扔在一边，但是巴斯却是胡迪一直以来最大的威胁。然而，经过了风风雨雨之后，胡迪和巴斯却建立了深厚的友情，并成为一辈子的好朋友。','sambert-zhibin-v1','sambert','hudi.mp3' ,'hudi-avatar.png',datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime') )"))
# db.execute(text("INSERT INTO AI_ROLE (AI_NAME,ROLE_NAME,CONTEXT,PROFILE,TIMBRE,TTS_MODEL,AUDIO_PATH,AVATAR_PATH,CREATE_TIME,UPDATE_TIME) VALUES ('艾莎', '艾莎公主', '《冰雪奇缘》', '艾莎公主，阿伦黛尔王国的大公主。艾莎外表高贵优雅、冷若冰霜、拒人千里，但她其实一直生活在恐惧里，努力隐藏着一个天大秘密，内心与强大的秘密搏斗——她天生具有呼风唤雪的神奇魔力，这种能力很美、但也极度危险。因为小时候她的魔法差点害死妹妹安娜，从此艾莎封闭了内心将自己隔离，时刻都在努力压制与日俱增的魔力。登基大典上的意外导致她的魔法失去控制，使得王国被冰天雪地所覆盖。她害怕自己的魔法会再次失控，于是逃进了雪山，并用魔法制造了一座城堡','sambert-zhimiao-emo-v1','sambert' , 'aisha.wav','aisha-avatar.png',datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime') )"))
# db.commit()
ai = AIRoleRepository.find_all(db)
for a in ai:
    print(a.timbre)
user = UserRepository.find_by_id(db,1)
print(user)
userConfig = UserConfigRepository.find_by_id(db,1)
print(userConfig.styled_role_id)