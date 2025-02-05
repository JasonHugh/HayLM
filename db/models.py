from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base

class User(Base):
    __tablename__ = "USER"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(255), nullable=False, unique=True)
    phone: str = Column(String(11), nullable=False, unique=True)
    SN: str = Column(String(11), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)

class UserConfig(Base):
    __tablename__ = "USER_CONFIG"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(Integer)
    ai_name: str = Column(String(255), nullable=False)
    ai_role: str = Column(String(255), nullable=False)
    ai_timbre_name: str = Column(String(255), nullable=False)
    ai_timbre: str = Column(String(255), nullable=False)
    ai_tts_model: str = Column(String(255), nullable=False)
    ai_profile: str = Column(String(1000), nullable=False)
    styled_role_id: int = Column(Integer)
    child_name: str = Column(String(255), nullable=False)
    child_sex: str = Column(String(255), nullable=False)
    child_age: int = Column(Integer)
    child_profile: str = Column(String(1000), nullable=False)
    learning: str = Column(String(1000), nullable=False)
    game_enable: bool = Column(Boolean, nullable=False)
    game_id: int = Column(Integer)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)


class UserSession(Base):
    __tablename__ = "SESSION"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: int = Column(Integer)
    name: str = Column(String(255), nullable=False)
    summary: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, nullable=False)
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
    create_time= Column(DateTime, nullable=False)


class Game(Base):
    __tablename__ = "GAME"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title: str = Column(String(255), nullable=False)
    short_desc: str = Column(String(255), nullable=False)
    desc: str = Column(String(2000), nullable=False)
    prompt: str = Column(String(100000), nullable=False)
    timbre: str = Column(String(255), nullable=False)
    tts_model: str = Column(String(255), nullable=False)
    audio_path: str = Column(String(255), nullable=False)
    icon_path: str = Column(String(255), nullable=False)
    banner_path: str = Column(String(255), nullable=False)
    is_vip: bool = Column(Boolean, nullable=False)
    is_banner: bool = Column(Boolean, nullable=False)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)

class SN(Base):
    __tablename__ = "SN"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sn: str = Column(String(11), nullable=False)
    is_used: bool = Column(Boolean, nullable=False)
    create_time: str = Column(String(255), nullable=False)
    update_time: str = Column(String(255), nullable=False)