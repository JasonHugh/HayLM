import sqlite3, os

db_dir = "user_data/sqlite"

if not os.path.exists(db_dir):
    os.makedirs(db_dir)

conn = sqlite3.connect(db_dir+"/chat.db")
c = conn.cursor()

def init_table():
    c.execute('''CREATE TABLE USER
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        NAME         TEXT,
        AGE          INTEGER,
        PHONE        CHAR(11),
        SN           CHAR(11));''')
    # insert test data
    c.execute("INSERT INTO USER (NAME,AGE,PHONE,SN) VALUES ('奇大哥', 3, '11011011011', 'SICO4JNI6K9')")
    print ("数据表USER创建成功")

    c.execute('''CREATE TABLE HISTORY
        (ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_ID      INTEGER
        ROLE         TEXT,
        CONTENT      TEXT,
        IS_IMPORTANT BOOLEAN,
        CREATE_TIME  DATETIME);''')
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
