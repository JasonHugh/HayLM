from db.repositories import *
from util.schemas import *
from db.database import DatabaseUtil
from .response_models import GameResponse

class GameService:
    def __init__(self):
        self.db = DatabaseUtil.get_session()

    def add_game(self, history: History):
        if(not history.create_time):
            history.create_time =  get_current_time()
        return HistoryRepository.save(self.db, history)
    
    def find_all(self) -> list[Game]:
        return GameRepository.find_all(self.db)
    
    def find_by_id(self, id:int) -> Game:
        return GameRepository.find_by_id(self.db, id)
    
    def get_game_list(self) -> list[GameResponse]:
        games: list[Game] = GameRepository.find_all(self.db)
        return [GameResponse.model_validate(game) for game in games]