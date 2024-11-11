from sqlalchemy.orm import Session
from .models import *
from datetime import datetime

def get_current_time():
    return datetime.now().strftime("%y-%m-%d %H:%M:%S")

class UserRepository:
    @staticmethod
    def find_all(db: Session) -> list:
        return db.query(User).all()

    @staticmethod
    def save(db: Session, user: User) -> User:
        if user.id:
            user.update_time = get_current_time()
            db.merge(user)
        else:
            user.create_time = get_current_time()
            user.update_time = get_current_time()
            db.add(user)
        db.commit()
        return user

    @staticmethod
    def find_by_id(db: Session, id: int) -> User:
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def exists_by_name(db: Session, name: str) -> bool:
        return db.query(User).filter(User.name == name).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        user = db.query(User).filter(User.id == id).first()
        if user is not None:
            db.delete(user)
            db.commit()

class UserConfigRepository:
    @staticmethod
    def find_all(db: Session) -> list:
        return db.query(UserConfig).all()

    @staticmethod
    def save(db: Session, user_config: UserConfig) -> UserConfig:
        if user_config.id:
            user_config.update_time = get_current_time()
            db.merge(user_config)
        else:
            user_config.create_time = get_current_time()
            user_config.update_time = get_current_time()
            db.add(user_config)
        db.commit()
        return user_config

    @staticmethod
    def find_by_id(db: Session, id: int) -> UserConfig:
        return db.query(UserConfig).filter(UserConfig.id == id).first()
    
    @staticmethod
    def find_by_user_id(db: Session, user_id: int) -> UserConfig:
        return db.query(UserConfig).filter(UserConfig.user_id == user_id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(UserConfig).filter(UserConfig.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        user_config = db.query(UserConfig).filter(UserConfig.id == id).first()
        if user_config is not None:
            db.delete(user_config)
            db.commit()

class AIRoleRepository:
    @staticmethod
    def find_all(db: Session) -> list[AIRole]:
        return db.query(AIRole).all()

    @staticmethod
    def save(db: Session, ai_role: AIRole) -> AIRole:
        if ai_role.id:
            ai_role.update_time = get_current_time()
            db.merge(ai_role)
        else:
            ai_role.create_time = get_current_time()
            ai_role.update_time = get_current_time()
            db.add(ai_role)
        db.commit()
        return ai_role

    @staticmethod
    def find_by_id(db: Session, id: int) -> AIRole:
        return db.query(AIRole).filter(AIRole.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(AIRole).filter(AIRole.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        ai_role = db.query(AIRole).filter(AIRole.id == id).first()
        if ai_role is not None:
            db.delete(ai_role)
            db.commit()


class HistoryRepository:
    @staticmethod
    def find_all(db: Session) -> list:
        return db.query(History).all()
    
    @staticmethod
    def find_by_user(db: Session, user_id: int, session_id: int, date: str, is_important: bool) -> History:
        return db.query(History).filter(History.user_id == user_id and History.session_id == user_id).all()

    @staticmethod
    def save(db: Session, history: History) -> History:
        if history.id:
            db.merge(history)
        else:
            db.add(history)
        db.commit()
        return history

    @staticmethod
    def find_by_id(db: Session, id: int) -> History:
        return db.query(History).filter(History.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(History).filter(History.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        history = db.query(History).filter(History.id == id).first()
        if history is not None:
            db.delete(history)
            db.commit()

class SNRepository:
    @staticmethod
    def find_all(db: Session) -> list:
        return db.query(SN).all()

    @staticmethod
    def save(db: Session, sn: SN) -> History:
        if sn.id:
            sn.update_time = get_current_time()
            db.merge(sn)
        else:
            sn.create_time = get_current_time()
            sn.update_time = get_current_time()
            db.add(sn)
        db.commit()
        return sn

    @staticmethod
    def find_by_id(db: Session, id: int) -> SN:
        return db.query(SN).filter(SN.id == id).first()

    @staticmethod
    def find_by_sn(db: Session, sn: str) -> bool:
        return db.query(SN).filter(SN.sn == sn).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        sn = db.query(SN).filter(SN.id == id).first()
        if sn is not None:
            db.delete(sn)
            db.commit()

class UserSessionRepository:
    @staticmethod
    def find_all(db: Session) -> list:
        return db.query(UserSession).all()

    @staticmethod
    def save(db: Session, us: UserSession) -> History:
        if us.id:
            us.update_time = get_current_time()
            db.merge(us)
        else:
            us.create_time = get_current_time()
            us.update_time = get_current_time()
            db.add(us)
        db.commit()
        return us

    @staticmethod
    def find_by_id(db: Session, id: int) -> UserSession:
        return db.query(UserSession).filter(UserSession.id == id).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        us = db.query(UserSession).filter(UserSession.id == id).first()
        if us is not None:
            db.delete(us)
            db.commit()