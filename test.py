import os
from service.user_service import UserService
from service.content_service import ContentService
from util.schemas import UserRequest, UserResponse
from service.game_service import GameService
from db.repositories import *
from db.models import *
from sqlalchemy.orm import Session
from db.database import DatabaseUtil
from sqlalchemy import text



db: Session = DatabaseUtil.get_session()
# db.execute(text("delete from HISTORY"))
# db.commit()

# historyRepository = HistoryRepository()
# histories = historyRepository.find_by_user(db, 1, 1, '2024-12-12',1)
# for history in histories:
#     print(history.id)
#     print(history.role)
#     print(history.is_important)
#     print(history.session_id)
#     print(history.user_id)
#     print(history.create_time)
# ai = AIRoleRepository.find_all(db)
# for a in ai:
#     print(a.timbre)
# user = UserRepository.find_by_id(db,1)
# print(user)
# userConfig = UserConfigRepository.find_by_id(db,1)
# print(userConfig.game_enable)

# for history in ContentService().get_histories(1,2,'2025-01-14'):
#     print(history.content)
#     print(history.create_time)
# db.commit()


# for session in UserService().get_user_sessions(1):
#     print(session.id)
#     print(session.name)
#     print(session.is_active)

for game in GameService().find_all():
    print(game.prompt)

# with open('/home/lighthouse/HayLM/game_taikong_prompt.txt', 'r', encoding="utf-8") as f:
#         prompt = f.read()
#         print(prompt)
#         game = GameService().find_by_id(3)
#         game.prompt = prompt
#         gameRepository = GameRepository()
#         gameRepository.save(db, game)
#         db.commit()