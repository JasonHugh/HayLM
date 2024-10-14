from db.repositories import *
from util.schemas import *
from db.database import DatabaseUtil

class UserService:
    def __init__(self):
        self.db = DatabaseUtil.get_session()

    def login(self):
        pass

    def register(self, userRequest: UserRequest):
        if UserRepository.exists_by_name(self.db, userRequest.name):
            return False, "Username exists"
        
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
        
    
