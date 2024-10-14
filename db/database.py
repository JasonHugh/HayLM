from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

DATABASE_URL = "sqlite:///user_data/sqlite//chat.db"

class DatabaseUtil:
    _db_engine = None
    _session = None

    @classmethod
    def get_db_engine(cls):
        if cls._db_engine is None:
            cls._db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        return cls._db_engine

    @classmethod
    def get_session(cls):
        if cls._session is None:
            Session = sessionmaker(bind=cls.get_db_engine())
            cls._session = Session()
        return cls._session
    
if __name__ == "__main__":
    # init database
    db = DatabaseUtil.get_session()
    db.execute('''CREATE TABLE IF NOT EXISTS USER
            (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME            TEXT UNIQUE,
            PHONE           CHAR(11) UNIQUE,
            PASSWORD        TEXT,
            SN              CHAR(11) UNIQUE,
            CREATE_TIME     DATETIME,
            UPDATE_TIME     DATETIME);''')
    print ("USER created")

    db.execute('''CREATE TABLE IF NOT EXISTS USER_CONFIG
        (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID         INTEGER,
        AI_NAME         TEXT,
        AI_ROLE         TEXT,
        AI_PROFILE      TEXT,
        AI_TIMBRE       TEXT,
        AI_TTS_MODEL    TEXT,
        STYLED_ROLE_ID  INTEGER,
        CHILD_NAME      TEXT,
        CHILD_SEX       TEXT,
        CHILD_AGE       TEXT,
        CHILD_PROFILE   TEXT,
        LEARNING        TEXT,
        CREATE_TIME     DATETIME,
        UPDATE_TIME     DATETIME);''')
    # # insert test data
    db.execute("INSERT INTO USER_CONFIG (USER_ID, AI_NAME,AI_ROLE,AI_PROFILE,AI_TIMBRE,AI_TTS_MODEL,STYLED_ROLE_ID,CHILD_NAME,CHILD_SEX,CHILD_AGE,CHILD_PROFILE,LEARNING,CREATE_TIME,UPDATE_TIME) VALUES (1, '悟空', '西游记里的孙悟空','孙悟空（又称美猴王、齐天大圣、孙行者、斗战胜佛），是中国古典神魔小说《西游记》中的人物。由开天辟地产生的仙石孕育而生，出生地位于东胜神洲的花果山上，因带领猴群进入水帘洞而被尊为“美猴王”。 为了学艺而漂洋过海拜师于须菩提祖师，得名“孙悟空”， 学会大品天仙诀、七十二变 、筋斗云等高超的法术。','sambert-zhiying-v1','sambert', null, '奇大哥', 'boy', '3', '奇大哥是一个3岁的小男孩，性格有点内向', '', datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'))")
    print ("USER_CONFIG created")

    # every week, auto job will generate a summary for all history
    db.execute('''CREATE TABLE IF NOT EXISTS SESSION
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID      INTEGER,
        NAME         TEXT,
        SUMMARY      TEXT,
        IS_ACTIVE    BOOLEAN,
        CREATE_TIME  DATETIME,
        UPDATE_TIME     DATETIME);''')
    print ("SESSION created")

    db.execute('''CREATE TABLE IF NOT EXISTS HISTORY
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID      INTEGER,
        SESSION_ID   INTEGER,
        ROLE         TEXT,
        CONTENT      TEXT,
        IS_IMPORTANT BOOLEAN,
        CREATE_TIME  DATETIME);''')
    print ("HISTORY created")

    ''' history report, every week, auto job will generate a report for this week activities '''
    db.execute('''CREATE TABLE IF NOT EXISTS REPORT
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID      INTEGER,
        SESSION_ID   INTEGER,
        TITLE        TEXT,
        KEY_WORDS    TEXT,
        CONTENT      TEXT,
        START_DATE   DATE,
        END_DATE     DATE,
        CREATE_TIME  DATETIME);''')
    print ("SUMMARY created")


    db.execute('''CREATE TABLE IF NOT EXISTS AI_ROLE
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        AI_NAME      TEXT,
        ROLE_NAME    TEXT,
        CONTEXT      TEXT,
        PROFILE      TEXT,
        TIMBRE       TEXT,
        TTS_MODEL    TEXT,
        AUDIO_PATH   TEXT,
        AVATAR_PATH  TEXT,
        CREATE_TIME  DATETIME,
        UPDATE_TIME  DATETIME);''')
    # insert test data
    db.execute("INSERT INTO AI_ROLE (AI_NAME,ROLE_NAME,CONTEXT,PROFILE,TIMBRE,TTS_MODEL,CREATE_TIME,UPDATE_TIME) VALUES ('胡迪', '胡迪', '《玩具总动员》', '胡迪是玩具总动员系列电影中的一个怀旧的缝线牛仔玩偶，也是一名牛仔警长。他是安迪（Andy）自小最喜欢的玩具，在安迪（Andy）的床上有一块领地，而且是众玩具之首领。直到巴斯光年的到来。巴斯光年是一次Andy生日会得到的新玩具，当安迪（Andy）得到巴斯的时候，高兴得把其他玩具都扔在一边，但是巴斯却是胡迪一直以来最大的威胁。然而，经过了风风雨雨之后，胡迪和巴斯却建立了深厚的友情，并成为一辈子的好朋友。','sambert-zhiying-v1','sambert', datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime') )")
    db.execute("INSERT INTO AI_ROLE (AI_NAME,ROLE_NAME,CONTEXT,PROFILE,TIMBRE,TTS_MODEL,CREATE_TIME,UPDATE_TIME) VALUES ('艾莎', '艾莎公主', '《冰雪奇缘》', '艾莎公主，阿伦黛尔王国的大公主。艾莎外表高贵优雅、冷若冰霜、拒人千里，但她其实一直生活在恐惧里，努力隐藏着一个天大秘密，内心与强大的秘密搏斗——她天生具有呼风唤雪的神奇魔力，这种能力很美、但也极度危险。因为小时候她的魔法差点害死妹妹安娜，从此艾莎封闭了内心将自己隔离，时刻都在努力压制与日俱增的魔力。登基大典上的意外导致她的魔法失去控制，使得王国被冰天雪地所覆盖。她害怕自己的魔法会再次失控，于是逃进了雪山，并用魔法制造了一座城堡','sambert-zhiyuan-v1','sambert' , datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime') )")
    print ("AI_ROLE created")

    db.execute('''CREATE TABLE IF NOT EXISTS SN
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        SN           CHAR(11) UNIQUE,
        IS_USED      BOOLEAN,
        CREATE_TIME  DATETIME,
        UPDATE_TIME     DATETIME);''')
    # insert test data
    db.execute("INSERT INTO SN (SN,IS_USED,CREATE_TIME) VALUES ('HUESDOCFT46', 0 , datetime(CURRENT_TIMESTAMP,'localtime'))")
    db.execute("INSERT INTO SN (SN,IS_USED,CREATE_TIME) VALUES ('EUTI47CU9K3', 0 , datetime(CURRENT_TIMESTAMP,'localtime'))")
    print ("SN created")

    db.commit()