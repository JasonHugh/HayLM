from db.repositories import *
from util.schemas import *
from db.database import DatabaseUtil
from passlib.context import CryptContext

class UserService:
    def __init__(self):
        self.db = DatabaseUtil.get_session()

    def login(self):
        pass

    def register(self, userRequest: UserRequest):
        if UserRepository.exists_by_name(self.db, userRequest.name):
            return False, "Username exists"
        
        # is SN invalid
        sn: SN = SNRepository.find_by_sn(self.db, userRequest.SN)
        if not sn or sn.is_used:
            return False, "Invalid SN"
        
        # init user
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = User(name = userRequest.name, phone = userRequest.phone, SN = userRequest.SN, password = pwd_context.hash(userRequest.password))
        user = UserRepository.save(self.db, user)

        # init session
        session = UserSession(name = "MAIN", user_id = user.id, summary = "", is_active = True)
        UserSessionRepository.save(self.db, session)

        # init user config
        user_config = UserConfig(user_id = user.id, ai_name = "", ai_role = "", ai_profile = "", styled_role_id = 1, child_name = "", child_age = 3, child_profile = "", child_sex = "boy", learning = "")
        UserConfigRepository.save(self.db, user_config)

        # sn used
        sn.is_used = True
        SNRepository.save(self.db, sn)

        return True, user
        
        
    def find_all_airoles(self):
        return AIRoleRepository.find_all(self.db)
        
    def get_ai_role(self, role_id: int):
        return AIRoleRepository.find_by_id(self.db, role_id)

    def get_user_config(self, user_id: int):
        return UserConfigRepository.find_by_id(self.db, user_id)
    
    def update_user_styled_role(self, user_id: int, styled_role_id: int):
        user_config = UserConfigRepository.find_by_user_id(self.db, user_id)
        if not user_config:
            return False, "User not found"
        user_config.styled_role_id = styled_role_id
        UserConfigRepository.save(self.db, user_config)
        return True, ""
    
    def update_custom_ai_role(self, user_id: int, custom_ai: CustomAIRequest):
        user_config = UserConfigRepository.find_by_user_id(self.db, user_id)
        if not user_config:
            return False, "User not found"
        user_config.ai_name = custom_ai.ai_name
        user_config.ai_role = custom_ai.ai_role
        user_config.ai_timbre = custom_ai.ai_timbre
        user_config.ai_timbre_name = custom_ai.ai_timbre_name
        user_config.ai_tts_model = custom_ai.ai_tts_model
        user_config.ai_profile = custom_ai.ai_profile

        user_config.styled_role_id = None
        UserConfigRepository.save(self.db, user_config)
        return True, ""
    
    def enable_game(self, user_id: int, game_id: int):
        game: Game = GameRepository.find_by_id(self.db, game_id)
        if not game:
            return False, "Game not found"
        user_config: UserConfig = UserConfigRepository.find_by_user_id(self.db, user_id)
        if not user_config:
            return False, "User not found"
        
        user_config.game_enable = True
        user_config.game_id = game_id
        UserConfigRepository.save(self.db, user_config)

        # create a new session
        session = UserSession(name = "GAME:"+str(game_id), user_id = user_id, summary = "", is_active = True)
        UserSessionRepository.save(self.db, session)

        # make MAIN session inactive
        session = UserSessionRepository.find_by_name(self.db, user_id, "MAIN")
        session.is_active = False
        UserSessionRepository.save(self.db, session)
        return True, ""
    
    def disable_game(self, user_id: int):
        user_config = UserConfigRepository.find_by_user_id(self.db, user_id)
        if not user_config:
            return False, "User not found"

        # update current session
        session = UserSessionRepository.find_by_name(self.db, user_id, "GAME:"+str(user_config.game_id))
        if session:
            UserSessionRepository.delete_by_id(self.db, session.id)
        # make MAIN session active
        session = UserSessionRepository.find_by_name(self.db, user_id, "MAIN")
        session.is_active = True
        UserSessionRepository.save(self.db, session)

        # update user config
        user_config.game_enable = False
        user_config.game_id = None
        UserConfigRepository.save(self.db, user_config)
        return True, ""
        
    def get_user_sessions(self, user_id: int):
        return UserSessionRepository.find_by_user(self.db, user_id)
    
    def get_active_session(self, user_id: int):
        return UserSessionRepository.find_by_active(self.db, user_id)
