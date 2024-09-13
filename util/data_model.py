from pydantic import BaseModel, StringConstraints, AllowInfNan
from typing_extensions import Annotated

class User(BaseModel):
    id: int = None
    name: Annotated[str, StringConstraints(min_length=3, max_length=10)]
    phone: Annotated[str, StringConstraints(pattern=r'^1\d{10}$')]
    SN: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    password: str
    create_time: str = None
    update_time: str = None


class UserConfig(BaseModel):
    id: int = None
    user_id: int = None
    ai_name: Annotated[str, StringConstraints(min_length=0, max_length=255)]
    played_role: Annotated[str, StringConstraints(min_length=0, max_length=255)]
    child_name: Annotated[str, StringConstraints(min_length=0, max_length=255)]
    child_sex: Annotated[str, StringConstraints(pattern=r'boy|girl')]
    child_age: int
    child_profile: str = None
    learning: str = None
    create_time: str = None
    update_time: str = None

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

if __name__ == "__main__":
    User.model_validate()