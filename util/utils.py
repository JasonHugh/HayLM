from datetime import datetime

def get_current_time_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_current_time_str_zh():
    return datetime.now().strftime("%Y年%m月%d日 %H点%M分%S秒")