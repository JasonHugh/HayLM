from util.db import SQLiteTool

user_dir = "user_data"

# sqlite init
db_dir = user_dir + "/sqlite"
sqlite_tool = SQLiteTool(db_dir + '/chat.db')
sqlite_tool.connect()
# print(sqlite_tool.get_history(user_id=1, session_id=1, date="2024-09-11"))
sqlite_tool.delete_history(history_id=77)