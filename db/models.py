from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base

class User(Base):
    __tablename__ = "USER"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(255), nullable=False, unique=True)
    phone: str = Column(String(255), nullable=False, unique=True)
    SN: str = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)

class UserConfig(Base):
    __tablename__ = "USER_CONFIG"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(Integer)
    ai_name: str = Column(String(255), nullable=False)
    ai_role: str = Column(String(255), nullable=False)
    ai_profile: str = Column(String(1000), nullable=False)
    styled_role_id: int = Column(Integer)
    child_name: str = Column(String(255), nullable=False)
    child_sex: str = Column(String(255), nullable=False)
    child_age: int = Column(Integer)
    child_profile: str = Column(String(1000), nullable=False)
    learning: str = Column(String(1000), nullable=False)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)


class AIRole(Base):
    __tablename__ = "AI_ROLE"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ai_name: str = Column(String(255), nullable=False)
    role_name: str = Column(String(255), nullable=False)
    context: str = Column(String(255), nullable=False)
    profile: str = Column(String(255), nullable=False)
    timbre: str = Column(String(255), nullable=False)
    tts_model: str = Column(String(255), nullable=False)
    audio_path: str = Column(String(255), nullable=False)
    avatar_path: str = Column(String(255), nullable=False)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)

class History(Base):
    __tablename__ = "HISTORY"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(Integer)
    session_id: int = Column(Integer)
    role: str = Column(String(255), nullable=False)
    content: str = Column(String, nullable=False)
    is_important: bool = Column(Boolean, nullable=False)
    create_time: str = Column(String(255), nullable=False)