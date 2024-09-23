import sqlite3, os
from .data_model import User, UserConfig, History, Session, SN
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
            PLAYED_ROLE     TEXT,
            CHILD_NAME      TEXT,
            CHILD_SEX       TEXT,
            CHILD_AGE       TEXT,
            CHILD_PROFILE   TEXT,
            LEARNING        TEXT,
            CREATE_TIME     DATETIME,
            UPDATE_TIME     DATETIME);''')
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
            query = f"""INSERT INTO USER_CONFIG (USER_ID, AI_NAME, played_role, CHILD_NAME, CHILD_AGE, child_profile, child_sex, learning, CREATE_TIME, UPDATE_TIME) 
            VALUES ({user_config.user_id}, '{user_config.ai_name}', '{user_config.played_role}', '{user_config.child_name}', {user_config.child_age}, '{user_config.child_profile}', '{user_config.child_sex}','{user_config.learning}', datetime(CURRENT_TIMESTAMP,'localtime'), datetime(CURRENT_TIMESTAMP,'localtime'))"""
            self.cursor.execute(query)

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
        query = f"SELECT ID, USER_ID, AI_NAME, played_role, CHILD_NAME, CHILD_AGE, child_profile, child_sex, learning, CREATE_TIME, UPDATE_TIME from USER_CONFIG WHERE user_id={user_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            return UserConfig(id = result[0], user_id = result[1], ai_name = result[2], played_role = result[3], child_name = result[4], child_age = result[5], child_profile = result[6], child_sex = result[7], learning = result[8], create_time = result[9], update_time = result[10])
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