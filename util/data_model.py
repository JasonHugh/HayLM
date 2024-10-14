from pydantic import BaseModel, StringConstraints
from typing_extensions import Annotated
from typing import Optional

class User(BaseModel):
    id: int = None
    name: Annotated[str, StringConstraints(min_length=3, max_length=16)]
    phone: Annotated[str, StringConstraints(pattern=r'^1\d{10}$')]
    SN: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    password: str
    create_time: str = None
    update_time: str = None


class UserConfig(BaseModel):
    id: int = Optional[int]
    user_id: Optional[int]
    ai_name: Annotated[Optional[str], StringConstraints(min_length=0, max_length=255)]
    ai_role: Annotated[Optional[str], StringConstraints(min_length=0, max_length=255)]
    ai_profile: Annotated[Optional[str], StringConstraints(min_length=0, max_length=900)]
    styled_role_id: Optional[int]
    child_name: Annotated[str, StringConstraints(min_length=0, max_length=255)]
    child_sex: Annotated[str, StringConstraints(pattern=r'boy|girl')]
    child_age: int
    child_profile: Annotated[Optional[str], StringConstraints(min_length=0, max_length=900)]
    learning: Annotated[Optional[str], StringConstraints(min_length=0, max_length=900)]
    create_time: Optional[str]
    update_time: Optional[str]

class Session(BaseModel):
    id: int = None
    user_id: int = None
    name: Annotated[str, StringConstraints(min_length=0, max_length=255)]
    summary: str
    is_active: bool
    create_time: str
    update_time: str

class History(BaseModel):
    id: int = None
    user_id: int = None
    session_id: int = None
    role: Annotated[str, StringConstraints(pattern=r'user|assistant')]
    content: str
    is_important: bool = None
    create_time: str = None


class Report(BaseModel):
    id: int = None
    user_id: int = None
    session_id: int = None
    title: str
    key_words: str
    content: str
    start_date: str
    end_date: str
    create_time: str

class SN(BaseModel):
    id: int = None
    SN: str = None
    is_used: bool = False
    create_time: Optional[str]
    update_time: Optional[str]


class AIRole(BaseModel):
    id: Optional[int]
    ai_name: str
    role_name: str
    context: str
    profile: str
    timbre: str
    tts_model: str
    create_time: str
    update_time: str


if __name__ == "__main__":
    User.model_validate()