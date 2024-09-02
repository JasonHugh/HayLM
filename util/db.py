import sqlite3, os
from .data_model import User

db_dir = "user_data/sqlite"
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

conn = sqlite3.connect(db_dir+"/chat.db")
c = conn.cursor()

def init_table():
    c.execute('''CREATE TABLE IF NOT EXISTS USER
        (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME            TEXT,
        PHONE           CHAR(11),
        PASSWORD        TEXT,
        SN              CHAR(11),
        CREATE_TIME     DATETIME,
        UPDATE_TIME     DATETIME);''')
    print ("数据表USER创建成功")

    c.execute('''CREATE TABLE IF NOT EXISTS USER_CONFIG
        (ID             INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID         INTEGER,
        AI_NAME         TEXT,
        ANIMATION       TEXT,
        ROLE_NAME       TEXT,
        CHILD_NAME      TEXT,
        CHILD_AGE       TEXT,
        CREATE_TIME     DATETIME,
        UPDATE_TIME     DATETIME);''')
    print ("数据表USER_CONFIG创建成功")

    c.execute('''CREATE TABLE IF NOT EXISTS SESSION
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID      INTEGER,
        NAME         TEXT,
        IS_ACTIVE    BOOLEAN,
        CREATE_TIME  DATETIME,
        UPDATE_TIME     DATETIME);''')
    print ("数据表SESSION创建成功")

    c.execute('''CREATE TABLE IF NOT EXISTS HISTORY
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID      INTEGER,
        SESSION_ID   INTEGER,
        ROLE         TEXT,
        CONTENT      TEXT,
        IS_IMPORTANT BOOLEAN,
        CREATE_TIME  DATETIME);''')
    print ("数据表HISTORY创建成功")


    c.execute('''CREATE TABLE IF NOT EXISTS SN
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        SN           CHAR(11) UNIQUE,
        IS_USED      BOOLEAN,
        CREATE_TIME  DATETIME,
        UPDATE_TIME     DATETIME);''')
    # insert test data
    c.execute("INSERT INTO SN (SN,IS_USED,CREATE_TIME) VALUES ('HUESDOCFT46', 0 , CURRENT_TIMESTAMP)")
    c.execute("INSERT INTO SN (SN,IS_USED,CREATE_TIME) VALUES ('EUTI47CU9K3', 0 , CURRENT_TIMESTAMP)")
    print ("数据表HISTORY创建成功")

    conn.commit()

def add_user_history(user_id, content, is_important:bool):
    __add_history(user_id, "user", content, is_important)

def add_ai_history(user_id, content, is_important:bool):
    __add_history(user_id, "assistent", content, is_important)

def add_system_prompt(user_id, content, is_important:bool):
    __add_history(user_id, "system", content, is_important)

def __add_history(user_id, role, content, is_important:bool):
    c.execute(f"INSERT INTO HISTORY (USER_ID,ROLE,CONTENT,IS_IMPORTANT,CREATE_TIME) VALUES ({user_id}, {role}, {content},{is_important}, CURRENT_TIMESTAMP)")
    conn.commit()

def close():
    conn.close()

def add_user(user: User):
    # is user name existing
    query = f"SELECT id FROM USER WHERE name='{user.name}'"
    c.execute(query)
    result = c.fetchone()
    if result:
        return False, "username exists"
    
    # is SN invalid
    query = f"SELECT id, is_used FROM SN WHERE SN='{user.SN}'"
    c.execute(query)
    result = c.fetchone()
    # no SN or SN is used
    if not result or result[1]:
        return False, "Invalid SN"
    
    SN_ID = result[0]
    
    try:
        # set SN used
        query = f"UPDATE SN set is_used=1,UPDATE_TIME=CURRENT_TIMESTAMP WHERE id='{SN_ID}'"
        c.execute(query)

        # init user
        query = f"INSERT INTO USER (NAME,PHONE,PASSWORD,SN,CREATE_TIME,UPDATE_TIME) VALUES ('{user.name}', '{user.phone}', '{user.password}','{user.SN}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
        c.execute(query)
        user_id = c.lastrowid
        conn.commit()
        return True, user_id
    except Exception:
        Exception.with_traceback()
        conn.rollback()
        return False, "add user failed"

def config_user(
        user_id: str = None, SN: str = None, ai_name: str = None,
        animation: str = None, role_name: str = None,
        child_name: str = None, child_age: int = None
    ):
    try:
        # init session
        query = f"INSERT INTO SESSION (USER_ID, NAME, IS_ACTIVE, CREATE_TIME) VALUES ({user_id}, 'MAIN', 1, CURRENT_TIMESTAMP)"
        c.execute(query)
        session_id = c.lastrowid
        # set config
        query = f"""INSERT INTO USER_CONFIG (USER_ID, AI_NAME, ANIMATION, ROLE_NAME, CHILD_NAME, CHILD_AGE, CREATE_TIME, UPDATE_TIME) 
        VALUES ('{user_id}', '{ai_name}', '{animation}', '{role_name}', '{child_name}', {child_age}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
        c.execute(query)
        conn.commit()
        return True, user_id
    except Exception:
        Exception.with_traceback()
        conn.rollback()
        return False, "config failed"

def get_user(user_name) -> User:
    query = f"SELECT id, name, phone, SN, password FROM USER WHERE name='{user_name}'"
    c.execute(query)
    result = c.fetchone()
    print(result)
    if result:
        return User(id = result[0], name = result[1], phone = result[2], SN = result[3], password = result[4])
    else:
        return None


if __name__ == "__main__":
    # init_table()
    # user = User.model_validate({"name":"hay", "phone":"11011011011", "SN":"HUESDOCFT46", "password":"hay123"})
    # print(user)
    # success, result = add_user(user)
    print(get_user("hay"))
