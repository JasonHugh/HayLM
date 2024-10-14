from db.repositories import *
from util.schemas import *
from db.database import DatabaseUtil

class ContentService:
    def __init__(self):
        self.db = DatabaseUtil.get_session()

    def addHistory(self, history: History):
        if(not history.create_time):
            history.create_time =  get_current_time()
        return HistoryRepository.save(self.db, history)
        
    def addAIHistory(self, history: History):
        history.role = "assistant"
        if(not history.create_time):
            history.create_time =  get_current_time()
        return HistoryRepository.save(self.db, history)
    
    def addUserHistory(self, history: History):
        history.role = "user"
        history.is_important = True
        if(not history.create_time):
            history.create_time =  get_current_time()
        return HistoryRepository.save(self.db, history)
    
    def getHistories(self, user_id: int, session_id: int, date: str, is_important: bool) -> list[History]:
        return HistoryRepository.find_by_user_id(self.db, user_id)