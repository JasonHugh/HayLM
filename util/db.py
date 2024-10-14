import sqlite3, os

from db.models import History
from .data_model import User, UserConfig, Session, SN, AIRole
import threading
 
class SQLiteTool:
    _instance_lock = threading.Lock()
    
    def __init__(self, db_file):
        self.connection = None
        self.db_file = db_file
        self.cursor = None
 
    def connect(self):
        with SQLiteTool._instance_lock:
            if not self.connection:
                self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
                self.cursor = self.connection.cursor()
 
    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection
 
    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
 
    def __del__(self):
        self.close_connection()

    def init_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS USER
            (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME            TEXT UNIQUE,
            PHONE           CHAR(11) UNIQUE,
            PASSWORD        TEXT,
            SN              CHAR(11) UNIQUE,
            CREATE_TIME     DATETIME,
            UPDATE_TIME     DATETIME);''')
        print ("USER created")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS USER_CONFIG
            (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID         INTEGER,
            AI_NAME         TEXT,
            AI_ROLE         TEXT,
            AI_PROFILE      TEXT,
            STYLED_ROLE_ID  INTEGER,
            CHILD_NAME      TEXT,
            CHILD_SEX       TEXT,
            CHILD_AGE       TEXT,
            CHILD_PROFILE   TEXT,
            LEARNING        TEXT,
            CREATE_TIME     DATETIME,
            UPDATE_TIME     DATETIME);''')
        # # insert test data
        self.cursor.execute("INSERT INTO USER_CONFIG (USER_ID, AI_NAME,AI_ROLE,AI_PROFILE,STYLED_ROLE_ID,CHILD_NAME,CHILD_SEX,CHILD_AGE,CHILD_PROFILE,LEARNING,CREATE_TIME,UPDATE_TIME) VALUES (1, '悟空', '西游记里的孙悟空','孙悟空（又称美猴王、齐天大圣、孙行者、斗战胜佛），是中国古典神魔小说《西游记》中的人物。由开天辟地产生的仙石孕育而生，出生地位于东胜神洲的花果山上，因带领猴群进入水帘洞而被尊为“美猴王”。 为了学艺而漂洋过海拜师于须菩提祖师，得名“孙悟空”， 学会大品天仙诀、七十二变 、筋斗云等高超的法术。', null, '奇大哥', 'boy', '3', '奇大哥是一个3岁的小男孩，性格有点内向', '', datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'))")
        print ("USER_CONFIG created")

        # every week, auto job will generate a summary for all history
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS SESSION
            (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID      INTEGER,
            NAME         TEXT,
            SUMMARY      TEXT,
            IS_ACTIVE    BOOLEAN,
            CREATE_TIME  DATETIME,
            UPDATE_TIME     DATETIME);''')
        print ("SESSION created")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS HISTORY
            (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID      INTEGER,
            SESSION_ID   INTEGER,
            ROLE         TEXT,
            CONTENT      TEXT,
            IS_IMPORTANT BOOLEAN,
            CREATE_TIME  DATETIME);''')
        print ("HISTORY created")

        ''' history report, every week, auto job will generate a report for this week activities '''
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS REPORT
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


        self.cursor.execute('''CREATE TABLE IF NOT EXISTS AI_ROLE
            (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            AI_NAME      TEXT,
            ROLE_NAME    TEXT,
            CONTEXT      TEXT,
            PROFILE      TEXT,
            TIMBRE       TEXT,
            TTS_MODEL    TEXT,
            CREATE_TIME  DATETIME,
            UPDATE_TIME  DATETIME);''')
        # insert test data
        self.cursor.execute("INSERT INTO AI_ROLE (AI_NAME,ROLE_NAME,CONTEXT,PROFILE,TIMBRE,TTS_MODEL,CREATE_TIME,UPDATE_TIME) VALUES ('胡迪', '胡迪', '《玩具总动员》', '胡迪是玩具总动员系列电影中的一个怀旧的缝线牛仔玩偶，也是一名牛仔警长。他是安迪（Andy）自小最喜欢的玩具，在安迪（Andy）的床上有一块领地，而且是众玩具之首领。直到巴斯光年的到来。巴斯光年是一次Andy生日会得到的新玩具，当安迪（Andy）得到巴斯的时候，高兴得把其他玩具都扔在一边，但是巴斯却是胡迪一直以来最大的威胁。然而，经过了风风雨雨之后，胡迪和巴斯却建立了深厚的友情，并成为一辈子的好朋友。','sambert-zhiying-v1','sambert', datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime') )")
        self.cursor.execute("INSERT INTO AI_ROLE (AI_NAME,ROLE_NAME,CONTEXT,PROFILE,TIMBRE,TTS_MODEL,CREATE_TIME,UPDATE_TIME) VALUES ('艾莎', '艾莎公主', '《冰雪奇缘》', '艾莎公主，阿伦黛尔王国的大公主。艾莎外表高贵优雅、冷若冰霜、拒人千里，但她其实一直生活在恐惧里，努力隐藏着一个天大秘密，内心与强大的秘密搏斗——她天生具有呼风唤雪的神奇魔力，这种能力很美、但也极度危险。因为小时候她的魔法差点害死妹妹安娜，从此艾莎封闭了内心将自己隔离，时刻都在努力压制与日俱增的魔力。登基大典上的意外导致她的魔法失去控制，使得王国被冰天雪地所覆盖。她害怕自己的魔法会再次失控，于是逃进了雪山，并用魔法制造了一座城堡','sambert-zhiyuan-v1','sambert' , datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime') )")
        print ("AI_ROLE created")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS SN
            (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
            SN           CHAR(11) UNIQUE,
            IS_USED      BOOLEAN,
            CREATE_TIME  DATETIME,
            UPDATE_TIME     DATETIME);''')
        # insert test data
        self.cursor.execute("INSERT INTO SN (SN,IS_USED,CREATE_TIME) VALUES ('HUESDOCFT46', 0 , datetime(CURRENT_TIMESTAMP,'localtime'))")
        self.cursor.execute("INSERT INTO SN (SN,IS_USED,CREATE_TIME) VALUES ('EUTI47CU9K3', 0 , datetime(CURRENT_TIMESTAMP,'localtime'))")
        print ("SN created")

        self.connection.commit()

    def add_user_history(self, user_id, session_id, content, is_important:bool):
        self.__add_history(user_id, session_id, "user", content, is_important)

    def add_ai_history(self, user_id, session_id, content, is_important:bool):
        self.__add_history(user_id, session_id, "assistant", content, is_important)

    def __add_history(self, user_id, session_id, role, content: str, is_important:bool):
        try:
            self.cursor.execute("INSERT INTO HISTORY (USER_ID,SESSION_ID,ROLE,CONTENT,IS_IMPORTANT,CREATE_TIME) VALUES (?, ?, ?, ?, ?, datetime(CURRENT_TIMESTAMP,'localtime'))", (user_id,session_id,role,content,is_important))
            self.connection.commit()
            return True, self.cursor.lastrowid
        except Exception as e:
            e.with_traceback()
            self.connection.rollback()
            return False, "add history failed"
        
    def add_user(self, user: User):
        # is user name existing
        query = f"SELECT id FROM USER WHERE name='{user.name}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return False, "Username exists"
        
        # is SN invalid
        query = f"SELECT id, is_used FROM SN WHERE SN='{user.SN}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        # no SN or SN is used
        if not result or result[1]:
            return False, "Invalid SN"
        
        SN_ID = result[0]
        
        try:
            # set SN used
            query = f"UPDATE SN set is_used=1,UPDATE_TIME=datetime(CURRENT_TIMESTAMP,'localtime') WHERE id='{SN_ID}'"
            self.cursor.execute(query)

            # init user
            query = f"INSERT INTO USER (NAME,PHONE,PASSWORD,SN,CREATE_TIME,UPDATE_TIME) VALUES ('{user.name}', '{user.phone}', '{user.password}','{user.SN}', datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'))"
            self.cursor.execute(query)
            user_id = self.cursor.lastrowid
            self.connection.commit()
            return True, user_id
        except Exception:
            Exception.with_traceback()
            self.connection.rollback()
            return False, "add user failed"

    def config_user(
            self, 
            user_config: UserConfig
        ):
        try:
            # set config
            query = f"""INSERT INTO USER_CONFIG (USER_ID, AI_NAME, AI_ROLE,AI_PROFILE,STYLED_ROLE_ID, CHILD_NAME, CHILD_AGE, child_profile, child_sex, learning, CREATE_TIME, UPDATE_TIME) 
            VALUES (?,?,?,?,?,?,?,?,?,?, datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'))"""
            self.cursor.execute(query, (user_config.user_id,user_config.ai_name,user_config.ai_role,user_config.ai_profile,user_config.styled_role_id,user_config.child_name,user_config.child_age,user_config.child_profile,user_config.child_sex,user_config.learning))

            # init session
            query = f"INSERT INTO SESSION (USER_ID, NAME, summary, IS_ACTIVE, CREATE_TIME, UPDATE_TIME) VALUES ({user_config.user_id}, 'MAIN', '', 1, datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'))"
            self.cursor.execute(query)
            session_id = self.cursor.lastrowid

            self.connection.commit()
            return True, session_id
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False, "config failed"

    def get_user(self, username) -> User:
        query = f"SELECT id, name, phone, SN, password, create_time, update_time FROM USER WHERE name='{username}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return User(id = result[0], name = result[1], phone = result[2], SN = result[3], password = result[4], create_time = result[5], update_time = result[6])
        else:
            return None
        
    def get_user_config(self, user_id) -> UserConfig:
        query = f"SELECT * from USER_CONFIG WHERE user_id={user_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return UserConfig(id = result[0], user_id = result[1], ai_name = result[2], ai_role = result[3], ai_profile=result[4], styled_role_id = result[5], child_name = result[6], child_sex = result[7], child_age = result[8], child_profile = result[9], learning = result[10], create_time = result[11], update_time = result[12])
        else:
            return None
    
    def get_active_session(self, user_id: int) -> Session:
        query = f"SELECT id, user_id, name, summary, is_active, create_time, update_time FROM SESSION WHERE user_id={user_id} and is_active={True}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return Session(id = result[0], user_id=result[1], name = result[2], summary = result[3], is_active = result[4], create_time = result[5], update_time = result[6])
        else:
            return None
        
    def get_history(self, user_id: int, session_id: int, date: str, is_important: bool = None, batchSize: int = 10) -> list[History]:
        if is_important == None:
            important_sql = ""
        else:
            important_sql = f"and is_important={is_important}"
        query = f"SELECT id, user_id, session_id, role, content, is_important, create_time FROM HISTORY WHERE user_id={user_id} and session_id={session_id} and date(create_time)='{date}' {important_sql} order by id desc limit {batchSize*2}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            histories = []
            for r in result:
                histories.append(History(id = r[0], user_id = r[1], session_id = r[2], role = r[3], content = r[4], is_important = r[5], create_time = r[6]))
            return list(reversed(histories))
        else:
            return None
        
    def delete_history(self, history_id: int) -> bool:
        try:
            query = f"delete from HISTORY where ID={history_id}"
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            print(e.with_traceback())
            self.connection.rollback()
            return False

    def get_sn(self) -> list[SN]:
        query = f"SELECT * FROM SN"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if result:
            SNs = []
            for r in result:
                SNs.append(SN(id = r[0], SN = r[1], is_used = r[2], create_time = r[3], update_time = r[4]))
            return SNs
        else:
            return None


if __name__ == "__main__":
    db_dir = "user_data/sqlite"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    sqlite_tool = SQLiteTool(db_dir + '/chat.db')
    sqlite_tool.connect()

    # sqlite_tool.init_table()
    # sqlite_tool.add_user_history(1,1,"\"sxs\"",True)
    # print(sqlite_tool.get_important_history(1,1, is_important=True))
    print(sqlite_tool.get_history(1,1,"2024-09-09"))


    # query = f"delete from HISTORY"
    # sqlite_tool.cursor.execute(query)
    # sqlite_tool.connection.commit()