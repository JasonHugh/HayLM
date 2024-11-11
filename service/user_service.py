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
        
    
