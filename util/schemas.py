from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated
from typing import Optional

class UserBase(BaseModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=16)]
    phone: Annotated[str, StringConstraints(pattern=r'^1\d{10}$')]
    SN: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    
class UserRequest(UserBase):
    password: Annotated[Optional[str], StringConstraints(min_length=6)]

class UserResponse(UserBase):
    id: int
    create_time: str
    update_time: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserConfigBase(BaseModel):
    styled_role_id: int
    child_name: Annotated[str, StringConstraints(min_length=1, max_length=16)]
    child_sex: Annotated[str, StringConstraints(min_length=1, max_length=16)]
    child_age: int
    child_profile: Annotated[str, StringConstraints(min_length=1, max_length=1000)]
    learning: Annotated[str, StringConstraints(min_length=1, max_length=1000)]

class UserConfigRequest(UserConfigBase):
    pass

class CustomAIRequest(BaseModel):
    ai_name: Annotated[str, StringConstraints(min_length=1, max_length=16)]
    ai_role: Annotated[str, StringConstraints(min_length=1, max_length=16)]
    ai_timbre_name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    ai_timbre: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    ai_tts_model: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    ai_profile: Annotated[str, StringConstraints(min_length=1, max_length=1000)]

class UserConfigResponse(UserConfigBase):
    id: int
    create_time: str
    update_time: str
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True