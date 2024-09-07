import schedule
import time

def data_generation():
    print("任务执行时间：", time.ctime())


if __name__ == "__main__":
    # every monday, generate weekly report and the history summary
    schedule.every().monday.at("01:00").do(data_generation)

    while True:
        schedule.run_pending()
        time.sleep(1)