from pydantic import BaseModel

class GameResponse(BaseModel):
    id: int
    title: str
    short_desc: str
    desc: str 
    timbre: str 
    tts_model: str 
    audio_path: str 
    icon_path: str
    banner_path: str
    is_vip: bool
    is_banner: bool
    create_time: str
    update_time: str

    class Config:
        from_attributes = True